from PySide6.QtWidgets import QMainWindow, QApplication

from app.menu.ui.ui_view_menu import Ui_MenuPrincipal
from app.menu.menu_base_view import MenuBaseView
from app.core.temas import aplicar_tema_sistema
from app.core.configuracion import Configuracion
from app.core.excepciones import ConfiguracionError
from app.core.credenciales_view import CredencialesApiWooView
from app.core.dialogos import mostrar_error



class MenuPrincipalView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MenuPrincipal()
        self.ui.setupUi(self)

        self._conectar_eventos()

        # ✅ Aplica tema de sistema correctamente
        aplicar_tema_sistema(QApplication.instance())

        self.ventana = None

    def _conectar_eventos(self):
        self.ui.btnVentas.clicked.connect(self._ventas)
        self.ui.btnInventario.clicked.connect(self._inventario)
        self.ui.btnActualizarProductos.clicked.connect(self._actualizar)
        self.ui.btnDistribuidores.clicked.connect(self._distribuidores)

    def _abrir_modulo(self, VentanaClase):
        if not self._asegurar_credenciales():
            return

        if self.ventana:
            try:
                self.ventana.close()
            except Exception:
                pass

        self.ventana = VentanaClase(self)
        self.ventana.show()
        self.hide()

        self.ventana.destroyed.connect(self.show)


    def _mostrar_menu(self):
        self.show()


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
