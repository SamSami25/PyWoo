from PySide6.QtCore import QObject, Signal


class WorkerReporteVentas(QObject):
    progreso = Signal(int, str)
    terminado = Signal(object)
    error = Signal(str)

    def __init__(self, controlador, desde, hasta):
        super().__init__()
        self.controlador = controlador
        self.desde = desde
        self.hasta = hasta

    def ejecutar(self):
        try:
            modelo = self.controlador.generar_reporte(
                desde=self.desde,
                hasta=self.hasta,
                callback_progreso=self._emitir
            )
            self.terminado.emit(modelo)
        except Exception as e:
            self.error.emit(str(e))

    def _emitir(self, valor, mensaje):
        self.progreso.emit(valor, mensaje)
