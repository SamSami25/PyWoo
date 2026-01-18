# app/actualizar_productos/actualizar_productos_view.py
from PySide6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PySide6.QtCore import QDate
from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_MainW_actualizarproductos
from app.actualizar_productos.controlador_actualizar_productos import ActualizarProductosController


class ActualizarProductosView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        self.ui = Ui_MainW_actualizarproductos()
        self.ui.setupUi(self)

        # Controlador
        self.controller = ActualizarProductosController()

        # Inicializar estado
        self._inicializar_ui()
        self._conectar_senales()

    def _inicializar_ui(self):
        self.ui.lb_fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))

    def _conectar_senales(self):
        self.ui.bt_subirArchivo.clicked.connect(self.subir_archivo)
        self.ui.bt_actualizar.clicked.connect(self.actualizar_productos)
        self.ui.bt_exportar.clicked.connect(self.exportar)
        self.ui.bt_volver.clicked.connect(self.close)

    # ===== Métodos de la vista =====

    def subir_archivo(self):
        QMessageBox.information(
            self,
            "Archivo",
            "Funcionalidad de carga de archivo pendiente"
        )

    def actualizar_productos(self):
        productos = self.controller.obtener_productos()
        self._cargar_tabla(productos)
        QMessageBox.information(self, "Actualización", "Productos actualizados")

    def exportar(self):
        self.controller.exportar_productos()
        QMessageBox.information(self, "Exportar", "Datos exportados")

    def _cargar_tabla(self, productos):
        self.ui.tb_productos.clear()
        self.ui.tb_productos.setRowCount(len(productos))

        for fila, p in enumerate(productos):
            self.ui.tb_productos.setItem(
                fila, 0, QTableWidgetItem(str(p["id"]))
            )
            self.ui.tb_productos.setItem(
                fila, 1, QTableWidgetItem(p["name"])
            )
