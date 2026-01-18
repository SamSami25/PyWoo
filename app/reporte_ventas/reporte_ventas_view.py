# app/ventas/ventas_view.py
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QDate
from app.reporte_ventas.ui.ui_view_reporte_ventas import Ui_MainW_reporteVentas
from app.reporte_ventas.controlador_reporte_ventas import VentasController


class VentasView(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar UI
        self.ui = Ui_MainW_reporteVentas()
        self.ui.setupUi(self)

        # Controlador
        self.controller = VentasController()

        # Inicializar estado
        self._inicializar_ui()
        self._conectar_senales()

    def _inicializar_ui(self):
        self.ui.lb_fecha.setText(QDate.currentDate().toString("dd/MM/yyyy"))
        self.ui.dateE_desde.setDate(QDate.currentDate())
        self.ui.dateE_Hasta.setDate(QDate.currentDate())

    def _conectar_senales(self):
        self.ui.pbt_salir.clicked.connect(self.exportar)
        self.ui.bt_volver.clicked.connect(self.close)

    def exportar(self):
        fecha_desde = self.ui.dateE_desde.date().toString("yyyy-MM-dd")
        fecha_hasta = self.ui.dateE_Hasta.date().toString("yyyy-MM-dd")

        try:
            ventas = self.controller.obtener_ventas(fecha_desde, fecha_hasta)
            QMessageBox.information(
                self,
                "Reporte",
                f"Se encontraron {len(ventas)} ventas"
            )
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
