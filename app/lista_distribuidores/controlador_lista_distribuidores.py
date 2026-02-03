# app/lista_distribuidores/controlador_lista_distribuidores.py
from __future__ import annotations

from typing import Any, List, Tuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont, QBrush, QColor
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce


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

COL_URL = HEADERS_INTERNAL.index("URL")


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


class ModeloTablaDistribuidores(QAbstractTableModel):
    """
    - robusto (no revienta con None)
    - centrado (URL alineada a la izquierda)
    - headers en negrita
    - URL: azul + subrayado + tooltip (cursor se maneja en el view)
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

        ganancia = round(1 - (p_compra / pvp), 4) if pvp > 0 else 0.0
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
            ganancia,
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

            ganancia = round(1 - (p_compra / pvp), 4) if pvp > 0 else 0.0
            descuento_pct = self._por_descuento(ganancia)
            descuento_valor = round(descuento_pct * pvp, 2)
            pvd = round(pvp - descuento_valor, 2)

            variacion = " | ".join(
                f"{(a.get('name') or '').strip()}: {(a.get('option') or '').strip()}"
                for a in (v.get("attributes") or [])
            ) or "Variación"

            self.variados.append([
                (v.get("sku") or "").strip(),
                producto.get("name", "") or "",
                variacion,
                stock,
                round(pvp, 2),
                round(p_compra, 2),
                ganancia,
                round(descuento_pct * 100, 2),
                descuento_valor,
                pvd,
                self._observacion(descuento_pct, stock),
                producto.get("permalink", "") or "",
            ])

    def exportar_excel(self, ruta: str):
        wb = xlsxwriter.Workbook(ruta)

        header = wb.add_format({
            "bold": True, "align": "center", "valign": "vcenter",
            "border": 1, "bg_color": "#D9E1F2",
        })
        cell = wb.add_format({"border": 1})
        url_fmt = wb.add_format({"border": 1, "font_color": "blue", "underline": 1})

        widths = [14, 40, 22, 10, 10, 14, 12, 14, 14, 10, 28, 60]

        for nombre, datos in (("Productos Simples", self.simples), ("Productos Variados", self.variados)):
            ws = wb.add_worksheet(nombre[:31])

            for col, h in enumerate(HEADERS_INTERNAL):
                ws.write(0, col, h, header)
                ws.set_column(col, col, widths[col] if col < len(widths) else 18)

            for row_i, fila in enumerate(datos, start=1):
                for col, val in enumerate(fila):
                    if col == COL_URL:
                        link = _safe_str(val)
                        if link:
                            ws.write_url(row_i, col, link, url_fmt, string=link)
                        else:
                            ws.write(row_i, col, "", cell)
                    else:
                        ws.write(row_i, col, val, cell)

            ws.freeze_panes(1, 0)
            ws.autofilter(0, 0, max(1, len(datos)), len(HEADERS_INTERNAL) - 1)

        wb.close()
