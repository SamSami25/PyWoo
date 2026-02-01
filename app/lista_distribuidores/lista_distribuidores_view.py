# app/lista_distribuidores/lista_distribuidores_view.py
from PySide6.QtCore import QThread, QDate
from PySide6.QtWidgets import QFileDialog, QHeaderView
from shiboken6 import isValid

from app.lista_distribuidores.ui.ui_view_lista_distribuidores import Ui_ListaDistribuidores
from app.lista_distribuidores.controlador_lista_distribuidores import ControladorListaDistribuidores
from app.lista_distribuidores.worker_lista_distribuidores import WorkerListaDistribuidores

from app.core.base_windows import BaseModuleWindow
from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class ListaDistribuidoresView(BaseModuleWindow):
    """
    - Menú superior + tema claro (BaseModuleWindow)
    - Hilo para generar lista
    """

    def __init__(self, parent=None):
        super().__init__(menu_controller=parent, parent=parent)

        self.ui = Ui_ListaDistribuidores()
        self.ui.setupUi(self)

        # ✅ algunos .ui pueden pisar el menú común
        self._build_menu()

        self.controlador = ControladorListaDistribuidores()

        self.thread = None
        self.worker = None
        self.dialogo = None
        self._generado = False
        self._ocupado = False

        self._configurar()
        self._conectar()

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

    def _set_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
        self.ui.btnGenerar.setEnabled(not ocupado)
        self.ui.btnVolver.setEnabled(not ocupado)
        self.ui.btnExportar.setEnabled((not ocupado) and self._generado)

    # -------------------------------------------------
    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    def _volver_menu(self):
        if self._ocupado:
            return
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
        # ✅ Al cerrar con la X, el menú principal queda detrás y vuelve a estar activo
        if getattr(self, 'menu_controller', None):
            try:
                self.menu_controller.raise_()
                self.menu_controller.activateWindow()
            except Exception:
                pass

        
        event.accept()

    # -------------------------------------------------
    def _generar(self):
        if self._ocupado:
            return

        self._detener_hilo()
        self._limpiar_estado()
        self._set_ocupado(True)

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Generando Lista de Distribuidores")
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

        # limpieza
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

    def _cerrar_dialogo(self):
        if self.dialogo:
            try:
                self.dialogo.close()
            except Exception:
                pass
            self.dialogo = None

    def _finalizar(self, modelo_simples, modelo_variados):
        self._cerrar_dialogo()

        self.ui.tableSimples.setModel(modelo_simples)
        self.ui.tableVariados.setModel(modelo_variados)

        self.ui.labelEstado.setText("Lista generada correctamente")
        self._generado = True
        self._set_ocupado(False)

        mostrar_info("Lista de distribuidores generada correctamente.", self)

    def _error(self, mensaje):
        self._cerrar_dialogo()
        self._set_ocupado(False)
        mostrar_error(mensaje, self)

    # -------------------------------------------------
    def _exportar(self):
        hoy = QDate.currentDate().toString("ddMMyyyy")
        nombre = f"lista_distribuidores_{hoy}.xlsx"

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar lista de distribuidores",
            nombre,
            "Excel (*.xlsx)"
        )
        if ruta:
            try:
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)


    # -------------------------------------------------
    def _limpiar_estado(self):
        self.ui.tableSimples.setModel(None)
        self.ui.tableVariados.setModel(None)
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")
        self.ui.labelEstado.setText("")
        self.ui.btnExportar.setEnabled(False)
        self._generado = False
