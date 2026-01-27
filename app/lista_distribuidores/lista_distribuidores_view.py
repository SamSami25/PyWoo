from PySide6.QtWidgets import QMainWindow, QFileDialog, QHeaderView
from PySide6.QtCore import Qt, QThread

from app.lista_distribuidores.ui.ui_view_lista_distribuidores import Ui_ListaDistribuidores
from app.lista_distribuidores.controlador_lista_distribuidores import ControladorListaDistribuidores
from app.lista_distribuidores.worker_lista_distribuidores import WorkerListaDistribuidores

from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class ListaDistribuidoresView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_ListaDistribuidores()
        self.ui.setupUi(self)

        self.controlador = ControladorListaDistribuidores()

        self.thread = None
        self.worker = None
        self.dialogo = None
        self._generado = False

        self._configurar()
        self._conectar()

    # -------------------------------------------------
    # CONFIGURACIÓN
    # -------------------------------------------------
    def _configurar(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

        self.ui.btnExportar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    # -------------------------------------------------
    # CONEXIONES
    # -------------------------------------------------
    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    # ✅ VOLVER AL MENÚ (FORMA CORRECTA)
    def _volver_menu(self):
        self._detener_hilo()
        parent = self.parent()
        self.hide()
        if parent:
            parent.show()

    # -------------------------------------------------
    # CONTROL DE HILO
    # -------------------------------------------------
    def _detener_hilo(self):
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        self.thread = None
        self.worker = None

    # ❌ NO cerrar la app
    def closeEvent(self, event):
        self._detener_hilo()
        event.ignore()
        self.hide()

    # -------------------------------------------------
    # GENERAR LISTA (ASYNC)
    # -------------------------------------------------
    def _generar(self):
        self._detener_hilo()
        self._limpiar_estado()

        self.dialogo = ProcessDialog(self)
        self.dialogo.setModal(True)
        self.dialogo.ui.lblTitulo.setText("Generando Lista de Distribuidores")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Generando lista de distribuidores...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerListaDistribuidores(self.controlador)
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

    def _finalizar(self, modelo_simples, modelo_variados):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None

        self.ui.tableSimples.setModel(modelo_simples)
        self.ui.tableVariados.setModel(modelo_variados)

        self.ui.labelEstado.setText("Lista generada correctamente")
        self.ui.btnExportar.setEnabled(True)
        self._generado = True

        mostrar_info("Lista de distribuidores generada correctamente.")

    def _error(self, mensaje):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None
        mostrar_error(mensaje)

    # -------------------------------------------------
    # EXPORTAR
    # -------------------------------------------------
    def _exportar(self):
        if not self._generado:
            mostrar_error("Debe generar la lista primero.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar lista de distribuidores",
            "lista_distribuidores.xlsx",
            "Excel (*.xlsx)"
        )

        if ruta:
            try:
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.")
            except Exception as e:
                mostrar_error(str(e))

    # -------------------------------------------------
    # UTILIDADES
    # -------------------------------------------------
    def _limpiar_estado(self):
        self.ui.tableSimples.setModel(None)
        self.ui.tableVariados.setModel(None)
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")
        self.ui.labelEstado.setText("")
        self.ui.btnExportar.setEnabled(False)
        self._generado = False
