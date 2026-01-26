from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from app.core.ui.ui_proceso import Ui_ProcessDialog


class ProcessDialog(QDialog):
    """
    Diálogo de progreso reutilizable para todo el sistema.
    NO depende de ningún módulo de negocio.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ProcessDialog()
        self.ui.setupUi(self)

        self.setWindowModality(Qt.ApplicationModal)

        self.ui.progressBar.setValue(0)
        self.ui.btnCancelar.clicked.connect(self.close)

    # ------------------------
    # API pública
    # ------------------------
    def set_progreso(self, valor: int):
        self.ui.progressBar.setValue(valor)

    def set_mensaje(self, texto: str):
        self.ui.lblSubtitulo.setText(texto)
        self.ui.textLog.append(texto)

    def reset(self):
        self.ui.progressBar.setValue(0)
        self.ui.textLog.clear()
