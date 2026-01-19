from PySide6.QtWidgets import (QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem,)
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QFont
from datetime import datetime

from app.lista_distribuidores.ui.ui_view_lista_distribuidores import Ui_MainWindow
from app.lista_distribuidores.controlador_lista_distribuidores import ControladorListaDistribuidores
from app.core.excepciones import PyWooError


class ListaDistribuidoresView(QMainWindow):
    """
    Vista del módulo Lista de Distribuidores.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.controlador = ControladorListaDistribuidores()

        self._configurar_ui()
        self._configurar_tablas()
        self._conectar_senales()

    # --------------------------------------------------
    def _configurar_ui(self):
        self.ui.progressB_barra.setValue(0)
        self.ui.lb_blancocomentario.setText("")
        self.ui.lb_fecha.setText(
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    # --------------------------------------------------
    def _configurar_tablas(self):
        """
        Configura las dos pestañas del QTabWidget con QTableWidget reales
        """
        self.tabla_simples = QTableWidget()
        self.tabla_variados = QTableWidget()

        headers = self.controlador.HEADERS_TABLA

        font = QFont()
        font.setBold(True)

        for tabla in (self.tabla_simples, self.tabla_variados):
            tabla.setColumnCount(len(headers))
            tabla.setHorizontalHeaderLabels(headers)
            tabla.setEditTriggers(QTableWidget.NoEditTriggers)

            for i in range(len(headers)):
                tabla.horizontalHeaderItem(i).setFont(font)

        # Limpiar tabs generados por Qt Designer
        self.ui.tb_productos.clear()

        self.ui.tb_productos.addTab(self.tabla_simples, "Productos Simples")
        self.ui.tb_productos.addTab(self.tabla_variados, "Productos Variados")

    # --------------------------------------------------
    def _conectar_senales(self):
        self.ui.bt_generar.clicked.connect(self.generar_lista)
        self.ui.bt_exportar.clicked.connect(self.exportar_lista)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def generar_lista(self):
        try:
            self.ui.lb_blancocomentario.setText("Generando lista de distribuidores...")
            self.ui.progressB_barra.setValue(10)

            def progreso(actual, total):
                if total > 0:
                    valor = int((actual / total) * 80)
                    self.ui.progressB_barra.setValue(valor)

            simples, variados = self.controlador.generar_lista(progreso)

            self._cargar_tabla(self.tabla_simples, simples)
            self._cargar_tabla(self.tabla_variados, variados)

            self.ui.progressB_barra.setValue(100)
            self.ui.lb_blancocomentario.setText("Se Generó con Éxito")

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.lb_blancocomentario.setText("Error al generar la lista")
            self.ui.progressB_barra.setValue(0)

    # --------------------------------------------------
    def _cargar_tabla(self, tabla, datos):
        """
        Carga los datos en la tabla correspondiente
        """
        tabla.setRowCount(0)
        headers = self.controlador.HEADERS_TABLA

        for fila in datos:
            row = tabla.rowCount()
            tabla.insertRow(row)

            for col, h in enumerate(headers):
                valor = fila.get(h, "")
                tabla.setItem(row, col, QTableWidgetItem(str(valor)))

    # --------------------------------------------------
    def exportar_lista(self):
        try:
            self.ui.progressB_barra.setValue(90)

            nombre_archivo = "lista_distribuidores.xlsx"
            self.controlador.exportar_excel(nombre_archivo)

            self.ui.progressB_barra.setValue(100)
            QMessageBox.information(
                self,
                "Exportación completada",
                f"Archivo generado correctamente:\n{nombre_archivo}"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.lb_blancocomentario.setText("Error al exportar la lista")
            self.ui.progressB_barra.setValue(0)
