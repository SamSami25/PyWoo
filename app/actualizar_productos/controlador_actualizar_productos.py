# app/actualizar_productos/controlador_actualizar_productos.py
import csv
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

from openpyxl import load_workbook, Workbook
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont

from app.core.cliente_woocommerce import ClienteWooCommerce


HEADERS_UI = [
    "SKU", "NOMBRE", "CATEGORÍA",
    "STOCK ACTUAL", "STOCK NUEVO",
    "PRECIO ACTUAL", "PRECIO COMPRA",
    "PRECIO VENTA ACTUAL", "PRECIO VENTA NUEVO",
    "ESTADO"
]

COL_SKU = 0
COL_NOMBRE = 1
COL_CATEGORIA = 2
COL_STOCK_ACTUAL = 3
COL_STOCK_NUEVO = 4
COL_PRECIO_ACTUAL = 5
COL_PRECIO_COMPRA = 6
COL_PRECIO_VENTA_ACTUAL = 7
COL_PRECIO_VENTA_NUEVO = 8
COL_ESTADO = 9


def _norm_header(h: Any) -> str:
    if h is None:
        return ""
    return " ".join(str(h).strip().upper().split())


def _leer_num_opcional(valor: Any) -> Optional[float]:
    if valor is None:
        return None
    txt = str(valor).strip()
    if txt == "":
        return None
    txt = txt.replace(",", ".")
    try:
        return float(txt)
    except Exception:
        return None


def _mapear_columna(headers: List[str], aliases: List[str], requerido: bool, nombre_para_error: str) -> Optional[int]:
    aliases_norm = [_norm_header(a) for a in aliases]
    for a in aliases_norm:
        if a in headers:
            return headers.index(a)
    if requerido:
        raise ValueError(
            f"Falta la columna requerida '{nombre_para_error}'. "
            f"Se aceptan: {', '.join(aliases)}"
        )
    return None


def _validar_negrita_excel(ws, idxs_requeridos: List[int], nombres_requeridos: List[str]):
    for idx, nombre in zip(idxs_requeridos, nombres_requeridos):
        celda = ws.cell(row=1, column=idx + 1)
        bold = bool(getattr(celda.font, "bold", False))
        if not bold:
            raise ValueError(f"En Excel, el encabezado '{nombre}' debe estar en NEGRITA.")


@dataclass
class RegistroProducto:
    sku: str
    nombre: str
    categoria: str
    stock_actual: Any
    stock_nuevo: Optional[int]
    precio_actual: Any
    precio_compra: Any
    precio_venta_actual: Any
    precio_venta_nuevo: Optional[float]
    estado: str = ""

    _id: Optional[int] = None
    _tipo: str = "simple"          # simple | variable | variation
    _parent_id: Optional[int] = None  # ✅ necesario para variation

    def como_fila(self) -> List[Any]:
        return [
            self.sku,
            self.nombre,
            self.categoria,
            self.stock_actual,
            "" if self.stock_nuevo is None else self.stock_nuevo,
            self.precio_actual,
            self.precio_compra,
            self.precio_venta_actual,
            "" if self.precio_venta_nuevo is None else self.precio_venta_nuevo,
            self.estado,
        ]

    def tiene_cambios(self) -> bool:
        return (self.stock_nuevo is not None) or (self.precio_venta_nuevo is not None)


class ModeloActualizarProductos(QAbstractTableModel):
    def __init__(self, registros: List[RegistroProducto]):
        super().__init__()
        self._registros = registros

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._registros)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(HEADERS_UI)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        r = self._registros[index.row()]
        fila = r.como_fila()
        valor = fila[index.column()]

        if role in (Qt.DisplayRole, Qt.EditRole):
            return valor

        if role == Qt.TextAlignmentRole:
            if index.column() in (
                COL_STOCK_ACTUAL, COL_STOCK_NUEVO,
                COL_PRECIO_ACTUAL, COL_PRECIO_COMPRA,
                COL_PRECIO_VENTA_ACTUAL, COL_PRECIO_VENTA_NUEVO,
                COL_ESTADO
            ):
                return Qt.AlignCenter
            return Qt.AlignVCenter

        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        if index.column() in (COL_STOCK_NUEVO, COL_PRECIO_VENTA_NUEVO):
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        if not index.isValid() or role != Qt.EditRole:
            return False

        r = self._registros[index.row()]

        try:
            if index.column() == COL_STOCK_NUEVO:
                txt = str(value).strip()
                r.stock_nuevo = None if txt == "" else int(float(txt))
                if r.stock_nuevo is not None and r.stock_nuevo < 0:
                    return False

            elif index.column() == COL_PRECIO_VENTA_NUEVO:
                txt = str(value).strip().replace(",", ".")
                r.precio_venta_nuevo = None if txt == "" else float(txt)
                if r.precio_venta_nuevo is not None and r.precio_venta_nuevo < 0:
                    return False
            else:
                return False
        except Exception:
            return False

        self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
        return True

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return HEADERS_UI[section]
            if role == Qt.FontRole:
                f = QFont()
                f.setBold(True)
                return f
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
        return None

    def actualizar_estado(self, row: int, estado: str):
        if 0 <= row < len(self._registros):
            self._registros[row].estado = estado
            idx = self.index(row, COL_ESTADO)
            self.dataChanged.emit(idx, idx, [Qt.DisplayRole])


class ControladorActualizarProductos:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self.simples: List[RegistroProducto] = []
        self.variados: List[RegistroProducto] = []
        self.modelo_simples: Optional[ModeloActualizarProductos] = None
        self.modelo_variados: Optional[ModeloActualizarProductos] = None

    def cargar_archivo(self, ruta: str) -> Dict[str, Dict[str, Optional[float]]]:
        data: Dict[str, Dict[str, Optional[float]]] = {}

        ruta_lower = ruta.lower()
        if ruta_lower.endswith(".xls"):
            raise ValueError("Archivos .xls no son soportados. Guarda como .xlsx y vuelve a intentar.")

        SKU_ALIASES = ["SKU"]
        STOCK_ALIASES = ["STOCK", "STOCK NUEVO", "NUEVO STOCK"]
        PRECIO_ALIASES = ["PRECIO", "PRECIO VENTA", "PRECIO_VENTA", "PRECIO VENTA NUEVO", "PRECIO_VENTA_NUEVO"]

        if ruta_lower.endswith(".csv"):
            with open(ruta, encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames:
                    raise ValueError("El CSV no tiene encabezados.")
                headers = [_norm_header(h) for h in reader.fieldnames]

                idx_sku_name = _mapear_columna(headers, SKU_ALIASES, True, "SKU")
                idx_stock_name = _mapear_columna(headers, STOCK_ALIASES, False, "STOCK")
                idx_precio_name = _mapear_columna(headers, PRECIO_ALIASES, True, "PRECIO")

                name_sku = reader.fieldnames[idx_sku_name]
                name_stock = reader.fieldnames[idx_stock_name] if idx_stock_name is not None else None
                name_precio = reader.fieldnames[idx_precio_name]

                for r in reader:
                    sku = (r.get(name_sku) or "").strip()
                    if not sku:
                        continue

                    stock = _leer_num_opcional(r.get(name_stock)) if name_stock else None
                    precio = _leer_num_opcional(r.get(name_precio))

                    data[sku] = {
                        "STOCK": None if stock is None else int(stock),
                        "PRECIO": None if precio is None else float(precio),
                    }

        else:
            wb = load_workbook(ruta, data_only=True)
            ws = wb.active

            raw_headers = [c.value for c in ws[1]]
            headers = [_norm_header(h) for h in raw_headers]

            idx_sku = _mapear_columna(headers, SKU_ALIASES, True, "SKU")
            idx_stock = _mapear_columna(headers, STOCK_ALIASES, False, "STOCK")
            idx_precio = _mapear_columna(headers, PRECIO_ALIASES, True, "PRECIO")

            _validar_negrita_excel(
                ws,
                idxs_requeridos=[idx_sku, idx_precio],
                nombres_requeridos=["SKU", "PRECIO"],
            )

            for row in ws.iter_rows(min_row=2, values_only=True):
                sku = str(row[idx_sku] or "").strip()
                if not sku:
                    continue

                stock = _leer_num_opcional(row[idx_stock]) if idx_stock is not None else None
                precio = _leer_num_opcional(row[idx_precio])

                data[sku] = {
                    "STOCK": None if stock is None else int(stock),
                    "PRECIO": None if precio is None else float(precio),
                }

        return data

    # ✅ AHORA incluye variaciones
    def procesar_productos(
        self,
        datos_archivo: Dict[str, Dict[str, Optional[float]]],
        callback: Optional[Callable[[int, str], None]] = None
    ) -> Tuple[ModeloActualizarProductos, ModeloActualizarProductos]:

        productos = self.cliente.obtener_productos(incluir_variaciones=True)

        self.simples.clear()
        self.variados.clear()

        total = max(len(productos), 1)

        for i, p in enumerate(productos, start=1):
            sku = (p.get("sku") or "").strip()
            excel = datos_archivo.get(sku) if sku else None

            stock_nuevo = excel.get("STOCK") if excel else None
            precio_nuevo = excel.get("PRECIO") if excel else None

            tipo = (p.get("type") or "simple")
            tipo = str(tipo).strip().lower()

            registro = RegistroProducto(
                sku=sku,
                nombre=p.get("name", ""),
                categoria=", ".join(c.get("name", "") for c in (p.get("categories") or [])),
                stock_actual=p.get("stock_quantity", 0),
                stock_nuevo=stock_nuevo,
                precio_actual=p.get("price", 0),
                precio_compra=p.get("purchase_price", 0),
                precio_venta_actual=p.get("regular_price", p.get("price", 0)),
                precio_venta_nuevo=precio_nuevo,
                estado="",
                _id=p.get("id"),
                _tipo=tipo,
                _parent_id=p.get("parent_id"),
            )

            # simple -> hoja simples
            # variable y variation -> hoja variados
            if registro._tipo == "simple":
                self.simples.append(registro)
            else:
                self.variados.append(registro)

            if callback:
                callback(int((i / total) * 100), f"Procesando producto {i} de {total}")

        self.modelo_simples = ModeloActualizarProductos(self.simples)
        self.modelo_variados = ModeloActualizarProductos(self.variados)
        return self.modelo_simples, self.modelo_variados

    def aplicar_cambios(self, callback: Optional[Callable[[int, str], None]] = None):
        trabajos: List[Tuple[ModeloActualizarProductos, int, RegistroProducto]] = []

        if self.modelo_simples:
            for idx, r in enumerate(self.simples):
                if r.tiene_cambios():
                    trabajos.append((self.modelo_simples, idx, r))

        if self.modelo_variados:
            for idx, r in enumerate(self.variados):
                if r.tiene_cambios():
                    trabajos.append((self.modelo_variados, idx, r))

        total = max(len(trabajos), 1)

        for i, (modelo, row, r) in enumerate(trabajos, start=1):
            if not r._id:
                modelo.actualizar_estado(row, "❌ Sin ID")
                continue

            try:
                # ✅ simple
                if r._tipo == "simple":
                    self.cliente.actualizar_producto(
                        producto_id=int(r._id),
                        stock=r.stock_nuevo if r.stock_nuevo is not None else None,
                        precio=r.precio_venta_nuevo if r.precio_venta_nuevo is not None else None,
                    )
                    modelo.actualizar_estado(row, "✔ Actualizado")

                # ✅ variation (necesita parent_id)
                elif r._tipo == "variation":
                    if not r._parent_id:
                        modelo.actualizar_estado(row, "❌ Sin parent_id")
                    else:
                        self.cliente.actualizar_variacion(
                            parent_id=int(r._parent_id),
                            variacion_id=int(r._id),
                            stock=r.stock_nuevo if r.stock_nuevo is not None else None,
                            precio=r.precio_venta_nuevo if r.precio_venta_nuevo is not None else None,
                        )
                        modelo.actualizar_estado(row, "✔ Variación actualizada")

                # variable padre: no se actualiza directo (depende de tienda), pero ya tienes variaciones
                else:
                    modelo.actualizar_estado(row, "ℹ Variable (se actualiza por variaciones)")

            except Exception as e:
                modelo.actualizar_estado(row, f"❌ {str(e)[:80]}")

            if callback:
                callback(int((i / total) * 100), f"Aplicando cambios {i} de {total}")

    def exportar_excel(self, ruta: str):
        wb = Workbook()

        ws1 = wb.active
        ws1.title = "Productos Simples"
        ws1.append(HEADERS_UI)
        for r in self.simples:
            ws1.append(r.como_fila())

        ws2 = wb.create_sheet("Productos Variados")
        ws2.append(HEADERS_UI)
        for r in self.variados:
            ws2.append(r.como_fila())

        wb.save(ruta)
