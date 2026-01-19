from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtCore import QDate
from datetime import datetime

from app.reporte_ventas.ui.ui_view_reporte_ventas import Ui_MainW_reporteVentas
from app.reporte_ventas.controlador_reporte_ventas import ControladorReporteVentas
from app.core.excepciones import PyWooError


class ReporteVentasView(QMainWindow):
    """
    Vista del módulo Reporte de Ventas.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainW_reporteVentas()
        self.ui.setupUi(self)

        self.controlador = ControladorReporteVentas()

        self._configurar_ui()
        self._conectar_senales()

    # ---------------------------------------------------------
    def _configurar_ui(self):
        hoy = QDate.currentDate()
        self.ui.dateE_desde.setDate(hoy.addDays(-7))
        self.ui.dateE_Hasta.setDate(hoy)

        self.ui.progressB_barra.setValue(0)
        self.ui.lb_fecha.setText(
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )

    # ---------------------------------------------------------
    def _conectar_senales(self):
        self.ui.pbt_salir.clicked.connect(self.exportar_reporte)
        self.ui.bt_volver.clicked.connect(self.close)

    # ---------------------------------------------------------
    def exportar_reporte(self):
        try:
            self.ui.progressB_barra.setValue(20)

            fecha_desde = self.ui.dateE_desde.date().toString("yyyy-MM-dd")
            fecha_hasta = self.ui.dateE_Hasta.date().toString("yyyy-MM-dd")

            self.controlador.obtener_ventas(fecha_desde, fecha_hasta)

            self.ui.progressB_barra.setValue(70)

            nombre_archivo = f"reporte_ventas_{fecha_desde}_{fecha_hasta}.xlsx"
            self.controlador.exportar_excel(nombre_archivo)

            self.ui.progressB_barra.setValue(100)

            QMessageBox.information(
                self,
                "Reporte generado",
                f"Reporte exportado correctamente:\n{nombre_archivo}"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)
