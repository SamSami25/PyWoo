from PySide6.QtWidgets import QMainWindow, QFileDialog, QHeaderView
from PySide6.QtCore import QThread
from shiboken6 import isValid

from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_ActualizarProductos
from app.actualizar_productos.controlador_actualizar_productos import ControladorActualizarProductos
from app.actualizar_productos.worker_actualizar_productos import (
    WorkerActualizarProductos,
    WorkerAplicarCambios,
)

from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class ActualizarProductosView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ActualizarProductos()
        self.ui.setupUi(self)

        self.controlador = ControladorActualizarProductos()
        self.datos_archivo = None

        self.thread = None
        self.worker = None
        self.thread_aplicar = None
        self.worker_aplicar = None

        self.dialogo = None
        self._procesado = False

        self._configurar_tablas()
        self._configurar_estado()
        self._conectar()

    # -------------------------------------------------
    def _configurar_tablas(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Interactive)
            header.setStretchLastSection(False)

    def _configurar_estado(self):
        self.ui.btnExportar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _conectar(self):
        self.ui.btnSubirArchivo.clicked.connect(self._subir_archivo)
        self.ui.btnAplicar.clicked.connect(self._aplicar_async)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    def _volver_menu(self):
        parent = self.parent()
        self.close()
        if parent:
            parent.show()

    # -------------------------------------------------
    def _detener_hilos(self):
        for thread in (self.thread, self.thread_aplicar):
            if thread and isValid(thread):
                try:
                    if thread.isRunning():
                        thread.quit()
                        thread.wait()
                except RuntimeError:
                    pass

        self.thread = None
        self.worker = None
        self.thread_aplicar = None
        self.worker_aplicar = None

    def closeEvent(self, event):
        self._detener_hilos()
        event.accept()

    # -------------------------------------------------
    def _subir_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Excel (*.xlsx *.xls);;CSV (*.csv)"
        )
        if not ruta:
            return

        try:
            self.datos_archivo = self.controlador.cargar_archivo(ruta)
            self.ui.labelArchivo.setText(f"Archivo: {ruta.split('/')[-1]}")
            self._procesar_async()
        except Exception as e:
            mostrar_error(str(e), self)

    # -------------------------------------------------
    def _procesar_async(self):
        self._detener_hilos()

        self._procesado = False
        self.ui.btnExportar.setEnabled(False)
        self.ui.tableSimples.setModel(None)
        self.ui.tableVariados.setModel(None)

        self.dialogo = ProcessDialog(self)
        self.dialogo.ui.lblTitulo.setText("Procesando Productos")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Procesando...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerActualizarProductos(self.controlador, self.datos_archivo)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.ejecutar)
        self.worker.progreso.connect(self._actualizar_progreso)
        self.worker.terminado.connect(self._finalizar_proceso)
        self.worker.error.connect(self._error)

        self.worker.terminado.connect(self.thread.quit)
        self.worker.terminado.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _aplicar_async(self):
        if not self._procesado:
            mostrar_error("Primero debe procesar los productos.", self)
            return

        self._detener_hilos()

        self.dialogo = ProcessDialog(self)
        self.dialogo.ui.lblTitulo.setText("Aplicando Cambios")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Aplicando cambios...")
        self.dialogo.show()

        self.thread_aplicar = QThread(self)
        self.worker_aplicar = WorkerAplicarCambios(self.controlador)
        self.worker_aplicar.moveToThread(self.thread_aplicar)

        self.thread_aplicar.started.connect(self.worker_aplicar.ejecutar)
        self.worker_aplicar.progreso.connect(self._actualizar_progreso)
        self.worker_aplicar.terminado.connect(self._finalizar_aplicar)
        self.worker_aplicar.error.connect(self._error)

        self.worker_aplicar.terminado.connect(self.thread_aplicar.quit)
        self.worker_aplicar.terminado.connect(self.worker_aplicar.deleteLater)
        self.thread_aplicar.finished.connect(self.thread_aplicar.deleteLater)

        self.thread_aplicar.start()

    def _actualizar_progreso(self, valor, mensaje):
        self.ui.progressBar.setValue(valor)
        self.ui.lblProcesando.setText(mensaje)
        if self.dialogo:
            self.dialogo.set_progreso(valor)
            self.dialogo.set_mensaje(mensaje)

    def _finalizar_proceso(self, modelo_simples, modelo_variados):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None

        self.ui.tableSimples.setModel(modelo_simples)
        self.ui.tableVariados.setModel(modelo_variados)

        self.ui.labelEstado.setText("Productos procesados correctamente")
        self.ui.btnExportar.setEnabled(True)
        self._procesado = True

        mostrar_info("Productos procesados correctamente.", self)

    def _finalizar_aplicar(self):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None
        mostrar_info("Cambios aplicados correctamente.", self)

    def _error(self, mensaje):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None
        mostrar_error(mensaje, self)

    # -------------------------------------------------
    def _exportar(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar productos",
            "productos_actualizados.xlsx",
            "Excel (*.xlsx)"
        )
        if ruta:
            try:
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)
