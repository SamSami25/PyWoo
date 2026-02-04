# app/core/base_windows.py
from __future__ import annotations

import os

from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtCore import Qt

from app.core.credenciales_view import CredencialesApiWooView
from app.core.dialogos import mostrar_error
from app.core.configuracion import Configuracion
from app.core.excepciones import ConfiguracionError


def aplicar_tema_claro(app: QApplication) -> None:
    """Tema claro fijo para toda la app."""
    if not app:
        return
    try:
        app.setStyle("Fusion")
    except Exception:
        pass


class BaseModuleWindow(QMainWindow):
    def __init__(self, menu_controller, parent=None):
        super().__init__(parent)

        aplicar_tema_claro(QApplication.instance())

        self.menu_controller = menu_controller
        self._build_menu()

    def _build_menu(self):
        menubar = self.menuBar()
        menubar.clear()

        menu_woo = menubar.addMenu("WooCommerce")
        act_cred = QAction("Credenciales API", self)
        act_cred.triggered.connect(self._abrir_credenciales)
        menu_woo.addAction(act_cred)

        menu_mod = menubar.addMenu("Módulos")

        act_ventas = QAction("Reporte Ventas", self)
        act_inventario = QAction("Inventario", self)
        act_actualizar = QAction("Actualizar Productos", self)
        act_distribuidores = QAction("Lista de Distribuidores", self)

        act_ventas.triggered.connect(lambda: self.menu_controller and self.menu_controller._ventas())
        act_inventario.triggered.connect(lambda: self.menu_controller and self.menu_controller._inventario())
        act_actualizar.triggered.connect(lambda: self.menu_controller and self.menu_controller._actualizar())
        act_distribuidores.triggered.connect(lambda: self.menu_controller and self.menu_controller._distribuidores())

        menu_mod.addAction(act_ventas)
        menu_mod.addAction(act_inventario)
        menu_mod.addAction(act_actualizar)
        menu_mod.addAction(act_distribuidores)

        menu_help = menubar.addMenu("Ayuda")
        act_about = QAction("Acerca de", self)
        act_about.triggered.connect(self._acerca_de)
        menu_help.addAction(act_about)

    def _abrir_credenciales(self):
        dlg = CredencialesApiWooView(self)
        dlg.exec()

    def asegurar_credenciales(self) -> bool:
        try:
            Configuracion().obtener_credenciales()
            return True
        except ConfiguracionError:
            dlg = CredencialesApiWooView(self)
            if dlg.exec() == QDialog.Accepted:
                try:
                    Configuracion().obtener_credenciales()
                    return True
                except ConfiguracionError:
                    mostrar_error("Credenciales incompletas o inválidas.", self)
                    return False
            return False

    def _acerca_de(self):
        ruta_imagen = os.path.normpath(
            os.path.join(
                os.path.dirname(__file__),
                "..", "..", "assets", "images", "sello_ups.jpg"
            )
        )

        msg = QMessageBox(self)
        msg.setWindowTitle("Acerca de")
        msg.setTextFormat(Qt.RichText)

        msg.setText("""
            <div style="text-align:center;">
                <h3 style="margin:0; padding:0;">
                    <b>UNIVERSIDAD POLITÉCNICA SALESIANA</b>
                </h3>
                <p style="margin:6px 0 0 0;"><b>Proyecto:</b> PyWoo</p>
                <p style="margin:4px 0;"><b>Autor:</b> Sami Gabriela Aldaz Cabrera</p>
                <p style="margin:4px 0;"><b>Versión:</b> 2</p>
                <p style="margin:10px 0 0 0;">Integración WooCommerce</p>
            </div>
        """)

        if os.path.exists(ruta_imagen):
            pixmap = QPixmap(ruta_imagen)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                msg.setIconPixmap(pixmap)

        msg.setStandardButtons(QMessageBox.Ok)

        btn_ok = msg.button(QMessageBox.Ok)
        if btn_ok:
            btn_ok.setObjectName("btnOk")
            btn_ok.setCursor(Qt.PointingHandCursor)

        msg.setStyleSheet("""
            QPushButton#btnOk {
                background-color: #1E73F1;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 10px;
                font-weight: 700;
                min-width: 90px;
            }
            QPushButton#btnOk:hover {
                background-color: #155CC5;
            }
            QPushButton#btnOk:pressed {
                background-color: #0F4AA6;
            }
            QPushButton#btnOk:focus {
                outline: none;
            }
        """)

        msg.exec()
