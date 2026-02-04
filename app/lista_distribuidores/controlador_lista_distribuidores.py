# app/lista_distribuidores/controlador_lista_distribuidores.py
from __future__ import annotations

from typing import Any, List, Tuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont, QBrush, QColor
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce


# ---------------------------------------
# Columnas INTERNAS (para la tabla del app)
# ---------------------------------------
HEADERS_INTERNAL = [
    "SKU",
    "NOMBRE DEL PRODUCTO",
    "VARIACIÓN",
    "STOCK",
    "PVP",
    "PRECIO COMPRA",
    "GANANCIA",
    "DESCUENTO (%)",
    "DESCUENTO ($)",
    "PVD",
    "OBSERVACIÓN",
    "URL",
]

COL_SKU = 0
COL_NOMBRE = 1
COL_VARIACION = 2
COL_STOCK = 3
COL_PVP = 4
COL_PRECIO_COMPRA = 5
COL_GANANCIA = 6
COL_DESC_PCT = 7
COL_DESC_VAL = 8
COL_PVD = 9
COL_OBS = 10
COL_URL = 11


# ---------------------------------------
# Columnas EXPORT (para distribuidores)
# ---------------------------------------
HEADERS_EXPORT = [
    "SKU",
    "NOMBRE DEL PRODUCTO",
    "VARIACIÓN",
    "STOCK",
    "PVP",
    "PVD",
    "OBSERVACIÓN",
    "URL",
]

EXPORT_COLS_MAP = [
    COL_SKU,
    COL_NOMBRE,
    COL_VARIACION,
    COL_STOCK,
    COL_PVP,
    COL_PVD,
    COL_OBS,
    COL_URL,
]


def _to_float(x: Any) -> float:
    try:
        if x is None:
            return 0.0
        s = str(x).strip().replace(",", ".")
        if s == "":
            return 0.0
        return float(s)
    except Exception:
        return 0.0


def _to_int(x: Any) -> int:
    try:
        if x is None:
            return 0
        s = str(x).strip()
        if s == "":
            return 0
        return int(float(s))
    except Exception:
        return 0


def _safe_str(x: Any) -> str:
    return "" if x is None else str(x)


def _fmt_2_dec_trim(x: Any) -> str:
    """
    Formatea a máximo 2 decimales.
    - 0.36 -> "0.36"
    - 2.0 -> "2"
    - 2.50 -> "2.5"
    """
    try:
        v = float(x)
    except Exception:
        return _safe_str(x)

    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return s


class ModeloTablaDistribuidores(QAbstractTableModel):
    """
    - robusto (no revienta con None)
    - centrado (URL alineada a la izquierda)
    - headers en negrita
    - URL: azul + subrayado + tooltip (cursor se maneja en el view)
    - GANANCIA: máximo 2 decimales (visualmente)
    """

    def __init__(self, datos: List[List[Any]]):
        super().__init__()
        self._datos = datos

        self._font_url = QFont()
        self._font_url.setUnderline(True)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._datos)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(HEADERS_INTERNAL)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        row = index.row()
        col = index.column()

        fila = self._datos[row] if row < len(self._datos) else []
        valor = fila[col] if col < len(fila) else ""

        if role == Qt.TextAlignmentRole:
            if col == COL_URL:
                return Qt.AlignVCenter | Qt.AlignLeft
            return Qt.AlignCenter

        if role == Qt.DisplayRole:
            # ✅ GANANCIA con máximo 2 decimales (solo visual)
            if col == COL_GANANCIA:
                return _fmt_2_dec_trim(valor)
            return _safe_str(valor)

        if col == COL_URL:
            if role == Qt.ForegroundRole:
                return QBrush(QColor("#1e73f1"))
            if role == Qt.FontRole:
                return self._font_url
            if role == Qt.ToolTipRole:
                return _safe_str(valor)

        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return HEADERS_INTERNAL[section]
            if role == Qt.FontRole:
                f = QFont()
                f.setBold(True)
                return f
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter
        return None


class ControladorListaDistribuidores:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self.simples: List[List[Any]] = []
        self.variados: List[List[Any]] = []

    def _por_descuento(self, ganancia: float) -> float:
        if ganancia <= 0.1:
            return 0.0
        if ganancia <= 0.6:
            return 0.4 * ganancia - 0.04
        return 0.20

    def _observacion(self, descuento_pct: float, stock: int) -> str:
        if (descuento_pct * 100) >= 10 and stock > 1:
            return "COMPRA MÍNIMA 2 UNIDADES"
        return ""

    def generar_lista(self, callback_progreso=None) -> Tuple[ModeloTablaDistribuidores, ModeloTablaDistribuidores]:
        productos = self.cliente.obtener_productos(per_page=100)
        total = max(len(productos), 1)

        self.simples.clear()
        self.variados.clear()

        for i, p in enumerate(productos, start=1):
            tipo = (p.get("type") or "").strip().lower()

            if tipo == "simple":
                self._procesar_simple(p)
            elif tipo == "variable":
                self._procesar_variaciones(p)

            if callback_progreso:
                callback_progreso(int((i / total) * 100), f"Procesando producto {i} de {total}")

        return (ModeloTablaDistribuidores(self.simples), ModeloTablaDistribuidores(self.variados))

    def _procesar_simple(self, p: dict):
        stock = _to_int(p.get("stock_quantity"))
        if stock <= 0:
            return

        pvp = _to_float(p.get("price"))
        p_compra = _to_float(p.get("purchase_price"))

        ganancia = (1 - (p_compra / pvp)) if pvp > 0 else 0.0
        descuento_pct = self._por_descuento(ganancia)
        descuento_valor = round(descuento_pct * pvp, 2)
        pvd = round(pvp - descuento_valor, 2)

        self.simples.append([
            (p.get("sku") or "").strip(),
            p.get("name", "") or "",
            "",
            stock,
            round(pvp, 2),
            round(p_compra, 2),
            round(ganancia, 4),  # interno puede quedarse con 4 para cálculos, pero se muestra 2 dec.
            round(descuento_pct * 100, 2),
            descuento_valor,
            pvd,
            self._observacion(descuento_pct, stock),
            p.get("permalink", "") or "",
        ])

    def _procesar_variaciones(self, producto: dict):
        producto_id = producto.get("id")
        if not producto_id:
            return

        try:
            variaciones = self.cliente.obtener_variaciones_producto(int(producto_id), per_page=100)
        except Exception:
            return

        for v in variaciones:
            stock = _to_int(v.get("stock_quantity"))
            if stock <= 0:
                continue

            pvp = _to_float(v.get("price") or v.get("regular_price"))
            p_compra = _to_float(v.get("purchase_price"))

            ganancia = (1 - (p_compra / pvp)) if pvp > 0 else 0.0
            descuento_pct = self._por_descuento(ganancia)
            descuento_valor = round(descuento_pct * pvp, 2)
            pvd = round(pvp - descuento_valor, 2)

            variacion = " | ".join(
                f"{(a.get('name') or '').strip()}: {(a.get('option') or '').strip()}"
                for a in (v.get("attributes") or [])
                if (a.get("name") or "").strip() and (a.get("option") or "").strip()
            ) or "Variación"

            self.variados.append([
                (v.get("sku") or "").strip(),
                producto.get("name", "") or "",
                variacion,
                stock,
                round(pvp, 2),
                round(p_compra, 2),
                round(ganancia, 4),
                round(descuento_pct * 100, 2),
                descuento_valor,
                pvd,
                self._observacion(descuento_pct, stock),
                producto.get("permalink", "") or "",
            ])

    def exportar_excel(self, ruta: str):
        """
        ✅ EXPORT SOLO PARA DISTRIBUIDORES:
        SKU | NOMBRE | VARIACIÓN | STOCK | PVP | PVD | OBSERVACIÓN | URL
        (en 2 hojas: Simples / Variados)
        """
        wb = xlsxwriter.Workbook(ruta)

        header = wb.add_format({
            "bold": True, "align": "center", "valign": "vcenter",
            "border": 1, "bg_color": "#D9E1F2",
        })
        cell = wb.add_format({"border": 1, "align": "center", "valign": "vcenter"})
        money = wb.add_format({"border": 1, "num_format": "#,##0.00", "align": "center", "valign": "vcenter"})
        url_fmt = wb.add_format({"border": 1, "font_color": "blue", "underline": 1})

        # anchos export (8 cols)
        widths = [14, 40, 28, 10, 10, 10, 28, 60]

        for nombre, datos in (("Productos Simples", self.simples), ("Productos Variados", self.variados)):
            ws = wb.add_worksheet(nombre[:31])

            # headers export
            for col, h in enumerate(HEADERS_EXPORT):
                ws.write(0, col, h, header)
                ws.set_column(col, col, widths[col] if col < len(widths) else 18)

            # filas export
            for row_i, fila in enumerate(datos, start=1):
                for out_col, internal_col in enumerate(EXPORT_COLS_MAP):
                    val = fila[internal_col] if internal_col < len(fila) else ""

                    # URL
                    if internal_col == COL_URL:
                        link = _safe_str(val).strip()
                        if link:
                            ws.write_url(row_i, out_col, link, url_fmt, string=link)
                        else:
                            ws.write(row_i, out_col, "", cell)
                        continue

                    # precios (PVP, PVD) -> formato moneda
                    if internal_col in (COL_PVP, COL_PVD):
                        ws.write_number(row_i, out_col, float(_to_float(val)), money)
                        continue

                    # stock -> número entero
                    if internal_col == COL_STOCK:
                        ws.write_number(row_i, out_col, int(_to_int(val)), cell)
                        continue

                    ws.write(row_i, out_col, val, cell)

            ws.freeze_panes(1, 0)
            ws.autofilter(0, 0, max(1, len(datos)), len(HEADERS_EXPORT) - 1)

        wb.close()
