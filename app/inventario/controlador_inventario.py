from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce
from app.menu.menu_view import MenuPrincipalView


HEADERS = [
    "SKU",
    "NOMBRE",
    "CATEGORÍA",
    "STOCK",
    "PRECIO",
    "ESTADO",
]


class ModeloTablaInventario(QAbstractTableModel):
    def __init__(self, datos):
        super().__init__()
        self._datos = datos

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(HEADERS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            return self._datos[index.row()][index.column()]

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
        self._simples = []
        self._variados = []

    def generar_inventario(self, filtro, callback_progreso=None):
        productos = self.cliente.obtener_productos()
        total = len(productos)

        self._simples.clear()
        self._variados.clear()

        for i, p in enumerate(productos, start=1):
            stock = int(p.get("stock_quantity") or 0)

            # -------- FILTRO CORRECTO --------
            if filtro == "sin_stock" and stock > 0:
                continue
            if filtro == "con_stock" and stock <= 0:
                continue

            item = {
                "sku": p.get("sku", ""),
                "nombre": p.get("name", ""),
                "categoria": ", ".join(c["name"] for c in p.get("categories", [])),
                "stock": stock,
                "precio": p.get("price", ""),
                "estado": p.get("status", ""),
                "tipo": p.get("type"),
            }

            if item["tipo"] == "simple":
                self._simples.append(item)
            elif item["tipo"] == "variable":
                self._variados.append(item)

            if callback_progreso:
                callback_progreso(
                    int((i / total) * 100),
                    f"Procesando producto {i} de {total}"
                )

        return (
            ModeloTablaInventario(self._simples),
            ModeloTablaInventario(self._variados),
        )

    # ---------------- EXPORTAR ----------------
    def exportar_excel(self, ruta):
        workbook = xlsxwriter.Workbook(ruta)

        header_fmt = workbook.add_format({
            "bold": True,
            "align": "center",
            "border": 1
        })
        cell_fmt = workbook.add_format({"border": 1})

        for nombre, datos in (
            ("Productos Simples", self.simples),
            ("Productos Variados", self.variados),
        ):
            ws = workbook.add_worksheet(nombre)

            for col, h in enumerate(HEADERS):
                ws.write(0, col, h, header_fmt)

            for row, fila in enumerate(datos, start=1):
                for col, val in enumerate(fila):
                    ws.write(row, col, val, cell_fmt)

            ws.autofilter(0, 0, row, len(HEADERS) - 1)
            ws.freeze_panes(1, 0)

        workbook.close()
