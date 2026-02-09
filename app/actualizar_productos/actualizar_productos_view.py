# app/actualizar_productos/actualizar_productos_view.py
import os

from PySide6.QtCore import QThread, QDate, Qt
from PySide6.QtWidgets import QFileDialog, QHeaderView, QHBoxLayout, QLabel, QLineEdit, QPushButton
from shiboken6 import isValid

from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_ActualizarProductos
from app.actualizar_productos.controlador_actualizar_productos import ControladorActualizarProductos, COL_CATEGORIA, COL_PRECIO_COMPRA
from app.actualizar_productos.worker_actualizar_productos import (
    WorkerActualizarProductos,
    WorkerAplicarCambios,
)

from app.core.base_windows import BaseModuleWindow
from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info
from app.core.table_enhancer import TableEnhancer
from app.core.disabled_click_filter import DisabledClickFilter


class ActualizarProductosView(BaseModuleWindow):
    """
    Vista del módulo Actualización de Productos.
    - Hilos para procesar y aplicar cambios sin congelar UI.
    """

    def __init__(self, parent=None):
        super().__init__(menu_controller=parent, parent=parent)

        self.ui = Ui_ActualizarProductos()
        self.ui.setupUi(self)

        # Estado del botón Exportar (para explicar por qué está bloqueado)
        self._export_reason: str = ""
        self._export_filter = DisabledClickFilter(self, lambda: self._export_reason, title="Exportar deshabilitado")
        self.ui.btnExportar.installEventFilter(self._export_filter)

        self._build_menu()

        self.controlador = ControladorActualizarProductos()
        self.datos_archivo = None

        self.thread = None
        self.worker = None
        self.thread_aplicar = None
        self.worker_aplicar = None

        self.dialogo = None
        self._procesado = False
        self._aplicado = False  # ✅ exportar solo después de aplicar
        self._ocupado = False

        self._configurar_tablas()
        self._configurar_estado()
        self._conectar()

        # --- Sorting + Buscador (SKU/NOMBRE) ---
        self._enhancer = TableEnhancer((self.ui.tableSimples, self.ui.tableVariados), search_columns=(0, 1))
        self._crear_buscador()

    # ----------------------------
    # UI
    # ----------------------------
    def _configurar_tablas(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setStretchLastSection(True)
            tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

    def _configurar_estado(self):
        self._set_export_enabled(False, "Primero procesa el archivo y aplica cambios para habilitar Exportar.")
        self.ui.btnAplicar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _set_export_enabled(self, enabled: bool, reason: str = "") -> None:
        self.ui.btnExportar.setEnabled(enabled)
        self._export_reason = "" if enabled else (reason or "Exportar no está disponible.")
        self.ui.btnExportar.setToolTip("" if enabled else self._export_reason)

    def _set_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
        self.ui.btnSubirArchivo.setEnabled(not ocupado)
        self.ui.btnVolver.setEnabled(not ocupado)
        # ✅ Exportar SOLO si ya se aplicó (y no está ocupado)
        if ocupado:
            self._set_export_enabled(False, "Procesando... espera a que termine para exportar.")
        else:
            if self._aplicado:
                self._set_export_enabled(True)
            else:
                self._set_export_enabled(False, "Aplica los cambios para habilitar Exportar.")
        # Aplicar se habilita cuando hay procesado
        self.ui.btnAplicar.setEnabled((not ocupado) and self._procesado)

    def _conectar(self):
        self.ui.btnSubirArchivo.clicked.connect(self._subir_archivo)
        self.ui.btnAplicar.clicked.connect(self._aplicar_async)
        self.ui.btnExportar.clicked.connect(self._exportar)
        self.ui.btnVolver.clicked.connect(self._volver_menu)

    # ----------------------------
    # Navegación
    # ----------------------------
    def _volver_menu(self):
        if self._ocupado:
            return
        parent = self.parent()
        self.close()
        if parent:
            parent.show()

    # ----------------------------
    # Threads lifecycle
    # ----------------------------
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
        if getattr(self, 'menu_controller', None):
            try:
                self.menu_controller.raise_()
                self.menu_controller.activateWindow()
            except Exception:
                pass
        event.accept()

    # ----------------------------
    # Archivo + Procesar
    # ----------------------------
    def _subir_archivo(self):
        if self._ocupado:
            return

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Excel (*.xlsx);;CSV (*.csv)"
        )
        if not ruta:
            return

        try:
            self.datos_archivo = self.controlador.cargar_archivo(ruta)
            self.ui.labelArchivo.setText(f"Archivo: {os.path.basename(ruta)}")
            self._procesar_async()
        except Exception as e:
            mostrar_error(str(e), self)

    def _procesar_async(self):
        if self._ocupado:
            return

        self._detener_hilos()
        self._set_ocupado(True)

        self._procesado = False
        self._aplicado = False  # ✅ reset: exportar bloqueado hasta aplicar
        self._set_export_enabled(False, "Procesando... primero aplica cambios para exportar.")
        self.ui.btnAplicar.setEnabled(False)
        self._enhancer.clear()
        if getattr(self, "_txt_buscar", None):
            self._txt_buscar.setText("")

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Procesando Productos")
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
        self.worker.error.connect(self.thread.quit)
        self.worker.terminado.connect(self.worker.deleteLater)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    # ----------------------------
    # Aplicar
    # ----------------------------
    def _aplicar_async(self):
        if self._ocupado:
            return

        if not self._procesado:
            mostrar_error("Primero debe procesar los productos.", self)
            return

        self._detener_hilos()
        self._set_ocupado(True)

        self.dialogo = ProcessDialog(self)
        self.dialogo.set_titulo("Aplicando Cambios")
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
        self.worker_aplicar.error.connect(self.thread_aplicar.quit)
        self.worker_aplicar.terminado.connect(self.worker_aplicar.deleteLater)
        self.worker_aplicar.error.connect(self.worker_aplicar.deleteLater)
        self.thread_aplicar.finished.connect(self.thread_aplicar.deleteLater)

        self.thread_aplicar.start()

    # ----------------------------
    # Eventos de progreso
    # ----------------------------
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
        # Oculta columnas opcionales si no existen datos reales en la data
        def tiene_valor(s: str) -> bool:
            return bool((s or '').strip()) and str(s).strip().upper() != 'N/A'

        # Columnas opcionales típicas en este módulo
        # - CATEGORÍA: algunas tiendas no envían categorías
        # - PRECIO COMPRA: campo custom, puede no existir
        col_checks = {
            COL_CATEGORIA: lambda r: tiene_valor(getattr(r, 'categoria', '') or ''),
            COL_PRECIO_COMPRA: lambda r: tiene_valor(getattr(r, 'precio_compra', '') or ''),
        }

        pares = [
            (self.ui.tableSimples, getattr(self.controlador, 'simples', [])),
            (self.ui.tableVariados, getattr(self.controlador, 'variados', [])),
        ]

        for tabla, registros in pares:
            for col, pred in col_checks.items():
                ok = any(pred(r) for r in (registros or []))
                try:
                    tabla.setColumnHidden(col, not ok)
                except Exception:
                    pass

    def _finalizar_proceso(self, modelo_simples, modelo_variados):
        self._cerrar_dialogo()

        # ✅ sorting + filtrado (proxy) para ambos tabs
        self._enhancer.set_models((modelo_simples, modelo_variados))

        # Ocultar columnas opcionales si no existen en la data
        self._aplicar_columnas_dinamicas()

        self.ui.labelEstado.setText("Productos procesados correctamente")
        self._procesado = True

        # ✅ Exportar sigue bloqueado hasta aplicar
        self._set_export_enabled(False, "Aplica los cambios para habilitar Exportar.")

        self._set_ocupado(False)
        mostrar_info("Productos procesados correctamente.", self)

    def _finalizar_aplicar(self):
        self._cerrar_dialogo()
        self._aplicado = True  # ✅ ahora sí se puede exportar
        self._set_ocupado(False)
        self._set_export_enabled(True)
        mostrar_info("Cambios aplicados correctamente.", self)

    def _error(self, mensaje):
        self._cerrar_dialogo()
        self._set_ocupado(False)
        mostrar_error(mensaje, self)

    # ----------------------------
    # Exportar
    # ----------------------------
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
        if self._ocupado:
            return

        if not self._aplicado:
            mostrar_error("Debe aplicar cambios antes de exportar.", self)
            return

        hoy = QDate.currentDate().toString("ddMMyyyy")
        nombre = f"actualizar_productos_{hoy}.xlsx"

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar productos",
            nombre,
            "Excel (*.xlsx)"
        )

        if ruta:
            try:
                self.controlador.exportar_excel(ruta, simples=self._filas_ordenadas(self.ui.tableSimples), variados=self._filas_ordenadas(self.ui.tableVariados))
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)
