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


@dataclass
class RegistroProducto:
    # Campos visibles
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

    # Campos internos (NO visibles)
    _id: Optional[int] = None
    _tipo: str = "simple"

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

    # --- Qt model API ---
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
            # Centrar columnas numéricas y estado
            if index.column() in (COL_STOCK_ACTUAL, COL_STOCK_NUEVO,
                                  COL_PRECIO_ACTUAL, COL_PRECIO_COMPRA,
                                  COL_PRECIO_VENTA_ACTUAL, COL_PRECIO_VENTA_NUEVO,
                                  COL_ESTADO):
                return Qt.AlignCenter
            return Qt.AlignVCenter

        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        # editable: stock_nuevo y precio_venta_nuevo
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
            elif index.column() == COL_PRECIO_VENTA_NUEVO:
                txt = str(value).strip().replace(",", ".")
                r.precio_venta_nuevo = None if txt == "" else float(txt)
            else:
                return False
        except Exception:
            # Valor inválido -> no lo aceptamos
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

    # --- helpers ---
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

    # -------- CARGAR ARCHIVO --------
    def cargar_archivo(self, ruta: str) -> Dict[str, Dict[str, Optional[float]]]:
        """Devuelve un mapa:
        sku -> {'STOCK': Optional[int], 'PRECIO': Optional[float]}
        Si una celda viene vacía, se interpreta como 'sin cambio' (None).
        """
        data: Dict[str, Dict[str, Optional[float]]] = {}

        def _leer_valor_num(valor):
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

        if ruta.lower().endswith(".csv"):
            with open(ruta, encoding="utf-8-sig", newline="") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    sku = (r.get("SKU") or "").strip()
                    if not sku:
                        continue
                    stock = _leer_valor_num(r.get("STOCK"))
                    precio = _leer_valor_num(r.get("PRECIO VENTA"))
                    data[sku] = {
                        "STOCK": None if stock is None else int(stock),
                        "PRECIO": None if precio is None else float(precio),
                    }
        else:
            wb = load_workbook(ruta, data_only=True)
            ws = wb.active
            headers = [str(c.value).strip().upper() if c.value is not None else "" for c in ws[1]]

            def _idx(nombre: str) -> int:
                nombre = nombre.upper()
                if nombre not in headers:
                    raise ValueError(f"Falta la columna '{nombre}' en el archivo.")
                return headers.index(nombre)

            idx_sku = _idx("SKU")
            idx_stock = _idx("STOCK")
            idx_precio = _idx("PRECIO VENTA")

            for row in ws.iter_rows(min_row=2, values_only=True):
                sku = (row[idx_sku] or "")
                sku = str(sku).strip()
                if not sku:
                    continue
                stock = _leer_valor_num(row[idx_stock])
                precio = _leer_valor_num(row[idx_precio])

                data[sku] = {
                    "STOCK": None if stock is None else int(stock),
                    "PRECIO": None if precio is None else float(precio),
                }

        return data

    # -------- PROCESAR --------
    def procesar_productos(
        self,
        datos_archivo: Dict[str, Dict[str, Optional[float]]],
        callback: Optional[Callable[[int, str], None]] = None
    ) -> Tuple[ModeloActualizarProductos, ModeloActualizarProductos]:
        """Construye las tablas (simples / variados) y retorna los modelos.
        - Importantísimo: usa el ID real del producto para actualizar después.
        - Si un SKU no está en el archivo, NO se fuerza a 0; queda sin cambio (None).
        """
        productos = self.cliente.obtener_productos()
        self.simples.clear()
        self.variados.clear()

        total = max(len(productos), 1)

        for i, p in enumerate(productos, start=1):
            sku = (p.get("sku") or "").strip()
            excel = datos_archivo.get(sku) if sku else None

            stock_nuevo = excel.get("STOCK") if excel else None
            precio_nuevo = excel.get("PRECIO") if excel else None

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
                _tipo=p.get("type", "simple"),
            )

            if registro._tipo == "simple":
                self.simples.append(registro)
            else:
                self.variados.append(registro)

            if callback:
                callback(int((i / total) * 100), f"Procesando producto {i} de {total}")

        self.modelo_simples = ModeloActualizarProductos(self.simples)
        self.modelo_variados = ModeloActualizarProductos(self.variados)
        return self.modelo_simples, self.modelo_variados

    # -------- APLICAR --------
    def aplicar_cambios(self, callback: Optional[Callable[[int, str], None]] = None):
        """Aplica cambios SOLO donde hay datos nuevos (incluye 0).
        Se recomienda ejecutarlo en un QThread (puede tardar).
        """
        # armar lista de trabajos (modelo, row, registro)
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

            # Para productos variables, WooCommerce normalmente maneja precio/stock en variaciones.
            # Aquí marcamos como advertencia si intentan cambiar el padre.
            if r._tipo != "simple":
                modelo.actualizar_estado(row, "⚠ Variable (revisar variaciones)")
                # Si igual quieres forzar actualización del padre, comenta el 'continue'.
                continue

            try:
                self.cliente.actualizar_producto(
                    producto_id=int(r._id),
                    stock=r.stock_nuevo if r.stock_nuevo is not None else None,
                    precio=r.precio_venta_nuevo if r.precio_venta_nuevo is not None else None,
                )
                modelo.actualizar_estado(row, "✔ Actualizado")
            except Exception as e:
                modelo.actualizar_estado(row, f"❌ {str(e)[:40]}")

            if callback:
                callback(int((i / total) * 100), f"Aplicando cambios {i} de {total}")

    # -------- EXPORTAR --------
    def exportar_excel(self, ruta: str):
        wb = Workbook()
        ws = wb.active
        ws.append(HEADERS_UI)

        for r in self.simples + self.variados:
            ws.append(r.como_fila())

        wb.save(ruta)
