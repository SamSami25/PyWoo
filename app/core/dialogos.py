# app/core/dialogos.py

from PySide6.QtWidgets import QMessageBox


def mostrar_error(mensaje: str):
    QMessageBox.critical(
        None,
        "Error",
        mensaje
    )


def mostrar_info(mensaje: str):
    QMessageBox.information(
        None,
        "Información",
        mensaje
    )
