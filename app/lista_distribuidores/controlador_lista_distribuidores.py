from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QFont
import xlsxwriter

from app.core.cliente_woocommerce import ClienteWooCommerce
from app.menu.menu_view import MenuPrincipalView


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


# -------------------------------------------------
# MODELO TABLA
# -------------------------------------------------
class ModeloTablaDistribuidores(QAbstractTableModel):
    def __init__(self, datos):
        super().__init__()
        self._datos = datos

    def rowCount(self, parent=None):
        return len(self._datos)

    def columnCount(self, parent=None):
        return len(HEADERS_INTERNAL)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            return self._datos[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
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


# -------------------------------------------------
# CONTROLADOR
# -------------------------------------------------
class ControladorListaDistribuidores:
    def __init__(self):
        self.cliente = ClienteWooCommerce()
        self.simples = []
        self.variados = []

    # --------- REGLAS DE NEGOCIO ---------
    def _por_descuento(self, ganancia):
        if ganancia <= 0.1:
            return 0.0
        elif ganancia <= 0.6:
            return 0.4 * ganancia - 0.04
        else:
            return 0.20

    def _observacion(self, descuento, stock):
        if descuento >= 10 and stock > 1:
            return "COMPRA MÍNIMA 2 UNIDADES"
        return ""

    # --------- GENERAR LISTA ---------
    def generar_lista(self, callback_progreso=None):
        productos = self.cliente.obtener_productos(per_page=100)
        total = len(productos)

        self.simples.clear()
        self.variados.clear()

        for i, p in enumerate(productos, start=1):
            if p.get("type") == "simple":
                self._procesar_simple(p)
            elif p.get("type") == "variable":
                self._procesar_variaciones(p)

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
    def _procesar_simple(self, p):
        stock = int(p.get("stock_quantity") or 0)
        if stock <= 0:
            return

        pvp = float(p.get("price") or 0)
        p_compra = float(p.get("purchase_price") or 0)

        ganancia = round(1 - (p_compra / pvp), 4) if pvp > 0 else 0
        descuento_pct = self._por_descuento(ganancia)
        descuento_valor = round(descuento_pct * pvp, 2)
        pvd = round(pvp - descuento_valor, 2)

        self.simples.append([
            p.get("sku", ""),
            p.get("name", ""),
            "",
            stock,
            round(pvp, 2),
            p_compra,
            ganancia,
            round(descuento_pct * 100, 2),
            descuento_valor,
            pvd,
            self._observacion(descuento_valor, stock),
            p.get("permalink", ""),
        ])

    # --------- PRODUCTOS VARIADOS ---------
    def _procesar_variaciones(self, producto):
        for v in producto.get("variations_data", []):
            stock = int(v.get("stock_quantity") or 0)
            if stock <= 0:
                continue

            pvp = float(v.get("price") or 0)
            p_compra = float(v.get("purchase_price") or 0)

            ganancia = round(1 - (p_compra / pvp), 4) if pvp > 0 else 0
            descuento_pct = self._por_descuento(ganancia)
            descuento_valor = round(descuento_pct * pvp, 2)
            pvd = round(pvp - descuento_valor, 2)

            variacion = " | ".join(
                f"{a.get('name')}: {a.get('option')}"
                for a in v.get("attributes", [])
            ) or "Variación"

            self.variados.append([
                v.get("sku", ""),
                producto.get("name", ""),
                variacion,
                stock,
                round(pvp, 2),
                p_compra,
                ganancia,
                round(descuento_pct * 100, 2),
                descuento_valor,
                pvd,
                self._observacion(descuento_valor, stock),
                producto.get("permalink", ""),
            ])

    # --------- EXPORTAR ---------
    def exportar_excel(self, ruta):
        wb = xlsxwriter.Workbook(ruta)

        header = wb.add_format({"bold": True, "align": "center", "border": 1})
        cell = wb.add_format({"border": 1})

        for nombre, datos in (
            ("Productos Simples", self.simples),
            ("Productos Variados", self.variados),
        ):
            ws = wb.add_worksheet(nombre)

            for col, h in enumerate(HEADERS_INTERNAL):
                ws.write(0, col, h, header)
                ws.set_column(col, col, 18)

            for row, fila in enumerate(datos, start=1):
                for col, val in enumerate(fila):
                    ws.write(row, col, val, cell)

            ws.freeze_panes(1, 0)

        wb.close()
