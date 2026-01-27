from PySide6.QtWidgets import QDialog, QLineEdit

from app.core.configuracion import Configuracion
from app.core.cliente_woocommerce import ClienteWooCommerce
from app.core.dialogos import mostrar_error, mostrar_info
from app.core.controlador_credenciales import ControladorCredenciales

from app.core.ui.ui_view_credenciales_api import Ui_CredencialesApiWoo


class CredencialesApiWooView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_CredencialesApiWoo()
        self.ui.setupUi(self)

        # ✅ CREAR CONTROLADOR (ESTO FALTABA)
        self.controlador = ControladorCredenciales()

        self._cargar_guardadas()

        self.ui.btnCerrar.clicked.connect(self.close)
        self.ui.btnGuardar.clicked.connect(self._guardar)
        self.ui.btnProbarConexion.clicked.connect(self._probar_conexion)
        self.ui.checkVerCredenciales.toggled.connect(self._toggle_ver)


    # -------------------------------------------------
    # CARGAR CREDENCIALES GUARDADAS
    # -------------------------------------------------
    def _cargar_guardadas(self):
        try:
            config = Configuracion()
            cred = config.obtener_credenciales()

            self.ui.lineEditStoreUrl.setText(cred["url"])
            self.ui.lineEditConsumerKey.setText(cred["consumer_key"])
            self.ui.lineEditConsumerSecret.setText(cred["consumer_secret"])

            self.ui.checkCredencialesCargadas.setChecked(True)

        except Exception:
            # Primera vez: no mostrar error
            self.ui.checkCredencialesCargadas.setChecked(False)

    # -------------------------------------------------
    # GUARDAR CREDENCIALES
    # -------------------------------------------------
    def _guardar(self):
        url = self.ui.lineEditStoreUrl.text().strip()
        key = self.ui.lineEditConsumerKey.text().strip()
        secret = self.ui.lineEditConsumerSecret.text().strip()

        if not url or not key or not secret:
            mostrar_error("Debe completar todas las credenciales.")
            return

        try:
            config = Configuracion()
            config.guardar_credenciales(url, key, secret)
            mostrar_info("Credenciales guardadas correctamente.")
            self.accept()

        except Exception as e:
            mostrar_error(str(e))

    # -------------------------------------------------
    # PROBAR CONEXIÓN (SIN USAR ARCHIVO)
    # -------------------------------------------------
    def _probar_conexion(self):
        try:
            self.controlador.guardar_credenciales(
                self.ui.lineEditStoreUrl.text().strip(),
                self.ui.lineEditConsumerKey.text().strip(),
                self.ui.lineEditConsumerSecret.text().strip(),
            )

            cliente = ClienteWooCommerce()
            cliente.probar_conexion()

            mostrar_info("Conexión exitosa con WooCommerce.")

        except Exception as e:
            mostrar_error(str(e))


    # -------------------------------------------------
    # MOSTRAR / OCULTAR CREDENCIALES
    # -------------------------------------------------
    def _toggle_ver(self, visible):
        modo = QLineEdit.Normal if visible else QLineEdit.Password
        self.ui.lineEditConsumerKey.setEchoMode(modo)
        self.ui.lineEditConsumerSecret.setEchoMode(modo)
