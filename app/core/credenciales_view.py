# app/core/credenciales_view.py
from PySide6.QtWidgets import QDialog, QMessageBox
from app.core.ui.ui_view_credenciales_api import Ui_Dialog_urlWoocommerce
from app.core.controlador_credenciales import CredencialesController

class VentanaCredenciales(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_urlWoocommerce()
        self.ui.setupUi(self)

        self.controlador = CredencialesController()
        self._connect_signals()

    def _connect_signals(self):
        self.ui.pbt_salir.clicked.connect(self.reject)
        self.ui.pbt_guardar.clicked.connect(self.guardar)

    def guardar(self):
        try:
            self.controlador.guardar(
                self.ui.input_url.text().strip(),
                self.ui.input_consumer_key.text().strip(),
                self.ui.input_consumer_secret.text().strip()
            )
            QMessageBox.information(self, "Éxito", "Credenciales guardadas")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
