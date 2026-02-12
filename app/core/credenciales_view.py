from __future__ import annotations

from PySide6.QtWidgets import QDialog, QLineEdit

from app.core.configuracion import Configuracion
from app.core.dialogos import mostrar_error, mostrar_info
from app.core.controlador_credenciales import ControladorCredenciales

from app.core.ui.ui_view_credenciales_api import Ui_CredencialesApiWoo


class CredencialesApiWooView(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_CredencialesApiWoo()
        self.ui.setupUi(self)

        # El indicador "Credenciales cargadas" solo debe mostrarse cuando están
        # presentes y funcionan (conexión OK).
        try:
            self.ui.checkCredencialesCargadas.setChecked(False)
            self.ui.checkCredencialesCargadas.setVisible(False)
        except Exception:
            pass

        self.controlador = ControladorCredenciales()

        self._cargar_guardadas()

        self.ui.btnCerrar.clicked.connect(self.reject)
        self.ui.btnGuardar.clicked.connect(self._guardar)
        self.ui.btnProbarConexion.clicked.connect(self._probar_conexion)
        self.ui.checkVerCredenciales.toggled.connect(self._toggle_ver)

    # -------------------------------------------------
    # CARGAR CREDENCIALES GUARDADAS
    # -------------------------------------------------
    def _cargar_guardadas(self):
        try:
            cred = Configuracion().obtener_credenciales() or {}

            self.ui.lineEditStoreUrl.setText(cred.get("url", ""))
            self.ui.lineEditConsumerKey.setText(cred.get("consumer_key", ""))
            self.ui.lineEditConsumerSecret.setText(cred.get("consumer_secret", ""))

            # Solo mostrar el visto si las credenciales existen y la conexión funciona.
            url = (cred.get("url") or "").strip()
            ck = (cred.get("consumer_key") or "").strip()
            cs = (cred.get("consumer_secret") or "").strip()

            if url and ck and cs:
                try:
                    ok = bool(self.controlador.probar_conexion(url, ck, cs))
                except Exception:
                    ok = False

                self.ui.checkCredencialesCargadas.setVisible(ok)
                self.ui.checkCredencialesCargadas.setChecked(ok)
            else:
                self.ui.checkCredencialesCargadas.setVisible(False)
                self.ui.checkCredencialesCargadas.setChecked(False)
        except Exception:
            try:
                self.ui.checkCredencialesCargadas.setVisible(False)
                self.ui.checkCredencialesCargadas.setChecked(False)
            except Exception:
                pass

    # -------------------------------------------------
    # GUARDAR CREDENCIALES
    # -------------------------------------------------
    def _guardar(self):
        url = self.ui.lineEditStoreUrl.text().strip()
        ck = self.ui.lineEditConsumerKey.text().strip()
        cs = self.ui.lineEditConsumerSecret.text().strip()

        if not url or not ck or not cs:
            mostrar_error("Debe completar todas las credenciales.", self)
            return

        try:
            self.controlador.guardar_credenciales(url, ck, cs)
            # Verifica conexión para mostrar el visto
            ok = False
            try:
                ok = bool(self.controlador.probar_conexion(url, ck, cs))
            except Exception:
                ok = False
            try:
                self.ui.checkCredencialesCargadas.setVisible(ok)
                self.ui.checkCredencialesCargadas.setChecked(ok)
            except Exception:
                pass
            mostrar_info("Credenciales guardadas correctamente.", self)
            self.accept()
        except Exception as e:
            mostrar_error(str(e), self)

    # -------------------------------------------------
    # PROBAR CONEXIÓN (SIN GUARDAR)
    # -------------------------------------------------
    def _probar_conexion(self):
        url = self.ui.lineEditStoreUrl.text().strip()
        ck = self.ui.lineEditConsumerKey.text().strip()
        cs = self.ui.lineEditConsumerSecret.text().strip()

        if not url or not ck or not cs:
            mostrar_error("Debe completar URL, Consumer Key y Consumer Secret.", self)
            return

        try:
            self.controlador.probar_conexion(url, ck, cs)
            try:
                self.ui.checkCredencialesCargadas.setVisible(True)
                self.ui.checkCredencialesCargadas.setChecked(True)
            except Exception:
                pass
            mostrar_info("Conexión exitosa con WooCommerce.", self)
        except Exception as e:
            # Si falla la conexión, no muestres el visto
            try:
                self.ui.checkCredencialesCargadas.setVisible(False)
                self.ui.checkCredencialesCargadas.setChecked(False)
            except Exception:
                pass
            mostrar_error(str(e), self)

    # -------------------------------------------------
    # MOSTRAR / OCULTAR CREDENCIALES
    # -------------------------------------------------
    def _toggle_ver(self, visible: bool):
        modo = QLineEdit.Normal if visible else QLineEdit.Password
        self.ui.lineEditConsumerKey.setEchoMode(modo)
        self.ui.lineEditConsumerSecret.setEchoMode(modo)
