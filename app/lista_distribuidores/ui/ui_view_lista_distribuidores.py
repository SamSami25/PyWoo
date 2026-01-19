# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_lista_distribuidores.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 479)
        self.actionSistema = QAction(MainWindow)
        self.actionSistema.setObjectName(u"actionSistema")
        self.actionClaro = QAction(MainWindow)
        self.actionClaro.setObjectName(u"actionClaro")
        self.actionOscuro = QAction(MainWindow)
        self.actionOscuro.setObjectName(u"actionOscuro")
        self.actionReporte_Ventas = QAction(MainWindow)
        self.actionReporte_Ventas.setObjectName(u"actionReporte_Ventas")
        self.actionInventario = QAction(MainWindow)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionActualizar_Productos = QAction(MainWindow)
        self.actionActualizar_Productos.setObjectName(u"actionActualizar_Productos")
        self.actionLista_de_Distribuidores = QAction(MainWindow)
        self.actionLista_de_Distribuidores.setObjectName(u"actionLista_de_Distribuidores")
        self.actionAcerca_de = QAction(MainWindow)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.actionCredenciales_API = QAction(MainWindow)
        self.actionCredenciales_API.setObjectName(u"actionCredenciales_API")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.dateTimeEdit = QDateTimeEdit(self.centralwidget)
        self.dateTimeEdit.setObjectName(u"dateTimeEdit")
        self.dateTimeEdit.setGeometry(QRect(530, 30, 141, 22))
        self.dateTimeEdit.setStyleSheet(u"font: 9pt \"Consolas\";")
        self.lb_fecha = QLabel(self.centralwidget)
        self.lb_fecha.setObjectName(u"lb_fecha")
        self.lb_fecha.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(0, 0, 0);")
        self.lb_distribuidores = QLabel(self.centralwidget)
        self.lb_distribuidores.setObjectName(u"lb_distribuidores")
        self.lb_distribuidores.setGeometry(QRect(10, 10, 681, 58))
        self.lb_distribuidores.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 12pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.progressB_barra = QProgressBar(self.centralwidget)
        self.progressB_barra.setObjectName(u"progressB_barra")
        self.progressB_barra.setGeometry(QRect(10, 170, 691, 23))
        self.progressB_barra.setValue(24)
        self.lb_fondoblanco = QLabel(self.centralwidget)
        self.lb_fondoblanco.setObjectName(u"lb_fondoblanco")
        self.lb_fondoblanco.setGeometry(QRect(10, 80, 681, 75))
        self.lb_fondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
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
        self.lb_blancocomentario.setGeometry(QRect(169, 390, 511, 31))
        self.lb_blancocomentario.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
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
        self.bt_generar = QPushButton(self.centralwidget)
        self.bt_generar.setObjectName(u"bt_generar")
        self.bt_generar.setGeometry(QRect(20, 90, 131, 51))
        self.bt_generar.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
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
        self.lb_fecha_2 = QLabel(self.centralwidget)
        self.lb_fecha_2.setObjectName(u"lb_fecha_2")
        self.lb_fecha_2.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha_2.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(255, 255, 255);")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

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
        self.menuM_dulos.addAction(self.actionLista_de_Distribuidores)
        self.menuAyuda.addAction(self.actionAcerca_de)
        self.menuCredenciales_API.addAction(self.actionCredenciales_API)

        self.retranslateUi(MainWindow)

        self.tb_productos.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionSistema.setText(QCoreApplication.translate("MainWindow", u"Sistema", None))
        self.actionClaro.setText(QCoreApplication.translate("MainWindow", u"Claro", None))
        self.actionOscuro.setText(QCoreApplication.translate("MainWindow", u"Oscuro", None))
        self.actionReporte_Ventas.setText(QCoreApplication.translate("MainWindow", u"Reporte Ventas", None))
        self.actionInventario.setText(QCoreApplication.translate("MainWindow", u"Inventario", None))
        self.actionActualizar_Productos.setText(QCoreApplication.translate("MainWindow", u"Actualizar Productos", None))
        self.actionLista_de_Distribuidores.setText(QCoreApplication.translate("MainWindow", u"Lista de Distribuidores", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainWindow", u"Acerca de", None))
        self.actionCredenciales_API.setText(QCoreApplication.translate("MainWindow", u"Credenciales API", None))
        self.lb_fecha.setText("")
        self.lb_distribuidores.setText(QCoreApplication.translate("MainWindow", u"Lista de Distribuidores", None))
        self.lb_fondoblanco.setText("")
        self.bt_volver.setText(QCoreApplication.translate("MainWindow", u"Volver al Men\u00fa", None))
        self.lb_blancocomentario.setText("")
        self.bt_exportar.setText(QCoreApplication.translate("MainWindow", u"Exportar", None))
        self.bt_generar.setText(QCoreApplication.translate("MainWindow", u"Generar", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.lb_fecha_2.setText("")
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainWindow", u"Herramientas", None))
        self.menuM_dulos.setTitle(QCoreApplication.translate("MainWindow", u"M\u00f3dulos", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainWindow", u"Ayuda", None))
        self.menuCredenciales_API.setTitle(QCoreApplication.translate("MainWindow", u"WooCommerce", None))
    # retranslateUi

