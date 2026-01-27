from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from app.core.ui.ui_proceso import Ui_ProcessDialog


class ProcessDialog(QDialog):
    """
    Diálogo de progreso reutilizable para todo el sistema.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ProcessDialog()
        self.ui.setupUi(self)

        # 🔒 Modal real (bloquea la ventana padre)
        self.setWindowModality(Qt.ApplicationModal)

        # 🎨 FORZAR VISIBILIDAD DEL HEADER
        self.ui.frameHeader.setMinimumHeight(90)
        self.ui.lblTitulo.setMinimumHeight(32)

        # 🎯 Alineación clara
        self.ui.lblTitulo.setAlignment(Qt.AlignCenter)
        self.ui.lblSubtitulo.setAlignment(Qt.AlignCenter)

        # Estado inicial
        self.reset()

        # Cancelar solo cierra el diálogo (no mata procesos)
        self.ui.btnCancelar.clicked.connect(self.close)

    # ------------------------
    # API pública
    # ------------------------
    def set_titulo(self, texto: str):
        self.ui.lblTitulo.setText(texto)

    def set_progreso(self, valor: int):
        self.ui.progressBar.setValue(valor)

    def set_mensaje(self, texto: str):
        self.ui.lblSubtitulo.setText(texto)
        self.ui.textLog.append(texto)

    def reset(self):
        self.ui.progressBar.setValue(0)
        self.ui.textLog.clear()
        self.ui.lblSubtitulo.setText("")
