from __future__ import annotations

from PySide6.QtCore import QThread, QDate, Qt
from PySide6.QtWidgets import QFileDialog, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton
from shiboken6 import isValid

from app.inventario.ui.ui_view_inventario import Ui_Inventario
from app.inventario.controlador_inventario import ControladorInventario
from app.inventario.worker_inventario import WorkerInventario

from app.core.base_windows import BaseModuleWindow
from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info
from app.core.table_enhancer import TableEnhancer
from app.core.disabled_click_filter import DisabledClickFilter


class InventarioView(BaseModuleWindow):
    def __init__(self, parent=None):
        super().__init__(menu_controller=parent, parent=parent)

        self.ui = Ui_Inventario()
        self.ui.setupUi(self)

        # Estado del botón Exportar
        self._export_reason: str = ""
        self._export_filter = DisabledClickFilter(self, lambda: self._export_reason, title="Exportar deshabilitado")
        self.ui.btnExportar.installEventFilter(self._export_filter)

        try:
            self.ui.tabWidget.setCurrentIndex(0)
        except Exception:
            pass

        self.controlador = ControladorInventario()

        self.thread: QThread | None = None
        self.worker = None
        self.dialogo: ProcessDialog | None = None

        self._generado = False
        self._ocupado = False

        # Buscador
        # Limpia tablas.
        self._enhancer = TableEnhancer((self.ui.tableSimples, self.ui.tableVariados), search_columns=(0, 1))

        self._configurar_tablas()
        self._crear_buscador()
        self._configurar_checks()
        self._configurar_estado()
        self._conectar()

    def _configurar_tablas(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setStretchLastSection(True)

    def _crear_buscador(self):
        layout = self.ui.layoutMain
        fila = QHBoxLayout()

        lbl = QLabel("Buscar:")
        self._txt_buscar = QLineEdit()
        self._txt_buscar.setPlaceholderText("Buscar por SKU o nombre…")
        fila.addWidget(lbl)
        fila.addWidget(self._txt_buscar, 1)
        layout.insertLayout(3, fila)

        self._txt_buscar.textChanged.connect(self._on_buscar)
    def _tabla_activa(self):
        return self.ui.tableSimples if self.ui.tabWidget.currentIndex() == 0 else self.ui.tableVariados

    def _on_buscar(self, txt: str):
        self._enhancer.apply_search(self._tabla_activa(), txt)

    def _configurar_checks(self):
        self.ui.checkTodos.toggled.connect(self._on_check_todos)
        self.ui.checkSinStock.toggled.connect(self._on_check_sin_stock)
        self.ui.checkConStock.toggled.connect(self._on_check_con_stock)
        self.ui.checkTodos.setChecked(True)

    def _configurar_estado(self):
        self._set_export_enabled(False, "Genera el inventario para habilitar Exportar.")
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _set_export_enabled(self, enabled: bool, reason: str = "") -> None:
        self.ui.btnExportar.setEnabled(enabled)
        self._export_reason = "" if enabled else (reason or "Exportar no está disponible.")
        self.ui.btnExportar.setToolTip("" if enabled else self._export_reason)

    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)


    def _reset_checks(self, activo):
        for chk in (self.ui.checkTodos, self.ui.checkSinStock, self.ui.checkConStock):
            if chk is not activo:
                chk.blockSignals(True)
                chk.setChecked(False)
                chk.blockSignals(False)
        self._limpiar_tablas()

    def _on_check_todos(self, checked):
        if checked:
            self._reset_checks(self.ui.checkTodos)

    def _on_check_sin_stock(self, checked):
        if checked:
            self._reset_checks(self.ui.checkSinStock)

    def _on_check_con_stock(self, checked):
        if checked:
            self._reset_checks(self.ui.checkConStock)


    def _volver_menu(self):
        if self._ocupado:
            return
        self.close()
        if self.menu_controller:
            self.menu_controller.show()

    def closeEvent(self, event):
        self._detener_hilo()
        try:
            if self.menu_controller:
                self.menu_controller.show()
        except Exception:
            pass
        event.accept()


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


    def _generar(self):
        if self._ocupado:
            return

        self._detener_hilo()
        self._limpiar_tablas()
        self._set_export_enabled(False, "Generando inventario...")
        self._ocupado = True

        filtro = self._obtener_filtro()

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Generando Inventario")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Procesando inventario...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerInventario(self.controlador, filtro)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.ejecutar)
        self.worker.progreso.connect(self._actualizar_progreso)
        self.worker.terminado.connect(self._finalizar)
        self.worker.error.connect(self._error)

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

    def _finalizar(self, modelo_simples, modelo_variados):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None

        self._enhancer.set_models((modelo_simples, modelo_variados))

        self.ui.labelEstado.setText("Inventario generado correctamente")
        filas_visibles = 0
        try:
            filas_visibles = int(self._tabla_activa().model().rowCount())
        except Exception:
            filas_visibles = 0

        if filas_visibles > 0:
            self._set_export_enabled(True)
        else:
            self._set_export_enabled(False, "No hay datos para exportar con el filtro actual.")
        self._ocupado = False
        self._generado = True

        mostrar_info("Inventario generado correctamente.", self)

    def _error(self, mensaje):
        if self.dialogo:
            self.dialogo.close()
            self.dialogo = None
        self._ocupado = False
        mostrar_error(mensaje, self)


    def _filas_ordenadas(self, tabla):
        proxy = tabla.model()
        if proxy is None:
            return []

        source = getattr(proxy, "sourceModel", lambda: None)()
        datos = getattr(source, "_datos", None)

        if isinstance(datos, list):
            filas = []
            for r in range(proxy.rowCount()):
                try:
                    src_idx = proxy.mapToSource(proxy.index(r, 0))
                    filas.append(datos[src_idx.row()])
                except Exception:
                    filas.append({})
            return filas


        filas = []
        for r in range(proxy.rowCount()):
            fila = []
            for c in range(proxy.columnCount()):
                fila.append(proxy.index(r, c).data(Qt.DisplayRole))
            filas.append(fila)
        return filas


    def _exportar(self):
        if not self._generado:
            mostrar_error("Debe generar el inventario primero.", self)
            return

        hoy = QDate.currentDate().toString("ddMMyyyy")
        filtro = self._obtener_filtro()

        if filtro == "sin_stock":
            nombre = f"sin_stock_inventario_{hoy}.xlsx"
        elif filtro == "con_stock":
            nombre = f"con_stock_inventario_{hoy}.xlsx"
        else:
            nombre = f"inventario_{hoy}.xlsx"

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar inventario",
            nombre,
            "Excel (*.xlsx)"
        )

        if ruta:
            try:
                self.controlador.exportar_excel(ruta, filtro=filtro, simples=self._filas_ordenadas(self.ui.tableSimples), variados=self._filas_ordenadas(self.ui.tableVariados))
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)


    def _obtener_filtro(self):
        if self.ui.checkSinStock.isChecked():
            return "sin_stock"
        if self.ui.checkConStock.isChecked():
            return "con_stock"
        return "todos"

    def _limpiar_tablas(self):
        if hasattr(self, "_enhancer"):
            self._enhancer.clear()
        if getattr(self, "_txt_buscar", None):
            self._txt_buscar.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")
        self.ui.labelEstado.setText("")
        self._set_export_enabled(False, "Genera el inventario para habilitar Exportar.")
        self._generado = False
