from PySide6.QtCore import QObject, Signal


class WorkerInventario(QObject):
    progreso = Signal(int, str)
    terminado = Signal(object, object)
    error = Signal(str)

    def __init__(self, controlador, filtro):
        super().__init__()
        self.controlador = controlador
        self.filtro = filtro

    def ejecutar(self):
        try:
            modelo_simples, modelo_variados = self.controlador.generar_inventario(
                filtro=self.filtro,
                callback_progreso=self._emitir_progreso
            )
            self.terminado.emit(modelo_simples, modelo_variados)
        except Exception as e:
            self.error.emit(str(e))

    def _emitir_progreso(self, valor, mensaje):
        self.progreso.emit(valor, mensaje)
