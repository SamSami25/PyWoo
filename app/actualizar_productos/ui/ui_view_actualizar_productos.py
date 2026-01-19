# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_actualizar_productos.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QLabel, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QWidget)

class Ui_MainW_actualizarproductos(object):
    def setupUi(self, MainW_actualizarproductos):
        if not MainW_actualizarproductos.objectName():
            MainW_actualizarproductos.setObjectName(u"MainW_actualizarproductos")
        MainW_actualizarproductos.resize(700, 479)
        self.actionSistema = QAction(MainW_actualizarproductos)
        self.actionSistema.setObjectName(u"actionSistema")
        self.actionClaro = QAction(MainW_actualizarproductos)
        self.actionClaro.setObjectName(u"actionClaro")
        self.actionOscuro = QAction(MainW_actualizarproductos)
        self.actionOscuro.setObjectName(u"actionOscuro")
        self.actionReporte_Ventas = QAction(MainW_actualizarproductos)
        self.actionReporte_Ventas.setObjectName(u"actionReporte_Ventas")
        self.actionInventario = QAction(MainW_actualizarproductos)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionActualizaci_n_de_Productos = QAction(MainW_actualizarproductos)
        self.actionActualizaci_n_de_Productos.setObjectName(u"actionActualizaci_n_de_Productos")
        self.actionLista_de_Distribuidores = QAction(MainW_actualizarproductos)
        self.actionLista_de_Distribuidores.setObjectName(u"actionLista_de_Distribuidores")
        self.actionAcerca_de = QAction(MainW_actualizarproductos)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.actionCredenciales_API = QAction(MainW_actualizarproductos)
        self.actionCredenciales_API.setObjectName(u"actionCredenciales_API")
        self.centralwidget = QWidget(MainW_actualizarproductos)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressB_barra = QProgressBar(self.centralwidget)
        self.progressB_barra.setObjectName(u"progressB_barra")
        self.progressB_barra.setGeometry(QRect(10, 170, 691, 23))
        self.progressB_barra.setValue(24)
        self.dateTimeEdit = QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(530, 30, 141, 22))
        self.dateTimeEdit.setStyleSheet(u"font: 9pt \"Consolas\";")
        self.bt_volver = QPushButton(self.centralwidget)
        self.bt_volver.setObjectName(u"bt_volver")
        self.bt_volver.setGeometry(QRect(19, 380, 131, 51))
        self.bt_volver.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_blancocomentario = QLabel(self.centralwidget)
        self.lb_blancocomentario.setObjectName(u"lb_blancocomentario")
        self.lb_blancocomentario.setGeometry(QRect(169, 380, 511, 51))
        self.lb_blancocomentario.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.lb_actualizar = QLabel(self.centralwidget)
        self.lb_actualizar.setObjectName(u"lb_actualizar")
        self.lb_actualizar.setGeometry(QRect(10, 10, 681, 58))
        self.lb_actualizar.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 12pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.tb_productos = QTabWidget(self.centralwidget)
        self.tb_productos.setObjectName(u"tb_productos")
        self.tb_productos.setGeometry(QRect(10, 200, 681, 171))
        self.tb_productos.setStyleSheet(u"font: 9pt \"Arial\";")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tb_productos.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tb_productos.addTab(self.tab_2, "")
        self.lb_fondoblanco = QLabel(self.centralwidget)
        self.lb_fondoblanco.setObjectName(u"lb_fondoblanco")
        self.lb_fondoblanco.setGeometry(QRect(10, 80, 681, 75))
        self.lb_fondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.bt_exportar = QPushButton(self.centralwidget)
        self.bt_exportar.setObjectName(u"bt_exportar")
        self.bt_exportar.setGeometry(QRect(540, 90, 131, 51))
        self.bt_exportar.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.bt_subirArchivo = QPushButton(self.centralwidget)
        self.bt_subirArchivo.setObjectName(u"bt_subirArchivo")
        self.bt_subirArchivo.setGeometry(QRect(20, 90, 131, 51))
        self.bt_subirArchivo.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_archivocomentario = QLabel(self.centralwidget)
        self.lb_archivocomentario.setObjectName(u"lb_archivocomentario")
        self.lb_archivocomentario.setGeometry(QRect(160, 100, 201, 31))
        self.lb_archivocomentario.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"font: 10pt \"Arial\";\n"
"background-color: rgb(170, 209, 255);\n"
"\n"
"")
        self.bt_actualizar = QPushButton(self.centralwidget)
        self.bt_actualizar.setObjectName(u"bt_actualizar")
        self.bt_actualizar.setGeometry(QRect(390, 90, 131, 51))
        self.bt_actualizar.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_fecha = QLabel(self.centralwidget)
        self.lb_fecha.setObjectName(u"lb_fecha")
        self.lb_fecha.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        MainW_actualizarproductos.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainW_actualizarproductos)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 21))
        self.menuHerramientas = QMenu(self.menubar)
        self.menuHerramientas.setObjectName(u"menuHerramientas")
        self.menuM_dulos = QMenu(self.menubar)
        self.menuM_dulos.setObjectName(u"menuM_dulos")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        self.menuCredenciales_API = QMenu(self.menubar)
        self.menuCredenciales_API.setObjectName(u"menuCredenciales_API")
        MainW_actualizarproductos.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainW_actualizarproductos)
        self.statusbar.setObjectName(u"statusbar")
        MainW_actualizarproductos.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCredenciales_API.menuAction())
        self.menubar.addAction(self.menuM_dulos.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuHerramientas.addAction(self.actionSistema)
        self.menuHerramientas.addAction(self.actionClaro)
        self.menuHerramientas.addAction(self.actionOscuro)
        self.menuM_dulos.addAction(self.actionReporte_Ventas)
        self.menuM_dulos.addAction(self.actionInventario)
        self.menuM_dulos.addAction(self.actionActualizaci_n_de_Productos)
        self.menuM_dulos.addAction(self.actionLista_de_Distribuidores)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menuCredenciales_API.addAction(self.actionCredenciales_API)

        self.retranslateUi(MainW_actualizarproductos)

        QMetaObject.connectSlotsByName(MainW_actualizarproductos)
    # setupUi

    def retranslateUi(self, MainW_actualizarproductos):
        MainW_actualizarproductos.setWindowTitle(QCoreApplication.translate("MainW_actualizarproductos", u"MainWindow", None))
        self.actionSistema.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Sistema", None))
        self.actionClaro.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Claro", None))
        self.actionOscuro.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Oscuro", None))
        self.actionReporte_Ventas.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Reporte Ventas", None))
        self.actionInventario.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Inventario", None))
        self.actionActualizaci_n_de_Productos.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Actualizaci\u00f3n de Productos", None))
        self.actionLista_de_Distribuidores.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Lista de Distribuidores", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Acerca de", None))
        self.actionCredenciales_API.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Credenciales API", None))
        self.bt_volver.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Volver al Men\u00fa", None))
        self.lb_blancocomentario.setText("")
        self.lb_actualizar.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Actualizar Productos", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab), QCoreApplication.translate("MainW_actualizarproductos", u"Tab 1", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab_2), QCoreApplication.translate("MainW_actualizarproductos", u"Tab 2", None))
        self.lb_fondoblanco.setText("")
        self.bt_exportar.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Exportar", None))
        self.bt_subirArchivo.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Subir Archivo", None))
        self.lb_archivocomentario.setText("")
        self.bt_actualizar.setText(QCoreApplication.translate("MainW_actualizarproductos", u"Actualizar", None))
        self.lb_fecha.setText("")
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainW_actualizarproductos", u"Herramientas", None))
        self.menuM_dulos.setTitle(QCoreApplication.translate("MainW_actualizarproductos", u"M\u00f3dulos", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainW_actualizarproductos", u"Ayuda", None))
        self.menuCredenciales_API.setTitle(QCoreApplication.translate("MainW_actualizarproductos", u"WooCommerce", None))
    # retranslateUi

