# app/lista_distribuidores/lista_distribuidores_view.py
from PySide6.QtCore import QThread, QDate, QEvent, Qt, QUrl
from PySide6.QtWidgets import QFileDialog, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QDesktopServices, QCursor
from shiboken6 import isValid

from app.lista_distribuidores.ui.ui_view_lista_distribuidores import Ui_ListaDistribuidores
from app.lista_distribuidores.controlador_lista_distribuidores import ControladorListaDistribuidores
from app.lista_distribuidores.worker_lista_distribuidores import WorkerListaDistribuidores

from app.core.base_windows import BaseModuleWindow
from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info
from app.core.table_enhancer import TableEnhancer
from app.core.disabled_click_filter import DisabledClickFilter

COL_URL = 11  # URL es la última columna


class ListaDistribuidoresView(BaseModuleWindow):
    def __init__(self, parent=None):
        super().__init__(menu_controller=parent, parent=parent)

        self.ui = Ui_ListaDistribuidores()
        self.ui.setupUi(self)

        # Estado del botón Exportar (para explicar por qué está bloqueado)
        self._export_reason: str = ""
        self._export_filter = DisabledClickFilter(self, lambda: self._export_reason, title="Exportar deshabilitado")
        self.ui.btnExportar.installEventFilter(self._export_filter)

        self._build_menu()

        self.controlador = ControladorListaDistribuidores()

        self.thread = None
        self.worker = None
        self.dialogo = None
        self._generado = False
        self._ocupado = False

        self._configurar()
        self._conectar()

        # --- Sorting + Buscador (SKU/NOMBRE) ---
        self._enhancer = TableEnhancer((self.ui.tableSimples, self.ui.tableVariados), search_columns=(0, 1))
        self._crear_buscador()

        # ✅ cursor mano al pasar por URL
        self.ui.tableSimples.viewport().installEventFilter(self)
        self.ui.tableVariados.viewport().installEventFilter(self)

    def _configurar(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            header.setStretchLastSection(False)
            header.setSectionResizeMode(COL_URL, QHeaderView.Stretch)  # ✅ URL ocupa el resto

        self._set_export_enabled(False, "Genera la lista para habilitar Exportar.")
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _set_export_enabled(self, enabled: bool, reason: str = "") -> None:
        self.ui.btnExportar.setEnabled(enabled)
        self._export_reason = "" if enabled else (reason or "Exportar no está disponible.")
        self.ui.btnExportar.setToolTip("" if enabled else self._export_reason)

    def _crear_buscador(self):
        """Agrega un buscador al layout (sin tocar el .ui generado)."""
        layout = self.ui.layoutMain
        fila = QHBoxLayout()

        lbl = QLabel("Buscar:")
        self._txt_buscar = QLineEdit()
        self._txt_buscar.setPlaceholderText("Buscar por SKU o nombre…")
        fila.addWidget(lbl)
        fila.addWidget(self._txt_buscar, 1)
        # Inserta después de la barra de progreso (antes de tabs)
        layout.insertLayout(3, fila)

        self._txt_buscar.textChanged.connect(self._on_buscar)
    def _tabla_activa(self):
        return self.ui.tableSimples if self.ui.tabWidget.currentIndex() == 0 else self.ui.tableVariados

    def _on_buscar(self, txt: str):
        self._enhancer.apply_search(self._tabla_activa(), txt)

    def _set_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
        self.ui.btnGenerar.setEnabled(not ocupado)
        self.ui.btnVolver.setEnabled(not ocupado)
        if ocupado:
            self._set_export_enabled(False, "Procesando... espera a que termine para exportar.")
        else:
            if self._generado:
                self._set_export_enabled(True)
            else:
                self._set_export_enabled(False, "Genera la lista para habilitar Exportar.")

    def _conectar(self):
        self.ui.btnGenerar.clicked.connect(self._generar)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

        # ✅ abrir URL con click
        self.ui.tableSimples.clicked.connect(self._abrir_url_desde_click)
        self.ui.tableVariados.clicked.connect(self._abrir_url_desde_click)

    def _volver_menu(self):
        if self._ocupado:
            return
        parent = self.parent()
        self.close()
        if parent:
            parent.show()

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
        if getattr(self, "menu_controller", None):
            try:
                self.menu_controller.raise_()
                self.menu_controller.activateWindow()
            except Exception:
                pass
        event.accept()

    def _generar(self):
        if self._ocupado:
            return

        self._detener_hilo()
        self._limpiar_estado()
        self._set_ocupado(True)

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Generando Lista de Productos para Distribuidores")
        self.dialogo.reset()
        self.dialogo.set_mensaje("Generando lista de productos para distribuidores...")
        self.dialogo.show()

        self.thread = QThread(self)
        self.worker = WorkerListaDistribuidores(self.controlador)
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

    def _cerrar_dialogo(self):
        if self.dialogo:
            try:
                self.dialogo.close()
            except Exception:
                pass
            self.dialogo = None


    def _aplicar_columnas_dinamicas(self):
        """Oculta columnas opcionales si no existen datos reales en la tienda."""
        def col_tiene_dato(rows, col):
            for r in rows or []:
                try:
                    v = r[col] if col < len(r) else None
                except Exception:
                    v = None
                if v is None:
                    continue
                s = str(v).strip()
                if s and s.upper() != 'N/A':
                    return True
            return False

        # Columnas opcionales: VARIACIÓN / OBSERVACIÓN / URL
        opcionales = [COL_VARIACION, COL_OBS, COL_URL]
        pares = [
            (self.ui.tableSimples, self.controlador.simples),
            (self.ui.tableVariados, self.controlador.variados),
        ]
        for tabla, rows in pares:
            for col in opcionales:
                try:
                    tabla.setColumnHidden(col, not col_tiene_dato(rows, col))
                except Exception:
                    pass

    def _finalizar(self, modelo_simples, modelo_variados):
        self._cerrar_dialogo()

        # Envolver en proxy (sorting + filtro)
        self._enhancer.set_models((modelo_simples, modelo_variados))

        # Ocultar columnas opcionales que no existan en la data
        self._aplicar_columnas_dinamicas()

        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setStretchLastSection(False)
            header.setSectionResizeMode(COL_URL, QHeaderView.Stretch)

        self.ui.labelEstado.setText("Lista generada correctamente")
        self._generado = True
        self._set_ocupado(False)

        mostrar_info("Lista de productos para distribuidores generada correctamente.", self)

    def _error(self, mensaje):
        self._cerrar_dialogo()
        self._set_ocupado(False)
        mostrar_error(mensaje, self)

    def _filas_ordenadas(self, tabla):
        """Filas en el orden visible (proxy: filtro + sort)."""
        modelo = tabla.model()
        if modelo is None:
            return []
        filas = []
        for r in range(modelo.rowCount()):
            fila = []
            for c in range(modelo.columnCount()):
                fila.append(modelo.index(r, c).data(Qt.DisplayRole))
            filas.append(fila)
        return filas


    def _exportar(self):
        hoy = QDate.currentDate().toString("ddMMyyyy")
        nombre = f"lista_distribuidores_{hoy}.xlsx"

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar lista de productos para distribuidores",
            nombre,
            "Excel (*.xlsx)"
        )
        if ruta:
            try:
                self.controlador.exportar_excel(ruta, simples=self._filas_ordenadas(self.ui.tableSimples), variados=self._filas_ordenadas(self.ui.tableVariados))
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)

    def _limpiar_estado(self):
        self._enhancer.clear()
        if getattr(self, "_txt_buscar", None):
            self._txt_buscar.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")
        self.ui.labelEstado.setText("")
        self._set_export_enabled(False, "Genera la lista para habilitar Exportar.")
        self._generado = False

    # ✅ abrir URL al click
    def _abrir_url_desde_click(self, index):
        if not index.isValid() or index.column() != COL_URL:
            return
        url = (index.data(Qt.DisplayRole) or "").strip()
        if url:
            QDesktopServices.openUrl(QUrl(url))

    # ✅ cursor mano SOLO cuando el mouse está sobre la columna URL
    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseMove:
            tabla = None
            if obj is self.ui.tableSimples.viewport():
                tabla = self.ui.tableSimples
            elif obj is self.ui.tableVariados.viewport():
                tabla = self.ui.tableVariados

            if tabla is not None:
                idx = tabla.indexAt(event.pos())
                if idx.isValid() and idx.column() == COL_URL:
                    tabla.viewport().setCursor(QCursor(Qt.PointingHandCursor))
                else:
                    tabla.viewport().unsetCursor()

        elif event.type() == QEvent.Leave:
            # cuando sale el mouse del viewport
            if obj in (self.ui.tableSimples.viewport(), self.ui.tableVariados.viewport()):
                obj.unsetCursor()

        return super().eventFilter(obj, event)
