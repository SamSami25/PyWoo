from PySide6.QtCore import QObject, Signal, Slot

class WorkerReporteVentas(QObject):
    progreso = Signal(int, str)
    terminado = Signal(object, object)
    error = Signal(str)

    def __init__(self, controlador, desde, hasta, should_cancel=None):
        super().__init__()
        self.controlador = controlador
        self.desde = desde
        self.hasta = hasta
        self.should_cancel = should_cancel

    @Slot()
    def ejecutar(self):
        try:
            modelos = self.controlador.generar_reporte(
                self.desde,
                self.hasta,
                callback_progreso=self.progreso.emit,
                should_cancel=self.should_cancel,
            )
            self.terminado.emit(*modelos)
        except Exception as e:
            msg = str(e)
            if msg == "__CANCELADO__":
                self.error.emit("__CANCELADO__")
            else:
                self.error.emit(f"Error al generar reporte: {e}")
