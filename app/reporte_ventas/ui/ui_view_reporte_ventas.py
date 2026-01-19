# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_reporte_ventas.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QLabel, QMainWindow,
    QMenu, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStatusBar, QTabWidget, QWidget)

class Ui_MainW_reporteVentas(object):
    def setupUi(self, MainW_reporteVentas):
        if not MainW_reporteVentas.objectName():
            MainW_reporteVentas.setObjectName(u"MainW_reporteVentas")
        MainW_reporteVentas.resize(700, 479)
        self.actionSistema = QAction(MainW_reporteVentas)
        self.actionSistema.setObjectName(u"actionSistema")
        self.actionClaro = QAction(MainW_reporteVentas)
        self.actionClaro.setObjectName(u"actionClaro")
        self.actionOscuro = QAction(MainW_reporteVentas)
        self.actionOscuro.setObjectName(u"actionOscuro")
        self.actionReporte_Ventas = QAction(MainW_reporteVentas)
        self.actionReporte_Ventas.setObjectName(u"actionReporte_Ventas")
        self.actionInventario = QAction(MainW_reporteVentas)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionActualizar_Productos = QAction(MainW_reporteVentas)
        self.actionActualizar_Productos.setObjectName(u"actionActualizar_Productos")
        self.actionLista_de_Distribuidores = QAction(MainW_reporteVentas)
        self.actionLista_de_Distribuidores.setObjectName(u"actionLista_de_Distribuidores")
        self.actionAcerca_de = QAction(MainW_reporteVentas)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.centralwidget = QWidget(MainW_reporteVentas)
        self.centralwidget.setObjectName(u"centralwidget")
        self.lb_reporteVentas = QLabel(self.centralwidget)
        self.lb_reporteVentas.setObjectName(u"lb_reporteVentas")
        self.lb_reporteVentas.setGeometry(QRect(10, 10, 681, 58))
        self.lb_reporteVentas.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 12pt \"Arial Black\";\n"
"border-radius: 10px; \n"
"padding: 8px 12px;\n"
"")
        self.lb_fondoblanco = QLabel(self.centralwidget)
        self.lb_fondoblanco.setObjectName(u"lb_fondoblanco")
        self.lb_fondoblanco.setGeometry(QRect(10, 80, 681, 75))
        self.lb_fondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.lb_desde = QLabel(self.centralwidget)
        self.lb_desde.setObjectName(u"lb_desde")
        self.lb_desde.setGeometry(QRect(25, 110, 61, 20))
        self.lb_desde.setStyleSheet(u"font: 9pt \"Arial\";")
        self.lb_desde.setTextFormat(Qt.PlainText)
        self.lb_hasta = QLabel(self.centralwidget)
        self.lb_hasta.setObjectName(u"lb_hasta")
        self.lb_hasta.setGeometry(QRect(300, 110, 61, 20))
        self.lb_hasta.setStyleSheet(u"font: 9pt \"Arial\";")
        self.lb_hasta.setTextFormat(Qt.PlainText)
        self.dateE_desde = QDateEdit(self.centralwidget)
        self.dateE_desde.setObjectName(u"dateE_desde")
        self.dateE_desde.setGeometry(QRect(100, 110, 141, 22))
        self.dateE_desde.setStyleSheet(u"font: 9pt \"Consolas\";")
        self.dateE_Hasta = QDateEdit(self.centralwidget)
        self.dateE_Hasta.setObjectName(u"dateE_Hasta")
        self.dateE_Hasta.setGeometry(QRect(370, 110, 141, 22))
        self.dateE_Hasta.setStyleSheet(u"font: 9pt \"Consolas\";")
        self.pbt_generar_reporte = QPushButton(self.centralwidget)
        self.pbt_generar_reporte.setObjectName(u"pbt_generar_reporte")
        self.pbt_generar_reporte.setGeometry(QRect(529, 90, 151, 51))
        self.pbt_generar_reporte.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.progressB_barra = QProgressBar(self.centralwidget)
        self.progressB_barra.setObjectName(u"progressB_barra")
        self.progressB_barra.setGeometry(QRect(10, 170, 691, 23))
        self.progressB_barra.setValue(24)
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
        self.lb_blancocomentario = QLabel(self.centralwidget)
        self.lb_blancocomentario.setObjectName(u"lb_blancocomentario")
        self.lb_blancocomentario.setGeometry(QRect(169, 390, 511, 31))
        self.lb_blancocomentario.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
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
        self.lb_fecha = QLabel(self.centralwidget)
        self.lb_fecha.setObjectName(u"lb_fecha")
        self.lb_fecha.setGeometry(QRect(530, 30, 141, 22))
        self.lb_fecha.setStyleSheet(u"font: 9pt \"Consolas\";\n"
"color: rgb(0, 0, 0);")
        MainW_reporteVentas.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainW_reporteVentas)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 700, 21))
        self.menuHerramientas = QMenu(self.menubar)
        self.menuHerramientas.setObjectName(u"menuHerramientas")
        self.menuM_dulo = QMenu(self.menubar)
        self.menuM_dulo.setObjectName(u"menuM_dulo")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        self.menuCredenciales_API = QMenu(self.menubar)
        self.menuCredenciales_API.setObjectName(u"menuCredenciales_API")
        MainW_reporteVentas.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainW_reporteVentas)
        self.statusbar.setObjectName(u"statusbar")
        MainW_reporteVentas.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuCredenciales_API.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuM_dulo.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuHerramientas.addAction(self.actionSistema)
        self.menuHerramientas.addAction(self.actionClaro)
        self.menuHerramientas.addAction(self.actionOscuro)
        self.menuM_dulo.addAction(self.actionReporte_Ventas)
        self.menuM_dulo.addAction(self.actionInventario)
        self.menuM_dulo.addAction(self.actionActualizar_Productos)
        self.menuM_dulo.addAction(self.actionLista_de_Distribuidores)
        self.menuAyuda.addAction(self.actionAcerca_de)

        self.retranslateUi(MainW_reporteVentas)

        self.tb_productos.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainW_reporteVentas)
    # setupUi

    def retranslateUi(self, MainW_reporteVentas):
        MainW_reporteVentas.setWindowTitle(QCoreApplication.translate("MainW_reporteVentas", u"MainWindow", None))
        self.actionSistema.setText(QCoreApplication.translate("MainW_reporteVentas", u"Sistema", None))
        self.actionClaro.setText(QCoreApplication.translate("MainW_reporteVentas", u"Claro", None))
        self.actionOscuro.setText(QCoreApplication.translate("MainW_reporteVentas", u"Oscuro", None))
        self.actionReporte_Ventas.setText(QCoreApplication.translate("MainW_reporteVentas", u"Reporte Ventas", None))
        self.actionInventario.setText(QCoreApplication.translate("MainW_reporteVentas", u"Inventario", None))
        self.actionActualizar_Productos.setText(QCoreApplication.translate("MainW_reporteVentas", u"Actualizar Productos", None))
        self.actionLista_de_Distribuidores.setText(QCoreApplication.translate("MainW_reporteVentas", u"Lista de Distribuidores", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainW_reporteVentas", u"Acerca de", None))
        self.lb_reporteVentas.setText(QCoreApplication.translate("MainW_reporteVentas", u"Reporte Ventas", None))
        self.lb_fondoblanco.setText("")
        self.lb_desde.setText(QCoreApplication.translate("MainW_reporteVentas", u"Desde:", None))
        self.lb_hasta.setText(QCoreApplication.translate("MainW_reporteVentas", u"Hasta:", None))
        self.pbt_generar_reporte.setText(QCoreApplication.translate("MainW_reporteVentas", u"Generar Reporte", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab), QCoreApplication.translate("MainW_reporteVentas", u"Tab 1", None))
        self.tb_productos.setTabText(self.tb_productos.indexOf(self.tab_2), QCoreApplication.translate("MainW_reporteVentas", u"Tab 2", None))
        self.lb_blancocomentario.setText("")
        self.bt_volver.setText(QCoreApplication.translate("MainW_reporteVentas", u"Volver al Men\u00fa", None))
        self.lb_fecha.setText("")
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainW_reporteVentas", u"Herramientas", None))
        self.menuM_dulo.setTitle(QCoreApplication.translate("MainW_reporteVentas", u"M\u00f3dulos", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MainW_reporteVentas", u"Ayuda", None))
        self.menuCredenciales_API.setTitle(QCoreApplication.translate("MainW_reporteVentas", u"Credenciales API", None))
    # retranslateUi

