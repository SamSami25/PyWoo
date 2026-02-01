# app/lista_distribuidores/controlador_lista_distribuidores.py
from __future__ import annotations

from typing import Any, List, Optional, Tuple

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide6.QtGui import QFont
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


class ModeloTablaDistribuidores(QAbstractTableModel):
    """
    Modelo robusto:
    - no revienta si una fila viene corta o con None
    - alinea al centro y pone headers en negrita
    """

    def __init__(self, datos: List[List[Any]]):
        super().__init__()
        self._datos = datos

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._datos)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(HEADERS_INTERNAL)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        if role != Qt.DisplayRole:
            return None

        fila = self._datos[index.row()]
        col = index.column()

        if col >= len(fila):
            return ""

        v = fila[col]
        return "" if v is None else str(v)

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

    # --------- REGLAS DE NEGOCIO ---------
    def _por_descuento(self, ganancia: float) -> float:
        # ganancia: 0..1
        if ganancia <= 0.1:
            return 0.0
        if ganancia <= 0.6:
            return 0.4 * ganancia - 0.04
        return 0.20

    def _observacion(self, descuento_pct: float, stock: int) -> str:
        # descuento_pct viene en 0..1
        if (descuento_pct * 100) >= 10 and stock > 1:
            return "COMPRA MÍNIMA 2 UNIDADES"
        return ""

    # --------- GENERAR LISTA ---------
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
            else:
                # si llega otro tipo, lo ignoramos para lista de distribuidores
                pass

            if callback_progreso:
                callback_progreso(
                    int((i / total) * 100),
                    f"Procesando producto {i} de {total}"
                )

        return (
            ModeloTablaDistribuidores(self.simples),
            ModeloTablaDistribuidores(self.variados),
        )

    # --------- PRODUCTOS SIMPLES ---------
    def _procesar_simple(self, p: dict):
        stock = _to_int(p.get("stock_quantity"))
        if stock <= 0:
            return

        pvp = _to_float(p.get("price"))
        p_compra = _to_float(p.get("purchase_price"))

        # evitar división por 0
        ganancia = round(1 - (p_compra / pvp), 4) if pvp > 0 else 0.0
        descuento_pct = self._por_descuento(ganancia)  # 0..1
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

    # --------- PRODUCTOS VARIADOS ---------
    def _procesar_variaciones(self, producto: dict):
        """
        ERROR típico: Woo NO trae 'variations_data' en /products por defecto.
        Trae 'variations' = [ids]. Para tener datos, hay que pedir /products/{id}/variations.
        """
        producto_id = producto.get("id")
        if not producto_id:
            return

        try:
            variaciones = self.cliente.obtener_variaciones_producto(int(producto_id), per_page=100)
        except Exception:
            # si falla, no rompemos todo
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

    # --------- EXPORTAR ---------
    def exportar_excel(self, ruta: str):
        wb = xlsxwriter.Workbook(ruta)

        header = wb.add_format({"bold": True, "align": "center", "valign": "vcenter", "border": 1})
        cell = wb.add_format({"border": 1})

        for nombre, datos in (
            ("Productos Simples", self.simples),
            ("Productos Variados", self.variados),
        ):
            ws = wb.add_worksheet(nombre)

            for col, h in enumerate(HEADERS_INTERNAL):
                ws.write(0, col, h, header)
                ws.set_column(col, col, 18)

            for row_i, fila in enumerate(datos, start=1):
                for col, val in enumerate(fila):
                    ws.write(row_i, col, val, cell)

            # ✅ evitar problemas si está vacío
            ws.freeze_panes(1, 0)

        wb.close()
