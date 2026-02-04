# app/reporte_ventas/reporte_ventas_view.py
from __future__ import annotations

from datetime import date

from PySide6.QtCore import QThread, QDate
from PySide6.QtWidgets import QFileDialog, QHeaderView
from shiboken6 import isValid

from app.core.base_windows import BaseModuleWindow
from app.reporte_ventas.ui.ui_view_reporte_ventas import Ui_ReporteVentas
from app.reporte_ventas.controlador_reporte_ventas import ControladorReporteVentas
from app.reporte_ventas.worker_reporte_ventas import WorkerReporteVentas

from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


def _fmt_ddmmyyyy(d: date) -> str:
    return f"{d.day:02d}{d.month:02d}{d.year:04d}"


class ReporteVentasView(BaseModuleWindow):
    def __init__(self, menu_controller, parent=None):
        super().__init__(menu_controller, parent)

        self.ui = Ui_ReporteVentas()
        self.ui.setupUi(self)

        self.controlador = ControladorReporteVentas()
        self._generado = False

        self.thread: QThread | None = None
        self.worker = None
        self.dialogo: ProcessDialog | None = None

        self._cancel_requested = False

        self._configurar()
        self._conectar()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------
    def _configurar(self):
        hoy = QDate.currentDate()
        self.ui.dateDesde.setDate(hoy.addYears(-1))
        self.ui.dateHasta.setDate(hoy)

        header = self.ui.tableSimples.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        if hasattr(self.ui, "tableVariados"):
            try:
                self.ui.tableVariados.hide()
                self.ui.tableVariados.setModel(None)
            except Exception:
                pass

        if hasattr(self.ui, "tabWidget"):
            try:
                for idx in reversed(range(self.ui.tabWidget.count())):
                    if not self.ui.tabWidget.tabText(idx).strip():
                        self.ui.tabWidget.removeTab(idx)
            except Exception:
                pass

        self.ui.btnExportar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

        if hasattr(self.ui, "txtNombreArchivo"):
            self.ui.txtNombreArchivo.setText("")

    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    # --------------------------------------------------
    # Validaciones
    # --------------------------------------------------
    def _validar_rango_fechas(self, desde: date, hasta: date) -> bool:
        hoy = QDate.currentDate().toPython()

        if desde > hoy or hasta > hoy:
            mostrar_error(
                "No puedes seleccionar fechas futuras. El reporte solo puede generarse hasta hoy.",
                self,
            )
            return False

        if desde > hasta:
            mostrar_error("La fecha 'Desde' no puede ser mayor que la fecha 'Hasta'.", self)
            return False

        return True

    # --------------------------------------------------
    # Navegación
    # --------------------------------------------------
    def _volver_menu(self):
        self._cancelar_si_hay_proceso()
        self._detener_hilo()
        self.close()
        if self.menu_controller:
            self.menu_controller.show()

    def closeEvent(self, event):
        self._cancelar_si_hay_proceso()
        self._detener_hilo()
        try:
            if self.menu_controller:
                self.menu_controller.show()
        except Exception:
            pass
        event.accept()

    # --------------------------------------------------
    # Hilos
    # --------------------------------------------------
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

    def _cancelar_si_hay_proceso(self):
        # ✅ Marca cancelación solo cuando el usuario cancela (o cerramos por navegación)
        self._cancel_requested = True

        # ✅ Solo cerrar el diálogo si está abierto (pero sin disparar "cancel" por cierre normal)
        if self.dialogo:
            try:
                # esto lo cierra como "cancelado"
                self.dialogo.reject()
            except Exception:
                pass
            self.dialogo = None

    # --------------------------------------------------
    # Generar
    # --------------------------------------------------
    def _generar(self):
        self._detener_hilo()

        desde = self.ui.dateDesde.date().toPython()
        hasta = self.ui.dateHasta.date().toPython()

        if not self._validar_rango_fechas(desde, hasta):
            return

        # ✅ Nueva ejecución = no está cancelado
        self._cancel_requested = False

        self._generado = False
        self.ui.btnExportar.setEnabled(False)
        self.ui.tableSimples.setModel(None)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Generando Reporte de Ventas")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Generando reporte...")

        # ✅ SOLO si el usuario cancela/cierra (reject)
        self.dialogo.rejected.connect(self._cancelar_si_hay_proceso)

        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerReporteVentas(
            self.controlador,
            desde,
            hasta,
            should_cancel=lambda: self._cancel_requested,
        )
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.ejecutar)
        self.worker.progreso.connect(self._actualizar_progreso)
        self.worker.terminado.connect(self._finalizar)
        self.worker.error.connect(self._error)

        self.worker.terminado.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.worker.terminado.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _actualizar_progreso(self, valor, mensaje):
        self.ui.progressBar.setValue(valor)
        self.ui.lblProcesando.setText(mensaje)

        if self.dialogo:
            self.dialogo.set_progreso(valor)
            self.dialogo.set_mensaje(mensaje)

    def _finalizar(self, modelo_pedidos, _modelo_vacio):
        # ✅ OJO: cerrar como "OK" para NO disparar rejected/cancel
        if self.dialogo:
            try:
                self.dialogo.accept()
            except Exception:
                pass
            self.dialogo = None

        if self._cancel_requested:
            self.ui.labelEstado.setText("")
            self.ui.btnExportar.setEnabled(False)
            self._generado = False
            return

        self.ui.tableSimples.setModel(modelo_pedidos)

        self.ui.labelEstado.setText("Reporte generado correctamente")
        self.ui.btnExportar.setEnabled(True)
        self._generado = True

        mostrar_info("Reporte de ventas generado correctamente.", self)

    def _error(self, mensaje):
        if self.dialogo:
            try:
                # si hubo error, cerramos como cancelado
                self.dialogo.reject()
            except Exception:
                pass
            self.dialogo = None

        # Cancelación silenciosa
        if mensaje == "__CANCELADO__" or self._cancel_requested:
            self.ui.labelEstado.setText("")
            self.ui.btnExportar.setEnabled(False)
            self._generado = False
            return

        mostrar_error(mensaje, self)

    # --------------------------------------------------
    # Exportar
    # --------------------------------------------------
    def _exportar(self):
        if not self._generado:
            mostrar_error("Debe generar el reporte primero.", self)
            return

        desde = self.ui.dateDesde.date().toPython()
        hasta = self.ui.dateHasta.date().toPython()

        nombre_defecto = f"ventas_{_fmt_ddmmyyyy(desde)}_{_fmt_ddmmyyyy(hasta)}.xlsx"

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar reporte",
            nombre_defecto,
            "Excel (*.xlsx)"
        )

        if ruta:
            try:
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)
