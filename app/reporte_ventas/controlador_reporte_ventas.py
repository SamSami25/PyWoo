from PySide6.QtWidgets import QMainWindow, QFileDialog, QHeaderView
from PySide6.QtCore import QThread, QDate
from shiboken6 import isValid

from app.reporte_ventas.ui.ui_view_reporte_ventas import Ui_ReporteVentas
from app.reporte_ventas.controlador_reporte_ventas import ControladorReporteVentas
from app.reporte_ventas.worker_reporte_ventas import WorkerReporteVentas

from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class ReporteVentasView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ReporteVentas()
        self.ui.setupUi(self)

        self.controlador = ControladorReporteVentas()
        self._generado = False

        self.thread = None
        self.worker = None
        self.dialogo = None

        self._configurar()
        self._conectar()

    # -------------------------------------------------
    def _configurar(self):
        hoy = QDate.currentDate()
        self.ui.dateDesde.setDate(hoy)
        self.ui.dateHasta.setDate(hoy)

        header = self.ui.tableSimples.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.ui.btnExportar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    def _volver_menu(self):
        parent = self.parent()
        self.close()
        if parent:
            parent.show()

    # -------------------------------------------------
    def _detener_hilo(self):
        if self.thread and isValid(self.thread):
            try:
                if self.thread.isRunning():
                    self.thread.quit()
                    self.thread.wait()
            except RuntimeError:
                pass
        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        self._detener_hilo()
        event.accept()

    # -------------------------------------------------
    def _generar(self):
        self._detener_hilo()

        desde = self.ui.dateDesde.date().toPython()
        hasta = self.ui.dateHasta.date().toPython()

        self._generado = False
        self.ui.btnExportar.setEnabled(False)
        self.ui.tableSimples.setModel(None)

        self.dialogo = ProcessDialog(self)
        self.dialogo.ui.lblTitulo.setText("Generando Reporte de Ventas")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Generando reporte...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerReporteVentas(self.controlador, desde, hasta)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.ejecutar)
        self.worker.progreso.connect(self._actualizar_progreso)
        self.worker.terminado.connect(self._finalizar)
        self.worker.error.connect(self._error)

        self.worker.terminado.connect(self.thread.quit)
        self.worker.terminado.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _actualizar_progreso(self, valor, mensaje):
        self.ui.progressBar.setValue(valor)
        self.ui.lblProcesando.setText(mensaje)
        if self.dialogo:
            self.dialogo.set_progreso(valor)
            self.dialogo.set_mensaje(mensaje)

    def _finalizar(self, modelo):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None

        self.ui.tableSimples.setModel(modelo)
        self.ui.labelEstado.setText("Reporte generado correctamente")
        self.ui.btnExportar.setEnabled(True)
        self._generado = True

        mostrar_info("Reporte de ventas generado correctamente.")

    def _error(self, mensaje):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None
        mostrar_error(mensaje)

    # -------------------------------------------------
    def _exportar(self):
        if not self._generado:
            mostrar_error("Debe generar el reporte primero.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar reporte",
            "reporte_ventas.xlsx",
            "Excel (*.xlsx)"
        )

        if ruta:
            try:
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.")
            except Exception as e:
                mostrar_error(str(e))
