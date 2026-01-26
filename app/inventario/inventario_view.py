from PySide6.QtWidgets import QMainWindow, QFileDialog, QHeaderView
from PySide6.QtCore import Qt, QThread

from app.inventario.ui.ui_view_inventario import Ui_Inventario
from app.inventario.controlador_inventario import ControladorInventario
from app.inventario.worker_inventario import WorkerInventario

from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class InventarioView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Inventario()
        self.ui.setupUi(self)

        self.controlador = ControladorInventario()

        self.thread = None
        self.worker = None
        self.dialogo = None
        self._generado = False

        self._configurar_tablas()
        self._configurar_checks()
        self._configurar_estado()
        self._conectar()

    # -------------------------------------------------
    # CONFIGURACIÓN
    # -------------------------------------------------
    def _configurar_tablas(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

    def _configurar_checks(self):
        checks = (
            self.ui.checkTodos,
            self.ui.checkSinStock,
            self.ui.checkConStock,
        )

        for chk in checks:
            chk.toggled.connect(
                lambda checked, c=chk: self._exclusivo(c, checked)
            )

        self.ui.checkTodos.setChecked(True)

    def _configurar_estado(self):
        self.ui.btnExportar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    # -------------------------------------------------
    # CHECKBOXES EXCLUSIVOS
    # -------------------------------------------------
    def _exclusivo(self, activo, checked):
        if not checked:
            return

        for chk in (
            self.ui.checkTodos,
            self.ui.checkSinStock,
            self.ui.checkConStock,
        ):
            if chk is not activo:
                chk.blockSignals(True)
                chk.setChecked(False)
                chk.blockSignals(False)

    # -------------------------------------------------
    # CONEXIONES
    # -------------------------------------------------
    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._cerrar)

    # -------------------------------------------------
    # CONTROL DE HILO
    # -------------------------------------------------
    def _detener_hilo(self):
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

        self.thread = None
        self.worker = None

    def closeEvent(self, event):
        self._detener_hilo()
        event.accept()

    def _cerrar(self):
        self._detener_hilo()
        self.close()

    # -------------------------------------------------
    # GENERAR INVENTARIO (ASYNC)
    # -------------------------------------------------
    def _generar(self):
        self._detener_hilo()

        filtro = self._obtener_filtro()
        self._limpiar_tablas()
        self.ui.btnExportar.setEnabled(False)
        self._generado = False

        self.dialogo = ProcessDialog(self)
        self.dialogo.ui.lblTitulo.setText("Generando Inventario")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Generando inventario...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerInventario(self.controlador, filtro)
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

        self.ui.labelEstado.setText("Inventario generado correctamente")
        self.ui.btnExportar.setEnabled(True)
        self._generado = True

        mostrar_info("Inventario generado correctamente.")

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
            mostrar_error("Debe generar el inventario primero.")
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar inventario",
            "inventario.xlsx",
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
    def _obtener_filtro(self):
        if self.ui.checkSinStock.isChecked():
            return "sin_stock"
        if self.ui.checkConStock.isChecked():
            return "con_stock"
        return "todos"

    def _limpiar_tablas(self):
        self.ui.tableSimples.setModel(None)
        self.ui.tableVariados.setModel(None)
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")
        self.ui.labelEstado.setText("")
