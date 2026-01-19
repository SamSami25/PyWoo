from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QDate
from app.menu.ui.ui_view_menu import Ui_MainW_menu
from app.reporte_ventas.reporte_ventas_view import ReporteVentasView
from app.inventario.inventario_view import InventarioView
from app.actualizar_productos.actualizar_productos_view import ActualizarProductosView
from app.lista_distribuidores.lista_distribuidores_view import ListaDistribuidoresView



class MenuPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainW_menu()
        self.ui.setupUi(self)

        self._inicializar_ui()
        self._conectar_senales()

    def _inicializar_ui(self):
        self.ui.lb_fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))

    def _conectar_senales(self):
        self.ui.bt_inventario.clicked.connect(self.abrir_inventario)
        self.ui.bt_actualizarproductos.clicked.connect(self.abrir_actualizar_productos)
        self.ui.bt_reporteventas.clicked.connect(self.abrir_reporte_ventas)
        self.ui.bt_listadistribuidores.clicked.connect(self.abrir_distribuidores)
        self.ui.actionReporte_Ventas.triggered.connect(self.abrir_reporte_ventas)
        self.ui.actionInventario.triggered.connect(self.abrir_inventario)
        self.ui.actionActualizar_Productos.triggered.connect(self.abrir_actualizar_productos)
        self.ui.actionLista_de_Dsitribuidores.triggered.connect(self.abrir_distribuidores)

        

    def abrir_inventario(self):
        self.inventario = InventarioView()
        self.inventario.show()

    def abrir_actualizar_productos(self):
        self.actualizar = ActualizarProductosView()
        self.actualizar.show()

    def abrir_reporte_ventas(self):
        self.reporte = ReporteVentasView()
        self.reporte.show()

    def abrir_distribuidores(self):
        self.distribuidores = ListaDistribuidoresView()
        self.distribuidores.show()



