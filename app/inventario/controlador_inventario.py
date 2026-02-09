# app/inventario/controlador_inventario.py
from __future__ import annotations

from typing import Any, Optional
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.column_utils import prune_empty_columns

HEADERS = ["SKU", "NOMBRE", "CATEGORÍA", "STOCK", "PRECIO", "ESTADO"]
COLUMN_KEYS = ["sku", "nombre", "categoria", "stock", "precio", "estado"]


def _safe_str(x) -> str:
    if x is None:
        return "N/A"
    s = str(x)
    return s if s.strip() else "N/A"


def _to_float(x: Any) -> float:
    """Float seguro (para export) usando Decimal para evitar errores."""
    d = _to_dec(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if d < 0:
        d = Decimal("0")
    return float(d)


def _to_int(x: Any) -> int:
    try:
        if x is None or x == "":
            return 0
        return int(float(str(x).strip().replace(",", ".")))
    except Exception:
        return 0


def _to_dec(x: Any) -> Decimal:
    if x is None or x == "":
        return Decimal("0")
    s = str(x).strip().replace(",", ".")
    try:
        return Decimal(s)
    except (InvalidOperation, ValueError):
        return Decimal("0")


def _fmt_precio(x) -> str:
    d = _to_dec(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if d < 0:
        d = Decimal("0")
    return f"{d}"


def _join_categorias(p: dict) -> str:
    return ", ".join((c.get("name") or "") for c in (p.get("categories") or [])).strip(", ").strip()


def _stock_no_negativo(stock: int) -> int:
    return stock if stock > 0 else 0


def _bool_manage_stock(obj: dict) -> bool:
    return bool(obj.get("manage_stock"))


def _stock_status(obj: dict) -> str:
    return (obj.get("stock_status") or "").strip().lower()  # instock / outofstock / onbackorder ...


def _estado_texto(stock: int, filtro: str, manage_stock: bool, stock_status: str) -> str:
    """
    Si manage_stock=False, el estado real lo determina stock_status.
    Si manage_stock=True, el estado lo determina stock_quantity.
    """
    if not manage_stock:
        # Estado por stock_status (sin inventar cantidades)
        if stock_status == "instock":
            return "En Stock"
        return "Sin Stock"

    # manage_stock=True => estado por stock
    if filtro == "sin_stock":
        return "Agotado"
    if filtro == "con_stock":
        return f"Se dispone de {stock} unidades"
    return "En Stock" if stock > 0 else "Sin Stock"


def _pasa_filtro(filtro: str, stock: int, manage_stock: bool, stock_status: str) -> bool:
    """
    - con_stock: si manage_stock=False => instock cuenta como con stock
    - sin_stock: si manage_stock=False => todo lo que no sea instock cuenta como sin stock
    """
    if filtro == "todos":
        return True

    if not manage_stock:
        if filtro == "con_stock":
            return stock_status == "instock"
        if filtro == "sin_stock":
            return stock_status != "instock"
        return True

    # manage_stock=True
    if filtro == "con_stock":
        return stock > 0
    if filtro == "sin_stock":
        return stock <= 0
    return True


class ModeloTablaInventario(QAbstractTableModel):
    """
    - PRECIO: 2 decimales
    - STOCK: entero (nunca negativo)
    - ESTADO:
        - si manage_stock=False => En Stock / Sin Stock según stock_status
        - si manage_stock=True  => según stock_quantity y filtro
    """

    def __init__(self, datos: list[dict], filtro: str, headers: list[str], keys: list[str]):
        super().__init__()
        self._datos = datos
        self._filtro = filtro
        self._headers = headers
        self._keys = keys

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(self._keys)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        fila = self._datos[index.row()]
        clave = self._keys[index.column()]
        val = fila.get(clave, "")

        if role == Qt.DisplayRole:
            if clave == "precio":
                return _fmt_precio(val)

            if clave == "stock":
                return str(_stock_no_negativo(_to_int(val)))

            if clave == "estado":
                stock = _stock_no_negativo(_to_int(fila.get("stock")))
                manage_stock = bool(fila.get("__manage_stock__", False))
                stock_status = _safe_str(fila.get("__stock_status__", "")).lower().strip()
                return _estado_texto(stock, self._filtro, manage_stock, stock_status)

            return _safe_str(val)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._headers[section]
            if role == Qt.FontRole:
                f = QFont()
                f.setBold(True)
                return f
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
        return None


class ControladorInventario:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self._simples: list[dict] = []
        self._variados: list[dict] = []
        self._ultimo_filtro: str = "todos"
        self._headers = list(HEADERS)
        self._keys = list(COLUMN_KEYS)

    @property
    def simples(self):
        return self._simples

    @property
    def variados(self):
        return self._variados

    # -----------------------------
    # Helpers variaciones
    # -----------------------------
    def _nombre_variacion(self, producto: dict, variacion: dict) -> str:
        base = (producto.get("name") or "").strip()
        attrs = variacion.get("attributes") or []
        parts = []
        for a in attrs:
            n = (a.get("name") or "").strip()
            o = (a.get("option") or "").strip()
            if n and o:
                parts.append(f"{n}: {o}")
        if parts:
            return f"{base} ({' | '.join(parts)})"
        return base or "Variación"

    # -----------------------------
    # GENERAR
    # -----------------------------
    def generar_inventario(self, filtro: str, callback_progreso=None):
        self._ultimo_filtro = filtro

        # ✅ Tu cliente YA pagina productos, así que esto trae TODOS.
        productos = self.cliente.obtener_productos(per_page=100, filtro_stock=None)
        total = max(len(productos), 1)

        self._simples.clear()
        self._variados.clear()

        for i, p in enumerate(productos, start=1):
            tipo = (p.get("type") or "").strip().lower()
            categorias = _join_categorias(p)

            if tipo == "variable":
                producto_id = p.get("id")
                if not producto_id:
                    continue

                # ✅ traer TODAS las variaciones (tu cliente ya pagina)
                variaciones = self.cliente.obtener_variaciones_producto(int(producto_id), per_page=100)

                for v in variaciones:
                    manage = _bool_manage_stock(v)
                    st_status = _stock_status(v)

                    stock = _stock_no_negativo(_to_int(v.get("stock_quantity")))
                    if not _pasa_filtro(filtro, stock, manage, st_status):
                        continue

                    precio = v.get("price") or v.get("regular_price") or "0"

                    fila = {
                        "sku": ((v.get("sku") or "").strip() or "(SIN SKU)"),
                        "nombre": (self._nombre_variacion(p, v) or "(SIN NOMBRE)"),
                        # Si NUNCA viene categoría en tu tienda, se oculta la columna.
                        "categoria": (categorias or None),
                        "stock": stock,
                        "precio": _fmt_precio(precio),
                        # Si NUNCA viene estado, se oculta la columna.
                        "estado": ((p.get("status", "") or "").strip() or None),
                        # internos para estado/filtro correctos
                        "__manage_stock__": manage,
                        "__stock_status__": st_status,
                        "__tipo__": "variable",
                    }
                    self._variados.append(fila)

            else:
                manage = _bool_manage_stock(p)
                st_status = _stock_status(p)

                stock = _stock_no_negativo(_to_int(p.get("stock_quantity")))
                if not _pasa_filtro(filtro, stock, manage, st_status):
                    continue

                fila = {
                    "sku": ((p.get("sku") or "").strip() or "(SIN SKU)"),
                    "nombre": ((p.get("name", "") or "").strip() or "(SIN NOMBRE)"),
                    "categoria": (categorias or None),
                    "stock": stock,
                    "precio": _fmt_precio(p.get("price", "0") or "0"),
                    "estado": ((p.get("status", "") or "").strip() or None),
                    "__manage_stock__": manage,
                    "__stock_status__": st_status,
                    "__tipo__": "simple",
                }
                self._simples.append(fila)

            if callback_progreso:
                callback_progreso(int((i / total) * 100), f"Procesando producto {i} de {total}")

        # Quitar columnas opcionales que estén totalmente vacías / inexistentes
        optional = {"categoria", "estado"}
        combinadas = list(self._simples) + list(self._variados)
        self._headers, self._keys = prune_empty_columns(combinadas, HEADERS, COLUMN_KEYS, optional)

        return (
            ModeloTablaInventario(self._simples, filtro, self._headers, self._keys),
            ModeloTablaInventario(self._variados, filtro, self._headers, self._keys),
        )

    # -----------------------------
    # EXPORTAR
    # -----------------------------
    def exportar_excel(self, ruta: str, filtro: Optional[str] = None, simples=None, variados=None):
        if filtro is None:
            filtro = self._ultimo_filtro

        workbook = xlsxwriter.Workbook(ruta)

        header_fmt = workbook.add_format(
            {"bold": True, "align": "center", "valign": "vcenter", "border": 1, "bg_color": "#D9E1F2"}
        )
        text_fmt = workbook.add_format({"border": 1})
        int_fmt = workbook.add_format({"border": 1, "num_format": "0"})
        money_fmt = workbook.add_format({"border": 1, "num_format": "0.00"})

        col_widths = {"sku": 14, "nombre": 44, "categoria": 28, "stock": 10, "precio": 12, "estado": 30}

        datos_simples = simples if simples is not None else self._simples
        datos_variados = variados if variados is not None else self._variados

        for nombre, datos in (("Productos Simples", datos_simples), ("Productos Variados", datos_variados)):
            ws = workbook.add_worksheet(nombre[:31])

            for col, h in enumerate(self._headers):
                ws.write(0, col, h, header_fmt)

            for col, key in enumerate(self._keys):
                ws.set_column(col, col, col_widths.get(key, 18))

            last_row = 0
            for row, fila in enumerate(datos, start=1):
                last_row = row

                stock = _stock_no_negativo(_to_int(fila.get("stock")))
                manage = bool(fila.get("__manage_stock__", False))
                st_status = _safe_str(fila.get("__stock_status__", "")).lower().strip()

                for col, key in enumerate(self._keys):
                    val = fila.get(key, "")

                    if key == "stock":
                        ws.write_number(row, col, stock, int_fmt)
                    elif key == "precio":
                        ws.write_number(row, col, _to_float(val), money_fmt)
                    elif key == "estado":
                        ws.write(row, col, _estado_texto(stock, filtro, manage, st_status), text_fmt)
                    else:
                        ws.write(row, col, _safe_str(val), text_fmt)

            ws.autofilter(0, 0, max(1, last_row), max(0, len(self._headers) - 1))
            ws.freeze_panes(1, 0)

        workbook.close()
