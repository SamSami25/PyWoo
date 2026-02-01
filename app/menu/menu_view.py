# app/menu/menu_view.py
from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QMessageBox, QDialog
from PySide6.QtCore import QEvent

from app.menu.ui.ui_view_menu import Ui_MenuPrincipal
from app.core.configuracion import Configuracion
from app.core.excepciones import ConfiguracionError
from app.core.credenciales_view import CredencialesApiWooView
from app.core.dialogos import mostrar_error


class MenuPrincipalView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MenuPrincipal()
        self.ui.setupUi(self)

        self.ventana = None
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.ui.btnVentas.clicked.connect(self._ventas)
        self.ui.btnInventario.clicked.connect(self._inventario)
        self.ui.btnActualizarProductos.clicked.connect(self._actualizar)
        self.ui.btnDistribuidores.clicked.connect(self._distribuidores)

        self.ui.actionCredenciales_API.triggered.connect(self._abrir_credenciales)
        self.ui.actionReporte_Ventas.triggered.connect(self._ventas)
        self.ui.actionInventario.triggered.connect(self._inventario)
        self.ui.actionActualizar_Productos.triggered.connect(self._actualizar)
        self.ui.actionLista_de_Distribuidores.triggered.connect(self._distribuidores)
        self.ui.actionAcerca_de.triggered.connect(self._acerca_de)

    def _abrir_credenciales(self):
        dlg = CredencialesApiWooView(self)
        dlg.exec()

    def _asegurar_credenciales(self) -> bool:
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
                    mostrar_error("Credenciales incompletas o inválidas.")
                    return False
            return False

    def _abrir_modulo(self, VentanaClase):
        if not self._asegurar_credenciales():
            return

        if self.ventana:
            self.ventana.close()

        self.ventana = VentanaClase(self)
        self.ventana.show()
        self.ventana.raise_()
        self.ventana.activateWindow()
        # ✅ Mantener el menú principal detrás (no lo escondemos)
        # self.hide()
        self.ventana.destroyed.connect(self.show)

    def _ventas(self):
        from app.reporte_ventas.reporte_ventas_view import ReporteVentasView
        self._abrir_modulo(ReporteVentasView)

    def _inventario(self):
        from app.inventario.inventario_view import InventarioView
        self._abrir_modulo(InventarioView)

    def _actualizar(self):
        from app.actualizar_productos.actualizar_productos_view import ActualizarProductosView
        self._abrir_modulo(ActualizarProductosView)

    def _distribuidores(self):
        from app.lista_distribuidores.lista_distribuidores_view import ListaDistribuidoresView
        self._abrir_modulo(ListaDistribuidoresView)

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
