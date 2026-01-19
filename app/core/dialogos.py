from PySide6.QtWidgets import QDialog, QMessageBox
from app.core.ui.ui_view_credenciales_api import Ui_Dialog_urlWoocommerce
from app.core.controlador_credenciales import CredencialesController
from app.core.excepciones import PyWooError
from PySide6.QtWidgets import QMessageBox

# ==========================================================
# FUNCIONES AUXILIARES (DEBEN ESTAR A NIVEL DE MÓDULO)
# ==========================================================

def mostrar_info(parent, titulo, mensaje):
    QMessageBox.information(parent, titulo, mensaje)


def mostrar_error(parent, titulo, mensaje):
    QMessageBox.critical(parent, titulo, mensaje)


# ==========================================================
# DIÁLOGO DE CREDENCIALES
# ==========================================================

class DialogoCredencialesWoo(QDialog):
    """
    Diálogo de configuración de credenciales WooCommerce.
    Maneja exclusivamente interacción con la UI.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Dialog_urlWoocommerce()
        self.ui.setupUi(self)

        self.controlador = CredencialesController()

        self._cargar_credenciales()
        self._conectar_senales()

    # ------------------------------------------------------
    def _conectar_senales(self):
        self.ui.pbt_guardar.clicked.connect(self._guardar_credenciales)
        self.ui.pbt_conexion.clicked.connect(self._probar_conexion)
        self.ui.pbt_salir.clicked.connect(self.close)

    # ------------------------------------------------------
    def _cargar_credenciales(self):
        try:
            url, ck, cs = self.controlador.cargar_credenciales()
            self.ui.lnEdit_url.setText(url)
            self.ui.lnEdit_ck.setText(ck)
            self.ui.lnEdit_cs.setText(cs)
        except PyWooError:
            pass  # Primera ejecución

    # ------------------------------------------------------
    def _guardar_credenciales(self):
        try:
            self.controlador.guardar_credenciales(
                url=self.ui.lnEdit_url.text().strip(),
                consumer_key=self.ui.lnEdit_ck.text().strip(),
                consumer_secret=self.ui.lnEdit_cs.text().strip()
            )
            mostrar_info(
                self,
                "Credenciales guardadas",
                "Las credenciales se guardaron correctamente."
            )
        except PyWooError as e:
            mostrar_error(self, "Error", str(e))


    # ------------------------------------------------------
    def _probar_conexion(self):
        try:
            self.controlador.probar_conexion(
                url=self.ui.lnEdit_url.text().strip(),
                consumer_key=self.ui.lnEdit_ck.text().strip(),
                consumer_secret=self.ui.lnEdit_cs.text().strip()
            )
            mostrar_info(
                self,
                "Conexión exitosa",
                "Conexión con WooCommerce realizada correctamente."
            )
        except PyWooError as e:
            mostrar_error(self, "Error de conexión", str(e))

