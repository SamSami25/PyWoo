from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QDateTime
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
        self._conectar_senales()

    # --------------------------------------------------
    def _configurar_ui(self):
        self.ui.progressB_barra.setValue(0)
        self.ui.lb_fecha.setText(
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    # --------------------------------------------------
    def _conectar_senales(self):
        self.ui.bt_generar.clicked.connect(self.generar_lista)
        self.ui.bt_exportar.clicked.connect(self.exportar_lista)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def generar_lista(self):
        try:
            self.ui.progressB_barra.setValue(30)
            self.controlador.generar_lista()
            self.ui.progressB_barra.setValue(80)

            QMessageBox.information(
                self,
                "Lista generada",
                "Lista de distribuidores generada correctamente."
            )
        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)

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
            self.ui.progressB_barra.setValue(0)
