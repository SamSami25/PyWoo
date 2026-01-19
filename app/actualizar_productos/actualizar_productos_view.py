from PySide6.QtWidgets import QMainWindow, QMessageBox, QFileDialog
from PySide6.QtCore import QDateTime
from datetime import datetime

from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_MainW_actualizarproductos
from app.actualizar_productos.controlador_actualizar_productos import ControladorActualizarProductos
from app.core.excepciones import PyWooError


class ActualizarProductosView(QMainWindow):
    """
    Vista del módulo Actualizar Productos.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainW_actualizarproductos()
        self.ui.setupUi(self)

        self.controlador = ControladorActualizarProductos()

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
        self.ui.bt_subirArchivo.clicked.connect(self.subir_archivo)
        self.ui.bt_actualizar.clicked.connect(self.actualizar_productos)
        self.ui.bt_exportar.clicked.connect(self.exportar_plantilla)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def exportar_plantilla(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar plantilla",
            "plantilla_actualizar_productos.xlsx",
            "Excel (*.xlsx)"
        )
        if not ruta:
            return

        try:
            self.controlador.exportar_plantilla(ruta)
            QMessageBox.information(
                self,
                "Plantilla exportada",
                "Plantilla Excel generada correctamente."
            )
        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))

    # --------------------------------------------------
    def subir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Excel (*.xlsx)"
        )
        if not ruta:
            return

        try:
            self.ui.progressB_barra.setValue(30)
            self.controlador.cargar_archivo(ruta)
            self.ui.lb_archivocomentario.setText("Archivo cargado correctamente")
            self.ui.progressB_barra.setValue(60)
        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)

    # --------------------------------------------------
    def actualizar_productos(self):
        try:
            self.ui.progressB_barra.setValue(70)
            self.controlador.actualizar_productos()
            self.ui.progressB_barra.setValue(100)

            QMessageBox.information(
                self,
                "Actualización completada",
                "Productos actualizados correctamente."
            )
        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)
