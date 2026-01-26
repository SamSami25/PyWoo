from PySide6.QtCore import QObject, Signal


class WorkerActualizarProductos(QObject):
    # Para procesar (generar tablas)
    progreso = Signal(int, str)
    terminado = Signal(object, object)
    error = Signal(str)

    def __init__(self, controlador, datos_archivo):
        super().__init__()
        self.controlador = controlador
        self.datos_archivo = datos_archivo

    def ejecutar(self):
        try:
            modelo_simples, modelo_variados = self.controlador.procesar_productos(
                self.datos_archivo,
                callback=self._emitir_progreso
            )
            self.terminado.emit(modelo_simples, modelo_variados)
        except Exception as e:
            self.error.emit(str(e))

    def _emitir_progreso(self, valor, mensaje):
        self.progreso.emit(valor, mensaje)


class WorkerAplicarCambios(QObject):
    # Para aplicar cambios (actualizar tienda)
    progreso = Signal(int, str)
    terminado = Signal()
    error = Signal(str)

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

    def ejecutar(self):
        try:
            self.controlador.aplicar_cambios(callback=self._emitir_progreso)
            self.terminado.emit()
        except Exception as e:
            self.error.emit(str(e))

    def _emitir_progreso(self, valor, mensaje):
        self.progreso.emit(valor, mensaje)
