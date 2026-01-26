# app/core/credenciales_view.py

from PySide6.QtWidgets import QDialog, QLineEdit
from app.core.ui.ui_view_credenciales_api import Ui_CredencialesApiWoo
from app.core.controlador_credenciales import ControladorCredenciales
from app.core.dialogos import mostrar_error, mostrar_info


class CredencialesApiWooView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_CredencialesApiWoo()
        self.ui.setupUi(self)

        self.controlador = ControladorCredenciales()

        self._cargar_guardadas()

        self.ui.btnCerrar.clicked.connect(self.close)
        self.ui.btnGuardar.clicked.connect(self._guardar)
        self.ui.btnProbarConexion.clicked.connect(self._probar_conexion)
        self.ui.checkVerCredenciales.toggled.connect(self._toggle_ver)

    def _cargar_guardadas(self):
        try:
            cred = self.controlador.cargar_credenciales()
            self.ui.lineEditStoreUrl.setText(cred["url"])
            self.ui.lineEditConsumerKey.setText(cred["consumer_key"])
            self.ui.lineEditConsumerSecret.setText(cred["consumer_secret"])
        except Exception:
            pass  # primera vez, no molestar al usuario

    def _guardar(self):
        try:
            self.controlador.guardar_credenciales(
                self.ui.lineEditStoreUrl.text(),
                self.ui.lineEditConsumerKey.text(),
                self.ui.lineEditConsumerSecret.text(),
            )
            mostrar_info("Credenciales guardadas correctamente.")
        except Exception as e:
            mostrar_error(str(e))

    def _probar_conexion(self):
        try:
            self.controlador.probar_conexion()
            mostrar_info("Conexión exitosa con WooCommerce.")
        except Exception as e:
            mostrar_error(str(e))

    def _toggle_ver(self, visible):
        modo = QLineEdit.Normal if visible else QLineEdit.Password
        self.ui.lineEditConsumerKey.setEchoMode(modo)
        self.ui.lineEditConsumerSecret.setEchoMode(modo)
