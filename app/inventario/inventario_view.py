from PySide6.QtWidgets import QMainWindow, QTableWidgetItem
from app.inventario.ui.ui_view_inventario import Ui_MainWindow
from app.inventario.controlador_inventario import InventarioController
from PySide6.QtCore import QDate


class InventarioView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Controlador
        self.controller = InventarioController()

        # Inicializar estado
        self._inicializar_ui()
        self._conectar_senales()

    def _inicializar_ui(self):
        self.ui.lb_fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))

    def _conectar_senales(self):
        self.ui.pbt_exportar.clicked.connect(self.exportar)
        self.ui.bt_volver.clicked.connect(self.close)
        self.ui.checkB_todos.clicked.connect(self.cargar_todos)
        self.ui.checkB_con.clicked.connect(self.cargar_con_stock)
        self.ui.checkB_sin.clicked.connect(self.cargar_sin_stock)

    # ====== MÉTODOS DE VISTA ======

    def cargar_todos(self):
        productos = self.controller.obtener_todos()
        self._cargar_tabla(productos)

    def cargar_con_stock(self):
        productos = self.controller.obtener_con_stock()
        self._cargar_tabla(productos)

    def cargar_sin_stock(self):
        productos = self.controller.obtener_sin_stock()
        self._cargar_tabla(productos)

    def _cargar_tabla(self, productos):
        self.ui.tb_productos.clear()
        self.ui.tb_productos.setRowCount(len(productos))

        for fila, producto in enumerate(productos):
            self.ui.tb_productos.setItem(fila, 0, QTableWidgetItem(str(producto["id"])))
            self.ui.tb_productos.setItem(fila, 1, QTableWidgetItem(producto["name"]))
            self.ui.tb_productos.setItem(
                fila, 2,
                QTableWidgetItem(str(producto.get("stock_quantity", 0)))
            )

    def exportar(self):
        self.controller.exportar_inventario()
