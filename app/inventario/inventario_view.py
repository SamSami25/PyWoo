from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QDate
from datetime import datetime

from app.inventario.ui.ui_view_inventario import Ui_MainWindow
from app.inventario.controlador_inventario import ControladorInventario
from app.core.excepciones import PyWooError


class InventarioView(QMainWindow):
    """
    Vista del módulo Inventario.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.controlador = ControladorInventario()

        self._configurar_ui()
        self._conectar_senales()

    # --------------------------------------------------
    def _configurar_ui(self):
        self.ui.progressB_barra.setValue(0)
        self.ui.lb_fecha.setText(
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

        # Default
        self.ui.checkB_todos.setChecked(True)

    # --------------------------------------------------
    def _conectar_senales(self):
        self.ui.pbt_exportar.clicked.connect(self.exportar_inventario)
        self.ui.bt_volver.clicked.connect(self.close)

    # --------------------------------------------------
    def _obtener_filtro(self):
        if self.ui.checkB_con.isChecked():
            return "con_stock"
        if self.ui.checkB_sin.isChecked():
            return "sin_stock"
        return "todos"

    # --------------------------------------------------
    def exportar_inventario(self):
        try:
            self.ui.progressB_barra.setValue(20)

            filtro = self._obtener_filtro()
            self.controlador.obtener_productos(filtro)

            self.ui.progressB_barra.setValue(70)

            nombre_archivo = f"inventario_{filtro}.xlsx"
            self.controlador.exportar_excel(nombre_archivo)

            self.ui.progressB_barra.setValue(100)

            QMessageBox.information(
                self,
                "Inventario exportado",
                f"Archivo generado correctamente:\n{nombre_archivo}"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)
