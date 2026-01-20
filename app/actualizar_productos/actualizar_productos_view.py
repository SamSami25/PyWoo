from PySide6.QtWidgets import (QMainWindow, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QFont
from datetime import datetime
import os

from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_MainW_actualizarproductos
from app.actualizar_productos.controlador_actualizar_productos import ControladorActualizarProductos
from app.core.excepciones import PyWooError


class ActualizarProductosView(QMainWindow):
    """
    Vista del módulo Actualizar Productos
    """

    HEADERS = [
        "SKU",
        "NOMBRE DEL PRODUCTO",
        "STOCK",
        "PRECIO COMPRA",
        "PRECIO VENTA",
        "ESTADO"
    ]

    EDITABLES = {"STOCK", "PRECIO COMPRA", "PRECIO VENTA"}

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainW_actualizarproductos()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

        self.controlador = ControladorActualizarProductos()
        self._productos_cargados = None

        self._configurar_ui()
        self._configurar_tablas()
        self._conectar_senales()

    # --------------------------------------------------
    def _configurar_ui(self):
        self.ui.progressB_barra.setValue(0)
        self.ui.lb_archivocomentario.setText("")
        self.ui.lb_blancocomentario.setText("")
        self.ui.lb_fecha.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    # --------------------------------------------------
    def _configurar_tablas(self):
        self.tabla_simples = QTableWidget()
        self.tabla_variados = QTableWidget()

        font = QFont()
        font.setBold(True)

        for tabla in (self.tabla_simples, self.tabla_variados):
            tabla.setColumnCount(len(self.HEADERS))
            tabla.setHorizontalHeaderLabels(self.HEADERS)
            tabla.horizontalHeader().setStretchLastSection(True)

            for i, header in enumerate(self.HEADERS):
                item = tabla.horizontalHeaderItem(i)
                item.setFont(font)

            tabla.setEditTriggers(QTableWidget.DoubleClicked)

        self.ui.tb_productos.clear()
        self.ui.tb_productos.addTab(self.tabla_simples, "Productos Simples")
        self.ui.tb_productos.addTab(self.tabla_variados, "Productos Variados")

    # --------------------------------------------------
    def _conectar_senales(self):
        self.ui.bt_subirArchivo.clicked.connect(self.subir_archivo)
        self.ui.bt_actualizar.clicked.connect(self.actualizar_productos)
        self.ui.bt_exportar.clicked.connect(self.exportar_excel)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def subir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Excel (*.xlsx);;CSV (*.csv)"
        )

        if not ruta:
            return

        extension = os.path.splitext(ruta)[1].lower()
        if extension not in (".xlsx", ".csv"):
            self.ui.lb_archivocomentario.setText("Vuelva a Cargar el Archivo")
            return

        try:
            self.ui.progressB_barra.setValue(20)
            self._productos_cargados = self.controlador.cargar_archivo(ruta)

            self.tabla_simples.setRowCount(0)
            self.tabla_variados.setRowCount(0)

            self.ui.lb_archivocomentario.setText("Cargado Correctamente")
            self.ui.progressB_barra.setValue(40)

        except PyWooError as e:
            self.ui.lb_archivocomentario.setText(str(e))
            self.ui.progressB_barra.setValue(0)

    # --------------------------------------------------
    def actualizar_productos(self):
        if not self._productos_cargados:
            QMessageBox.warning(self, "Atención", "Debe cargar un archivo primero")
            return

        try:
            self.ui.lb_blancocomentario.setText("Actualizando productos...")
            self.ui.progressB_barra.setValue(50)

            def progreso(actual, total):
                if total > 0:
                    valor = 50 + int((actual / total) * 40)
                    self.ui.progressB_barra.setValue(valor)

            simples, variados = self.controlador.actualizar_productos(progreso)

            self._cargar_tabla(self.tabla_simples, simples)
            self._cargar_tabla(self.tabla_variados, variados)

            self.ui.progressB_barra.setValue(100)
            self.ui.lb_blancocomentario.setText("Actualizando con Éxito")

            QMessageBox.information(
                self,
                "Proceso completado",
                "Productos actualizados correctamente"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)

    # --------------------------------------------------
    def _cargar_tabla(self, tabla, productos):
        tabla.setRowCount(0)

        for p in productos:
            fila = tabla.rowCount()
            tabla.insertRow(fila)

            datos = [
                p.get("sku", ""),
                p.get("name", ""),
                p.get("stock_quantity", ""),
                p.get("precio_compra", ""),
                p.get("price", ""),
                p.get("estado", "Sin Actualizar")
            ]

            for col, valor in enumerate(datos):
                item = QTableWidgetItem(str(valor))

                header = self.HEADERS[col]
                if header not in self.EDITABLES:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)

                tabla.setItem(fila, col, item)

    # --------------------------------------------------
    def exportar_excel(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar resultados",
            "productos_actualizados.xlsx",
            "Excel (*.xlsx)"
        )

        if not ruta:
            return

        try:
            self.controlador.exportar_resultado(ruta)
            QMessageBox.information(
                self,
                "Exportado",
                "Archivo exportado correctamente"
            )
        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
