# app/actualizar_productos/actualizar_productos_view.py
import os

from PySide6.QtCore import QThread, QDate, Qt
from PySide6.QtWidgets import QFileDialog, QHeaderView
from shiboken6 import isValid

from app.actualizar_productos.ui.ui_view_actualizar_productos import Ui_ActualizarProductos
from app.actualizar_productos.controlador_actualizar_productos import ControladorActualizarProductos
from app.actualizar_productos.worker_actualizar_productos import (
    WorkerActualizarProductos,
    WorkerAplicarCambios,
)

from app.core.base_windows import BaseModuleWindow
from app.core.proceso import ProcessDialog
from app.core.dialogos import mostrar_error, mostrar_info


class ActualizarProductosView(BaseModuleWindow):
    """
    Vista del módulo Actualización de Productos.
    - Hilos para procesar y aplicar cambios sin congelar UI.
    """

    def __init__(self, parent=None):
        super().__init__(menu_controller=parent, parent=parent)

        self.ui = Ui_ActualizarProductos()
        self.ui.setupUi(self)

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

    # ----------------------------
    # UI
    # ----------------------------
    def _configurar_tablas(self):
        for tabla in (self.ui.tableSimples, self.ui.tableVariados):
            header = tabla.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)
            header.setStretchLastSection(True)
            tabla.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def _configurar_estado(self):
        self.ui.btnExportar.setEnabled(False)
        self.ui.btnAplicar.setEnabled(False)
        self.ui.labelEstado.setText("")
        self.ui.progressBar.setValue(0)
        self.ui.lblProcesando.setText("")

    def _set_ocupado(self, ocupado: bool):
        self._ocupado = ocupado
        self.ui.btnSubirArchivo.setEnabled(not ocupado)
        self.ui.btnVolver.setEnabled(not ocupado)
        # ✅ Exportar SOLO si ya se aplicó
        self.ui.btnExportar.setEnabled((not ocupado) and self._aplicado)
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
        self.ui.btnExportar.setEnabled(False)
        self.ui.btnAplicar.setEnabled(False)
        self.ui.tableSimples.setModel(None)
        self.ui.tableVariados.setModel(None)

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

    def _finalizar_proceso(self, modelo_simples, modelo_variados):
        self._cerrar_dialogo()

        self.ui.tableSimples.setModel(modelo_simples)
        self.ui.tableVariados.setModel(modelo_variados)

        self.ui.labelEstado.setText("Productos procesados correctamente")
        self._procesado = True

        # ✅ Exportar sigue bloqueado hasta aplicar
        self.ui.btnExportar.setEnabled(False)

        self._set_ocupado(False)
        mostrar_info("Productos procesados correctamente.", self)

    def _finalizar_aplicar(self):
        self._cerrar_dialogo()
        self._aplicado = True  # ✅ ahora sí se puede exportar
        self._set_ocupado(False)
        self.ui.btnExportar.setEnabled(True)
        mostrar_info("Cambios aplicados correctamente.", self)

    def _error(self, mensaje):
        self._cerrar_dialogo()
        self._set_ocupado(False)
        mostrar_error(mensaje, self)

    # ----------------------------
    # Exportar
    # ----------------------------
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
                self.controlador.exportar_excel(ruta)
                mostrar_info("Archivo exportado correctamente.", self)
            except Exception as e:
                mostrar_error(str(e), self)
