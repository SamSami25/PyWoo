# app/inventario/controlador_inventario.py
from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce

HEADERS = ["SKU", "NOMBRE", "CATEGORÍA", "STOCK", "PRECIO", "ESTADO"]

COLUMN_KEYS = ["sku", "nombre", "categoria", "stock", "precio", "estado"]


def _safe_str(x) -> str:
    return "" if x is None else str(x)


def _safe_float(x) -> float:
    try:
        if x is None or x == "":
            return 0.0
        return float(x)
    except Exception:
        return 0.0


def _fmt_precio(x) -> str:
    return f"{_safe_float(x):.2f}"


class ModeloTablaInventario(QAbstractTableModel):
    """
    - PRECIO: 2 decimales
    - STOCK: entero
    - ESTADO:
        - todos: En Stock / Sin Stock
        - sin_stock: Agotado
        - con_stock: Se dispone de X unidades
    """

    def __init__(self, datos: list[dict], filtro: str):
        super().__init__()
        self._datos = datos
        self._filtro = filtro

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(COLUMN_KEYS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        fila = self._datos[index.row()]
        clave = COLUMN_KEYS[index.column()]
        val = fila.get(clave, "")

        if role == Qt.DisplayRole:
            if clave == "precio":
                return _fmt_precio(val)

            if clave == "stock":
                try:
                    return str(int(val))
                except Exception:
                    return "0"

            if clave == "estado":
                try:
                    stock = int(fila.get("stock") or 0)
                except Exception:
                    stock = 0

                if self._filtro == "sin_stock":
                    return "Agotado"
                if self._filtro == "con_stock":
                    return f"Se dispone de {stock} unidades"
                return "En Stock" if stock > 0 else "Sin Stock"

            return _safe_str(val)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return HEADERS[section]
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

    @property
    def simples(self):
        return self._simples

    @property
    def variados(self):
        return self._variados

    # ---------------- GENERAR ----------------
    def generar_inventario(self, filtro: str, callback_progreso=None):
        self._ultimo_filtro = filtro

        productos = self.cliente.obtener_productos()
        total = max(len(productos), 1)

        self._simples.clear()
        self._variados.clear()

        for i, p in enumerate(productos, start=1):
            try:
                stock = int(p.get("stock_quantity") or 0)
            except Exception:
                stock = 0

            # filtros
            if filtro == "sin_stock" and stock > 0:
                continue
            if filtro == "con_stock" and stock <= 0:
                continue

            categorias = ", ".join((c.get("name") or "") for c in (p.get("categories") or []))
            tipo = (p.get("type") or "").strip().lower()

            item = {
                "sku": p.get("sku", "") or "",
                "nombre": p.get("name", "") or "",
                "categoria": categorias,
                "stock": stock,
                "precio": p.get("price", "") or "",
                # guardamos algo, pero el modelo mostrará lo pedido
                "estado": p.get("status", "") or "",
                "tipo": tipo,
            }

            if tipo == "variable":
                self._variados.append(item)
            else:
                self._simples.append(item)

            if callback_progreso:
                callback_progreso(int((i / total) * 100), f"Procesando producto {i} de {total}")

        return (
            ModeloTablaInventario(self._simples, filtro),
            ModeloTablaInventario(self._variados, filtro),
        )

    # ---------------- EXPORTAR ----------------
    def exportar_excel(self, ruta: str, filtro: str | None = None):
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

        def estado_export(stock: int) -> str:
            if filtro == "sin_stock":
                return "Agotado"
            if filtro == "con_stock":
                return f"Se dispone de {stock} unidades"
            return "En Stock" if stock > 0 else "Sin Stock"

        for nombre, datos in (("Productos Simples", self._simples), ("Productos Variados", self._variados)):
            ws = workbook.add_worksheet(nombre[:31])

            # headers
            for col, h in enumerate(HEADERS):
                ws.write(0, col, h, header_fmt)

            # widths
            for col, key in enumerate(COLUMN_KEYS):
                ws.set_column(col, col, col_widths.get(key, 18))

            last_row = 0
            for row, fila in enumerate(datos, start=1):
                last_row = row

                try:
                    stock = int(fila.get("stock") or 0)
                except Exception:
                    stock = 0

                for col, key in enumerate(COLUMN_KEYS):
                    val = fila.get(key, "")

                    if key == "stock":
                        ws.write_number(row, col, stock, int_fmt)
                    elif key == "precio":
                        ws.write_number(row, col, _safe_float(val), money_fmt)
                    elif key == "estado":
                        ws.write(row, col, estado_export(stock), text_fmt)
                    else:
                        ws.write(row, col, _safe_str(val), text_fmt)

            ws.autofilter(0, 0, last_row, len(HEADERS) - 1)
            ws.freeze_panes(1, 0)

        workbook.close()
