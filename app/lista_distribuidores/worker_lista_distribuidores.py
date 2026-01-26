from PySide6.QtCore import QObject, Signal


class WorkerListaDistribuidores(QObject):
    progreso = Signal(int, str)
    terminado = Signal(object, object)
    error = Signal(str)

    def __init__(self, controlador):
        super().__init__()
        self.controlador = controlador

    def ejecutar(self):
        try:
            m_simples, m_variados = self.controlador.generar_lista(
                callback_progreso=self._emitir
            )
            self.terminado.emit(m_simples, m_variados)
        except Exception as e:
            self.error.emit(str(e))

    def _emitir(self, valor, mensaje):
        self.progreso.emit(valor, mensaje)
