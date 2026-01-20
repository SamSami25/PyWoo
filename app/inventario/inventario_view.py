from PySide6.QtWidgets import (QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from datetime import datetime

from app.inventario.ui.ui_view_inventario import Ui_MainWindow
from app.inventario.controlador_inventario import ControladorInventario
from app.core.excepciones import PyWooError


class InventarioView(QMainWindow):
    """
    Vista del módulo Inventario.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

        self.controlador = ControladorInventario()
        self.HEADERS = self.controlador.HEADERS

        self.tabla_simples = None
        self.tabla_variados = None

        self._configurar_ui()
        self._conectar_senales()

    # --------------------------------------------------
    def _configurar_ui(self):
        self.ui.progressB_barra.setValue(0)
        self.ui.lb_fecha.setText(
            datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        self.ui.lb_blancocomentario.setText("")

        # Solo uno activo por defecto
        self.ui.checkB_todos.setChecked(True)
        self.ui.checkB_con.setChecked(False)
        self.ui.checkB_sin.setChecked(False)

        self._configurar_tablas()

    # --------------------------------------------------
    def _conectar_senales(self):
        self.ui.checkB_todos.clicked.connect(
            lambda: self._activar_check("todos")
        )
        self.ui.checkB_con.clicked.connect(
            lambda: self._activar_check("con")
        )
        self.ui.checkB_sin.clicked.connect(
            lambda: self._activar_check("sin")
        )

        self.ui.pbt_exportar.clicked.connect(self.exportar_inventario)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def _activar_check(self, tipo):
        """
        Garantiza que solo un checkbox esté activo.
        """
        self.ui.checkB_todos.setChecked(tipo == "todos")
        self.ui.checkB_con.setChecked(tipo == "con")
        self.ui.checkB_sin.setChecked(tipo == "sin")

        self.cargar_inventario()

    # --------------------------------------------------
    def _obtener_filtro(self):
        if self.ui.checkB_con.isChecked():
            return "con_stock"
        if self.ui.checkB_sin.isChecked():
            return "sin_stock"
        return "todos"

    # --------------------------------------------------
    def _configurar_tablas(self):
        """
        Configura las dos pestañas del QTabWidget con tablas
        """
        self.tabla_simples = QTableWidget()
        self.tabla_variados = QTableWidget()

        for tabla in (self.tabla_simples, self.tabla_variados):
            tabla.setColumnCount(len(self.HEADERS))
            tabla.setHorizontalHeaderLabels(self.HEADERS)
            tabla.setEditTriggers(QTableWidget.NoEditTriggers)
            tabla.horizontalHeader().setStretchLastSection(True)

            font = QFont()
            font.setBold(True)
            for i in range(len(self.HEADERS)):
                tabla.horizontalHeaderItem(i).setFont(font)

        # Limpiar tabs existentes
        while self.ui.tb_productos.count():
            self.ui.tb_productos.removeTab(0)

        # Agregar tabs reales
        self.ui.tb_productos.addTab(
            self.tabla_simples, "Productos Simples"
        )
        self.ui.tb_productos.addTab(
            self.tabla_variados, "Productos Variados"
        )

    # --------------------------------------------------
    def cargar_inventario(self):
        try:
            self.ui.progressB_barra.setValue(10)
            self.ui.lb_blancocomentario.setText("Cargando inventario...")

            productos = self.controlador.obtener_productos(
                self._obtener_filtro()
            )

            self._llenar_tablas(productos)

            self.ui.progressB_barra.setValue(100)
            self.ui.lb_blancocomentario.setText("Se generó con éxito.")

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)

    # --------------------------------------------------
    def _llenar_tablas(self, productos):
        self.tabla_simples.setRowCount(0)
        self.tabla_variados.setRowCount(0)

        for p in productos:
            tabla = (
                self.tabla_simples
                if p.get("type") == "simple"
                else self.tabla_variados
            )

            fila = tabla.rowCount()
            tabla.insertRow(fila)

            categorias = ", ".join(
                c.get("name", "") for c in p.get("categories", [])
            )

            valores = [
                p.get("sku", ""),
                p.get("name", ""),
                categorias,
                str(p.get("stock_quantity", 0)),
                p.get("price", ""),
                p.get("stock_status", "")
            ]

            for col, valor in enumerate(valores):
                item = QTableWidgetItem(valor)
                item.setTextAlignment(Qt.AlignCenter)
                tabla.setItem(fila, col, item)

    # --------------------------------------------------
    def exportar_inventario(self):
        try:
            nombre = f"inventario_{self._obtener_filtro()}.xlsx"
            self.controlador.exportar_excel(nombre)

            QMessageBox.information(
                self,
                "Inventario exportado",
                f"Archivo generado correctamente:\n{nombre}"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
