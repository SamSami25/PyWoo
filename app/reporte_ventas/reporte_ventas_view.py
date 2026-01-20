from PySide6.QtWidgets import (QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont
from datetime import datetime

from app.reporte_ventas.ui.ui_view_reporte_ventas import Ui_MainW_reporteVentas
from app.reporte_ventas.controlador_reporte_ventas import ControladorReporteVentas
from app.core.excepciones import PyWooError


class ReporteVentasView(QMainWindow):
    """
    Vista del módulo Reporte de Ventas.
    """

    HEADERS = [
        "FECHA", "CLIENTE", "SUBTOTAL", "ENVÍO", "IVA", "DESCUENTO", "TOTAL",
        "MÉTODO DE PAGO", "UTILIDAD", "ESTADO", "NOTAS", "PEDIDO",
        "IDENTIFICACIÓN", "CORREO", "TELÉFONO", "DIRECCIÓN", "CIUDAD", "CAJERO"
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainW_reporteVentas()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.setMinimumSize(self.size())
        self.setMaximumSize(self.size())

        self.controlador = ControladorReporteVentas()

        self._configurar_ui()
        self._configurar_tablas()
        self._conectar_senales()

    # ---------------------------------------------------------
    def _configurar_ui(self):
        hoy = QDate.currentDate()
        self.ui.dateE_desde.setDate(hoy.addDays(-7))
        self.ui.dateE_Hasta.setDate(hoy)

        self.ui.progressB_barra.setValue(0)
        self.ui.lb_fecha.setText(datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.ui.lb_blancocomentario.setText("")

    # ---------------------------------------------------------
    def _configurar_tablas(self):
        """
        Configura las dos pestañas del QTabWidget con tablas
        """
        self.tabla_simples = QTableWidget()
        self.tabla_variados = QTableWidget()

        for tabla in (self.tabla_simples, self.tabla_variados):
            tabla.setColumnCount(len(self.HEADERS))
            tabla.setHorizontalHeaderLabels(self.HEADERS)
            tabla.setEditTriggers(QTableWidget.NoEditTriggers)

            font = QFont()
            font.setBold(True)
            for i in range(len(self.HEADERS)):
                tabla.horizontalHeaderItem(i).setFont(font)

        self.ui.tb_productos.removeTab(0)
        self.ui.tb_productos.removeTab(0)

        self.ui.tb_productos.addTab(self.tabla_simples, "Productos Simples")
        self.ui.tb_productos.addTab(self.tabla_variados, "Productos Variados")

    # ---------------------------------------------------------
    def _conectar_senales(self):
        self.ui.pbt_generar_reporte.clicked.connect(self.generar_reporte)
        self.ui.bt_volver.clicked.connect(self.close)

    # ---------------------------------------------------------
    def generar_reporte(self):
        """
        Genera el reporte:
        - Valida fechas
        - Obtiene ventas
        - Exporta Excel
        - Muestra datos en tablas
        """
        fecha_desde_qt = self.ui.dateE_desde.date()
        fecha_hasta_qt = self.ui.dateE_Hasta.date()

        if fecha_hasta_qt < fecha_desde_qt:
            QMessageBox.warning(
                self,
                "Fechas inválidas",
                "La fecha HASTA debe ser mayor que la fecha DESDE"
            )
            return

        fecha_desde = fecha_desde_qt.toString("yyyy-MM-dd")
        fecha_hasta = fecha_hasta_qt.toString("yyyy-MM-dd")

        try:
            self.ui.progressB_barra.setValue(10)
            self.ui.lb_blancocomentario.setText("Conectando con WooCommerce...")

            ventas = self.controlador.obtener_ventas(fecha_desde, fecha_hasta)

            self.ui.progressB_barra.setValue(50)
            self._cargar_tablas(ventas)

            nombre_archivo = f"reporte_ventas_{fecha_desde}_{fecha_hasta}.xlsx"
            self.controlador.exportar_excel(nombre_archivo)

            self.ui.progressB_barra.setValue(100)
            self.ui.lb_blancocomentario.setText("Se generó con éxito")

            QMessageBox.information(
                self,
                "Reporte generado",
                f"Reporte exportado correctamente:\n{nombre_archivo}"
            )

        except PyWooError as e:
            QMessageBox.critical(self, "Error", str(e))
            self.ui.progressB_barra.setValue(0)

    # ---------------------------------------------------------
    def _cargar_tablas(self, ventas):
        """
        Llena las tablas de productos simples y variados.
        (Por ahora se duplican, luego puedes separarlos por tipo)
        """
        self.tabla_simples.setRowCount(0)
        self.tabla_variados.setRowCount(0)

        for venta in ventas:
            fila = self.tabla_simples.rowCount()
            self.tabla_simples.insertRow(fila)
            self.tabla_variados.insertRow(fila)

            datos = [
                venta.get("date_created", ""),
                f"{venta['billing']['first_name']} {venta['billing']['last_name']}",
                venta.get("subtotal", ""),
                venta.get("shipping_total", ""),
                venta.get("total_tax", ""),
                venta.get("discount_total", ""),
                venta.get("total", ""),
                venta.get("payment_method_title", ""),
                "",  # UTILIDAD
                venta.get("status", ""),
                venta.get("customer_note", ""),
                venta.get("id", ""),
                venta["billing"].get("company", ""),
                venta["billing"].get("email", ""),
                venta["billing"].get("phone", ""),
                venta["billing"].get("address_1", ""),
                venta["billing"].get("city", ""),
                ""   # CAJERO
            ]

            for col, valor in enumerate(datos):
                item = QTableWidgetItem(str(valor))
                self.tabla_simples.setItem(fila, col, item)
                self.tabla_variados.setItem(fila, col, QTableWidgetItem(str(valor)))
