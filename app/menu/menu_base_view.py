from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from app.menu.ui.ui_view_menu import Ui_MenuPrincipal
from app.core.credenciales_view import CredencialesApiWooView
from app.core.temas import (aplicar_tema_claro, aplicar_tema_oscuro, aplicar_tema_sistema)

class MenuBaseView(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui_menu = Ui_MenuPrincipal()
        self.ui_menu.setupUi(self)

        self._conectar_menu()

    def _conectar_menu(self):
        # WooCommerce
        self.ui_menu.actionCredenciales_API.triggered.connect(self._abrir_credenciales)

        # Módulos (IMPORTACIÓN DIFERIDA)
        self.ui_menu.actionReporte_Ventas.triggered.connect(self._abrir_reporte_ventas)
        self.ui_menu.actionInventario.triggered.connect(self._abrir_inventario)
        self.ui_menu.actionActualizar_Productos.triggered.connect(self._abrir_actualizar_productos)
        self.ui_menu.actionLista_de_Distribuidores.triggered.connect(self._abrir_distribuidores)

        # Temas
        self.ui_menu.actionSistema.triggered.connect(self._tema_sistema)
        self.ui_menu.actionClaro.triggered.connect(self._tema_claro)
        self.ui_menu.actionOscuro.triggered.connect(self._tema_oscuro)

        # Ayuda
        self.ui_menu.actionAcerca_de.triggered.connect(self._acerca_de)

    # ---------- ABRIR MÓDULOS ----------
    def _abrir_reporte_ventas(self):
        from app.reporte_ventas.reporte_ventas_view import ReporteVentasView
        self.ventana = ReporteVentasView(self)
        self.ventana.show()

    def _abrir_inventario(self):
        from app.inventario.inventario_view import InventarioView
        self.ventana = InventarioView(self)
        self.ventana.show()

    def _abrir_actualizar_productos(self):
        from app.actualizar_productos.actualizar_productos_view import ActualizarProductosView
        self.ventana = ActualizarProductosView(self)
        self.ventana.show()

    def _abrir_distribuidores(self):
        from app.lista_distribuidores.lista_distribuidores_view import ListaDistribuidoresView
        self.ventana = ListaDistribuidoresView(self)
        self.ventana.show()

    # ---------- OTROS ----------
    def _abrir_credenciales(self):
        dlg = CredencialesApiWooView(self)
        dlg.exec()

    def _tema_sistema(self):
        aplicar_tema_sistema(QApplication.instance())

    def _tema_claro(self):
        aplicar_tema_claro(QApplication.instance())

    def _tema_oscuro(self):
        aplicar_tema_oscuro(QApplication.instance())

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
