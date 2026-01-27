from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce

HEADERS = [
    "SKU",
    "NOMBRE",
    "CATEGORÍA",
    "STOCK",
    "PRECIO",
    "ESTADO",
]

# Claves REALES del diccionario (MISMO ORDEN)
COLUMN_KEYS = [
    "sku",
    "nombre",
    "categoria",
    "stock",
    "precio",
    "estado",
]


# =====================================================
# MODELO DE TABLA (DICT-SAFE)
# =====================================================
class ModeloTablaInventario(QAbstractTableModel):
    def __init__(self, datos: list[dict]):
        super().__init__()
        self._datos = datos

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(COLUMN_KEYS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        fila = self._datos[index.row()]
        clave = COLUMN_KEYS[index.column()]

        if role == Qt.DisplayRole:
            return str(fila.get(clave, ""))

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


# =====================================================
# CONTROLADOR
# =====================================================
class ControladorInventario:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self._simples = []
        self._variados = []

    @property
    def simples(self):
        return self._simples

    @property
    def variados(self):
        return self._variados

    # ---------------- GENERAR ----------------
    def generar_inventario(self, filtro, callback_progreso=None):
        productos = self.cliente.obtener_productos()
        total = len(productos)

        self._simples.clear()
        self._variados.clear()

        for i, p in enumerate(productos, start=1):
            stock = int(p.get("stock_quantity") or 0)

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
            ("Productos Simples", self._simples),
            ("Productos Variados", self._variados),
        ):
            ws = workbook.add_worksheet(nombre)

            for col, h in enumerate(HEADERS):
                ws.write(0, col, h, header_fmt)

            for row, fila in enumerate(datos, start=1):
                for col, key in enumerate(COLUMN_KEYS):
                    ws.write(row, col, fila.get(key, ""), cell_fmt)

            ws.autofilter(0, 0, row, len(HEADERS) - 1)
            ws.freeze_panes(1, 0)

        workbook.close()
