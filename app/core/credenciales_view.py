from PySide6.QtWidgets import QDialog
from app.core.controlador_credenciales import CredencialesController
from app.core.dialogos import mostrar_info, mostrar_error
from app.core.ui.ui_view_credenciales_api import Ui_Dialog_urlWoocommerce

class VentanaCredenciales(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog_urlWoocommerce()
        self.ui.setupUi(self)

        self.controlador = CredencialesController()
        self._connect_signals()

    # --------------------------------------------------
    def _connect_signals(self):
        self.ui.pbt_salir.clicked.connect(self.reject)
        self.ui.pbt_guardar.clicked.connect(self.guardar_credenciales)
        self.ui.pbt_conexion.clicked.connect(self.probar_conexion)

    # --------------------------------------------------
    def guardar_credenciales(self):
        try:
            self.controlador.guardar_credenciales(
                self.ui.lnEdit_url.text().strip(),
                self.ui.lnEdit_ck.text().strip(),
                self.ui.lnEdit_cs.text().strip()
            )
            mostrar_info(self, "Éxito", "Credenciales guardadas correctamente")
            self.accept()
        except Exception as e:
            mostrar_error(self, "Error", str(e))

    # --------------------------------------------------
    def guardar(self):
        try:
            self.controlador.guardar_credenciales(
                self.ui.lnEdit_url.text().strip(),
                self.ui.lnEdit_ck.text().strip(),
                self.ui.lnEdit_cs.text().strip()
            )
            mostrar_info(self, "Éxito", "Credenciales guardadas correctamente")
            self.accept()  # ← IMPORTANTE
        except Exception as e:
            mostrar_error(self, "Error", str(e))

    def probar_conexion(self):
        try:
            self.controlador.probar_conexion(
                self.ui.lnEdit_url.text().strip(),
                self.ui.lnEdit_ck.text().strip(),
                self.ui.lnEdit_cs.text().strip()
            )
            mostrar_info(self, "Conexión exitosa", "Conexión con WooCommerce establecida")
        except Exception as e:
            mostrar_error(self, "Error de conexión", str(e))