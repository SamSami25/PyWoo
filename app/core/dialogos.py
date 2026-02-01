# app/core/dialogos.py
from __future__ import annotations

from PySide6.QtWidgets import QMessageBox


def _apply_box_style(box: QMessageBox) -> None:
    # Estilo mínimo para que el botón OK siempre sea visible aunque haya QSS global
    box.setStyleSheet(
        "QMessageBox{background:#ffffff;}"
        "QLabel{color:#111; font-size:10pt;}"
        "QPushButton{min-width:90px; padding:6px 14px; border-radius:8px; "
        "background:#1e73f1; color:white; font-weight:bold;}"
        "QPushButton:hover{background:#1558c0;}"
        "QPushButton:pressed{background:#0d47a1;}"
    )


def mostrar_error(mensaje: str, parent=None):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Critical)
    box.setWindowTitle("Error")
    box.setText(mensaje)
    box.setStandardButtons(QMessageBox.Ok)
    box.setDefaultButton(QMessageBox.Ok)
    _apply_box_style(box)
    box.exec()


def mostrar_info(mensaje: str, parent=None):
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Information)
    box.setWindowTitle("Información")
    box.setText(mensaje)
    box.setStandardButtons(QMessageBox.Ok)
    box.setDefaultButton(QMessageBox.Ok)
    _apply_box_style(box)
    box.exec()
