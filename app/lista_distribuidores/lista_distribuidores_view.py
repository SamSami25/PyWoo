from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QDate
from app.lista_distribuidores.ui.ui_view_lista_distribuidores import Ui_MainWindow
from app.lista_distribuidores.controlador_lista_distribuidores import DistribuidoresController


class DistribuidoresView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Controlador
        self.controller = DistribuidoresController()

        # Inicializar estado
        self._inicializar_ui()
        self._conectar_senales()

    def _inicializar_ui(self):
        self.ui.lb_fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))

    def _conectar_senales(self):
        self.ui.bt_generar.clicked.connect(self.generar_lista)
        self.ui.bt_exportar.clicked.connect(self.exportar)
        self.ui.bt_volver.clicked.connect(self.close)

    # ===== Métodos de vista =====

    def generar_lista(self):
        distribuidores = self.controller.obtener_distribuidores()
        self._cargar_tabla(distribuidores)

    def exportar(self):
        self.controller.exportar_distribuidores()
        QMessageBox.information(self, "Exportar", "Lista exportada")

    def _cargar_tabla(self, distribuidores):
        self.ui.tb_productos.clear()
        self.ui.tb_productos.setRowCount(len(distribuidores))

        for fila, d in enumerate(distribuidores):
            self.ui.tb_productos.setItem(
                fila, 0, QTableWidgetItem(str(d.get("id", "")))
            )
            self.ui.tb_productos.setItem(
                fila, 1, QTableWidgetItem(d.get("first_name", ""))
            )
            self.ui.tb_productos.setItem(
                fila, 2, QTableWidgetItem(d.get("email", ""))
            )
