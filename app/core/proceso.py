# app/core/proceso.py
from __future__ import annotations

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from app.core.ui.ui_proceso import Ui_ProcessDialog


class ProcessDialog(QDialog):
    """Diálogo de progreso reutilizable para todo el sistema.

    Soporta:
    - Modo indeterminado (barra animada) mientras no hay porcentaje real.
    - Modo determinado cuando recibes valores 0..100.
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

    def set_indeterminado(self, activo: bool = True):
        """Activa/desactiva el modo animado."""
        if activo:
            # 0..0 => modo “busy” animado
            self.ui.progressBar.setRange(0, 0)
            self.ui.progressBar.setTextVisible(False)
        else:
            self.ui.progressBar.setRange(0, 100)
            self.ui.progressBar.setTextVisible(False)

    def set_progreso(self, valor: int):
        # En cuanto llega un % real, pasamos a modo determinado
        if self.ui.progressBar.maximum() == 0:
            self.set_indeterminado(False)
        self.ui.progressBar.setValue(int(valor))

    def set_mensaje(self, texto: str):
        self.ui.lblSubtitulo.setText(texto)
        self.ui.textLog.append(texto)

    def reset(self):
        self.set_indeterminado(True)
        self.ui.textLog.clear()
        self.ui.lblSubtitulo.setText("")
