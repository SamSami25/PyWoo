# app/core/base_windows.py
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog
from PySide6.QtGui import QAction

from app.core.credenciales_view import CredencialesApiWooView
from app.core.dialogos import mostrar_error
from app.core.configuracion import Configuracion
from app.core.excepciones import ConfiguracionError


def aplicar_tema_claro(app: QApplication) -> None:
    """Tema claro fijo para toda la app.

    Nota: Si en el futuro quieres un tema más elaborado, puedes mover esto a app/core/temas.py.
    """
    if not app:
        return
    # Forzamos el estilo “Fusion” para que se vea consistente
    try:
        app.setStyle("Fusion")
    except Exception:
        pass
    # Mantén el estilo del sistema / QSS de los .ui (los .ui ya están en claro)


class BaseModuleWindow(QMainWindow):
    """Ventana base para TODOS los módulos.

    - Tema claro fijo.
    - Menú superior común (WooCommerce / Módulos / Ayuda).
    - Navegación centralizada usando el controller del menú (MenuPrincipalView).
    """

    def __init__(self, menu_controller, parent=None):
        super().__init__(parent)

        # ✅ Tema claro SIEMPRE
        aplicar_tema_claro(QApplication.instance())

        self.menu_controller = menu_controller  # normalmente MenuPrincipalView
        self._build_menu()

    # -----------------------------
    # Menú superior común
    # -----------------------------
    def _build_menu(self):
        menubar = self.menuBar()
        menubar.clear()

        # -------- Menú: WooCommerce --------
        menu_woo = menubar.addMenu("WooCommerce")
        act_cred = QAction("Credenciales API", self)
        act_cred.triggered.connect(self._abrir_credenciales)
        menu_woo.addAction(act_cred)

        # -------- Menú: Módulos --------
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

        # -------- Menú: Ayuda --------
        menu_help = menubar.addMenu("Ayuda")
        act_about = QAction("Acerca de", self)
        act_about.triggered.connect(self._acerca_de)
        menu_help.addAction(act_about)

    # -----------------------------
    # Credenciales
    # -----------------------------
    def _abrir_credenciales(self):
        dlg = CredencialesApiWooView(self)
        dlg.exec()

    def asegurar_credenciales(self) -> bool:
        """Útil si un módulo quiere validar credenciales al iniciar."""
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

    # -----------------------------
    # About
    # -----------------------------
    def _acerca_de(self):
        QMessageBox.information(
            self,
            "Acerca de",
            "UNIVERSIDAD POLITÉCNICA\n"
            "Proyecto: PyWoo\n"
            "Autor: Sami Gabriela Aldaz Cabrera\n"
            "Versión: 2\n"
            "Integración WooCommerce"
        )
