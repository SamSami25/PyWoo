# app/reporte_ventas/worker_reporte_ventas.py
from PySide6.QtCore import QObject, Signal, Slot


class WorkerReporteVentas(QObject):
    progreso = Signal(int, str)
    terminado = Signal(object, object)
    error = Signal(str)

    def __init__(self, controlador, desde, hasta):
        super().__init__()
        self.controlador = controlador
        self.desde = desde
        self.hasta = hasta

    @Slot()
    def ejecutar(self):
        try:
            modelos = self.controlador.generar_reporte(
                self.desde,
                self.hasta,
                callback_progreso=self.progreso.emit
            )
            self.terminado.emit(*modelos)
        except Exception as e:
            # opcional: mensaje más claro
            self.error.emit(f"Error al generar reporte: {e}")
