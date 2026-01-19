# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_menu.ui'
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
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainW_menu(object):
    def setupUi(self, MainW_menu):
        if not MainW_menu.objectName():
            MainW_menu.setObjectName(u"MainW_menu")
        MainW_menu.resize(700, 479)
        self.actionSistema = QAction(MainW_menu)
        self.actionSistema.setObjectName(u"actionSistema")
        self.actionClaro = QAction(MainW_menu)
        self.actionClaro.setObjectName(u"actionClaro")
        self.actionOscuro = QAction(MainW_menu)
        self.actionOscuro.setObjectName(u"actionOscuro")
        self.actionReporte_Ventas = QAction(MainW_menu)
        self.actionReporte_Ventas.setObjectName(u"actionReporte_Ventas")
        self.actionInventario = QAction(MainW_menu)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionActualizar_Productos = QAction(MainW_menu)
        self.actionActualizar_Productos.setObjectName(u"actionActualizar_Productos")
        self.actionLista_de_Dsitribuidores = QAction(MainW_menu)
        self.actionLista_de_Dsitribuidores.setObjectName(u"actionLista_de_Dsitribuidores")
        self.actionAcerca_de = QAction(MainW_menu)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.actionCredenciales_API = QAction(MainW_menu)
        self.actionCredenciales_API.setObjectName(u"actionCredenciales_API")
        self.centralwidget = QWidget(MainW_menu)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lb_fecha = QLabel(self.centralwidget)
        self.lb_fecha.setObjectName(u"lb_fecha")
        self.lb_fecha.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(0, 0, 0);")
        self.lb_fecha_2 = QLabel(self.centralwidget)
        self.lb_fecha_2.setObjectName(u"lb_fecha_2")
        self.lb_fecha_2.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha_2.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(0, 0, 0);")
        self.dateTimeEdit = QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(530, 30, 141, 22))
        self.dateTimeEdit.setStyleSheet(u"font: 9pt \"Consolas\";")
        self.lb_menu = QLabel(self.centralwidget)
        self.lb_menu.setObjectName(u"lb_menu")
        self.lb_menu.setGeometry(QRect(10, 10, 681, 58))
        self.lb_menu.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 16pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_menu.setAlignment(Qt.AlignCenter)
        self.lb_rfondoblanco = QLabel(self.centralwidget)
        self.lb_rfondoblanco.setObjectName(u"lb_rfondoblanco")
        self.lb_rfondoblanco.setGeometry(QRect(60, 100, 260, 151))
        self.lb_rfondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.bt_reporteventas = QPushButton(self.centralwidget)
        self.bt_reporteventas.setObjectName(u"bt_reporteventas")
        self.bt_reporteventas.setGeometry(QRect(70, 110, 241, 131))
        self.bt_reporteventas.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_afondoblanco = QLabel(self.centralwidget)
        self.lb_afondoblanco.setObjectName(u"lb_afondoblanco")
        self.lb_afondoblanco.setGeometry(QRect(60, 280, 260, 151))
        self.lb_afondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.lb_ifondoblanco = QLabel(self.centralwidget)
        self.lb_ifondoblanco.setObjectName(u"lb_ifondoblanco")
        self.lb_ifondoblanco.setGeometry(QRect(380, 100, 260, 151))
        self.lb_ifondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.lb_lfondoblanco = QLabel(self.centralwidget)
        self.lb_lfondoblanco.setObjectName(u"lb_lfondoblanco")
        self.lb_lfondoblanco.setGeometry(QRect(380, 280, 260, 151))
        self.lb_lfondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.bt_actualizarproductos = QPushButton(self.centralwidget)
        self.bt_actualizarproductos.setObjectName(u"bt_actualizarproductos")
        self.bt_actualizarproductos.setGeometry(QRect(70, 290, 241, 131))
        self.bt_actualizarproductos.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.bt_inventario = QPushButton(self.centralwidget)
        self.bt_inventario.setObjectName(u"bt_inventario")
        self.bt_inventario.setGeometry(QRect(390, 110, 241, 131))
        self.bt_inventario.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.bt_listadistribuidores = QPushButton(self.centralwidget)
        self.bt_listadistribuidores.setObjectName(u"bt_listadistribuidores")
        self.bt_listadistribuidores.setGeometry(QRect(390, 290, 241, 131))
        self.bt_listadistribuidores.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_reporte_ventas = QLabel(self.centralwidget)
        self.lb_reporte_ventas.setObjectName(u"lb_reporte_ventas")
        self.lb_reporte_ventas.setGeometry(QRect(70, 210, 241, 31))
        self.lb_reporte_ventas.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 10pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_reporte_ventas.setAlignment(Qt.AlignCenter)
        self.lb_inventario = QLabel(self.centralwidget)
        self.lb_inventario.setObjectName(u"lb_inventario")
        self.lb_inventario.setGeometry(QRect(390, 210, 241, 31))
        self.lb_inventario.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 10pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_inventario.setAlignment(Qt.AlignCenter)
        self.lb_actualizarproductos = QLabel(self.centralwidget)
        self.lb_actualizarproductos.setObjectName(u"lb_actualizarproductos")
        self.lb_actualizarproductos.setGeometry(QRect(70, 390, 241, 31))
        self.lb_actualizarproductos.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 10pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_actualizarproductos.setAlignment(Qt.AlignCenter)
        self.lb_listadistribuidores = QLabel(self.centralwidget)
        self.lb_listadistribuidores.setObjectName(u"lb_listadistribuidores")
        self.lb_listadistribuidores.setGeometry(QRect(390, 390, 241, 31))
        self.lb_listadistribuidores.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 10pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_listadistribuidores.setAlignment(Qt.AlignCenter)
        self.lb_fecha_3 = QLabel(self.centralwidget)
        self.lb_fecha_3.setObjectName(u"lb_fecha_3")
        self.lb_fecha_3.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha_3.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(0, 0, 0);")
        MainW_menu.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainW_menu)
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
        MainW_menu.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainW_menu)
        self.statusbar.setObjectName(u"statusbar")
        MainW_menu.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCredenciales_API.menuAction())
        self.menubar.addAction(self.menuM_dulos.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuHerramientas.addAction(self.actionSistema)
        self.menuHerramientas.addAction(self.actionClaro)
        self.menuHerramientas.addAction(self.actionOscuro)
        self.menuM_dulos.addAction(self.actionReporte_Ventas)
        self.menuM_dulos.addAction(self.actionInventario)
        self.menuM_dulos.addAction(self.actionActualizar_Productos)
        self.menuM_dulos.addAction(self.actionLista_de_Dsitribuidores)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menuCredenciales_API.addAction(self.actionCredenciales_API)

        self.retranslateUi(MainW_menu)

        QMetaObject.connectSlotsByName(MainW_menu)
    # setupUi

    def retranslateUi(self, MainW_menu):
        MainW_menu.setWindowTitle(QCoreApplication.translate("MainW_menu", u"MainWindow", None))
        self.actionSistema.setText(QCoreApplication.translate("MainW_menu", u"Sistema", None))
        self.actionClaro.setText(QCoreApplication.translate("MainW_menu", u"Claro", None))
        self.actionOscuro.setText(QCoreApplication.translate("MainW_menu", u"Oscuro", None))
        self.actionReporte_Ventas.setText(QCoreApplication.translate("MainW_menu", u"Reporte Ventas", None))
        self.actionInventario.setText(QCoreApplication.translate("MainW_menu", u"Inventario", None))
        self.actionActualizar_Productos.setText(QCoreApplication.translate("MainW_menu", u"Actualizar Productos", None))
        self.actionLista_de_Dsitribuidores.setText(QCoreApplication.translate("MainW_menu", u"Lista de Dsitribuidores", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainW_menu", u"Acerca de", None))
        self.actionCredenciales_API.setText(QCoreApplication.translate("MainW_menu", u"Credenciales API", None))
        self.lb_fecha.setText("")
        self.lb_fecha_2.setText("")
        self.lb_menu.setText(QCoreApplication.translate("MainW_menu", u"Men\u00fa", None))
        self.lb_rfondoblanco.setText("")
        self.bt_reporteventas.setText("")
        self.lb_afondoblanco.setText("")
        self.lb_ifondoblanco.setText("")
        self.lb_lfondoblanco.setText("")
        self.bt_actualizarproductos.setText("")
        self.bt_inventario.setText("")
        self.bt_listadistribuidores.setText("")
        self.lb_reporte_ventas.setText(QCoreApplication.translate("MainW_menu", u"Reporte Ventas", None))
        self.lb_inventario.setText(QCoreApplication.translate("MainW_menu", u"Inventario", None))
        self.lb_actualizarproductos.setText(QCoreApplication.translate("MainW_menu", u"Actualizar Prouctos", None))
        self.lb_listadistribuidores.setText(QCoreApplication.translate("MainW_menu", u"Lista de Distribuidores", None))
        self.lb_fecha_3.setText("")
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainW_menu", u"Herramientas", None))
        self.menuM_dulos.setTitle(QCoreApplication.translate("MainW_menu", u"M\u00f3dulos", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainW_menu", u"Ayuda", None))
        self.menuCredenciales_API.setTitle(QCoreApplication.translate("MainW_menu", u"Woocomerce", None))
    # retranslateUi

