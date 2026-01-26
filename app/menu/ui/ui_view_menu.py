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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)
import iconos_rc

class Ui_MenuPrincipal(object):
    def setupUi(self, MenuPrincipal):
        if not MenuPrincipal.objectName():
            MenuPrincipal.setObjectName(u"MenuPrincipal")
        MenuPrincipal.resize(750, 516)
        icon = QIcon()
        icon.addFile(u":/assets/icons/label_reporte_ventas2.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MenuPrincipal.setWindowIcon(icon)
        self.actionCredenciales_API = QAction(MenuPrincipal)
        self.actionCredenciales_API.setObjectName(u"actionCredenciales_API")
        self.actionReporte_Ventas = QAction(MenuPrincipal)
        self.actionReporte_Ventas.setObjectName(u"actionReporte_Ventas")
        self.actionInventario = QAction(MenuPrincipal)
        self.actionInventario.setObjectName(u"actionInventario")
        self.actionActualizar_Productos = QAction(MenuPrincipal)
        self.actionActualizar_Productos.setObjectName(u"actionActualizar_Productos")
        self.actionLista_de_Distribuidores = QAction(MenuPrincipal)
        self.actionLista_de_Distribuidores.setObjectName(u"actionLista_de_Distribuidores")
        self.actionSistema = QAction(MenuPrincipal)
        self.actionSistema.setObjectName(u"actionSistema")
        self.actionClaro = QAction(MenuPrincipal)
        self.actionClaro.setObjectName(u"actionClaro")
        self.actionOscuro = QAction(MenuPrincipal)
        self.actionOscuro.setObjectName(u"actionOscuro")
        self.actionAcerca_de = QAction(MenuPrincipal)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.centralwidget = QWidget(MenuPrincipal)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutMain = QVBoxLayout(self.centralwidget)
        self.verticalLayoutMain.setSpacing(24)
        self.verticalLayoutMain.setObjectName(u"verticalLayoutMain")
        self.labelMenu = QLabel(self.centralwidget)
        self.labelMenu.setObjectName(u"labelMenu")
        self.labelMenu.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addWidget(self.labelMenu)

        self.gridLayoutCards = QGridLayout()
        self.gridLayoutCards.setSpacing(30)
        self.gridLayoutCards.setObjectName(u"gridLayoutCards")
        self.btnVentas = QPushButton(self.centralwidget)
        self.btnVentas.setObjectName(u"btnVentas")
        self.btnVentas.setMinimumSize(QSize(350, 180))
        icon1 = QIcon()
        icon1.addFile(u":/assets/icons/label_reporte_ventas.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnVentas.setIcon(icon1)
        self.btnVentas.setIconSize(QSize(90, 90))

        self.gridLayoutCards.addWidget(self.btnVentas, 0, 0, 1, 1)

        self.btnInventario = QPushButton(self.centralwidget)
        self.btnInventario.setObjectName(u"btnInventario")
        self.btnInventario.setMinimumSize(QSize(350, 180))
        icon2 = QIcon()
        icon2.addFile(u":/assets/icons/inventario.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnInventario.setIcon(icon2)
        self.btnInventario.setIconSize(QSize(90, 90))

        self.gridLayoutCards.addWidget(self.btnInventario, 0, 1, 1, 1)

        self.btnActualizarProductos = QPushButton(self.centralwidget)
        self.btnActualizarProductos.setObjectName(u"btnActualizarProductos")
        self.btnActualizarProductos.setMinimumSize(QSize(350, 180))
        icon3 = QIcon()
        icon3.addFile(u":/assets/icons/actualizar_productos.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnActualizarProductos.setIcon(icon3)
        self.btnActualizarProductos.setIconSize(QSize(90, 90))

        self.gridLayoutCards.addWidget(self.btnActualizarProductos, 1, 0, 1, 1)

        self.btnDistribuidores = QPushButton(self.centralwidget)
        self.btnDistribuidores.setObjectName(u"btnDistribuidores")
        self.btnDistribuidores.setMinimumSize(QSize(350, 180))
        icon4 = QIcon()
        icon4.addFile(u":/assets/icons/distribuidores.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btnDistribuidores.setIcon(icon4)
        self.btnDistribuidores.setIconSize(QSize(90, 90))

        self.gridLayoutCards.addWidget(self.btnDistribuidores, 1, 1, 1, 1)


        self.verticalLayoutMain.addLayout(self.gridLayoutCards)

        MenuPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MenuPrincipal)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 750, 21))
        self.menuWoo = QMenu(self.menubar)
        self.menuWoo.setObjectName(u"menuWoo")
        self.menuModulos = QMenu(self.menubar)
        self.menuModulos.setObjectName(u"menuModulos")
        self.menuHerramientas = QMenu(self.menubar)
        self.menuHerramientas.setObjectName(u"menuHerramientas")
        self.menuAyuda = QMenu(self.menubar)
        self.menuAyuda.setObjectName(u"menuAyuda")
        MenuPrincipal.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuWoo.menuAction())
        self.menubar.addAction(self.menuModulos.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menubar.addAction(self.menuAyuda.menuAction())
        self.menuWoo.addAction(self.actionCredenciales_API)
        self.menuModulos.addAction(self.actionReporte_Ventas)
        self.menuModulos.addAction(self.actionInventario)
        self.menuModulos.addAction(self.actionActualizar_Productos)
        self.menuModulos.addAction(self.actionLista_de_Distribuidores)
        self.menuHerramientas.addAction(self.actionSistema)
        self.menuHerramientas.addAction(self.actionClaro)
        self.menuHerramientas.addAction(self.actionOscuro)
        self.menuAyuda.addAction(self.actionAcerca_de)

        self.retranslateUi(MenuPrincipal)

        QMetaObject.connectSlotsByName(MenuPrincipal)
    # setupUi

    def retranslateUi(self, MenuPrincipal):
        MenuPrincipal.setWindowTitle(QCoreApplication.translate("MenuPrincipal", u"Men\u00fa PyWoo", None))
        MenuPrincipal.setStyleSheet(QCoreApplication.translate("MenuPrincipal", u"\n"
"QMainWindow {\n"
"    background-color: #f2f2f2;\n"
"    font-family: Segoe UI;\n"
"}\n"
"\n"
"/* ================= BOTONES BASE ================= */\n"
"QPushButton {\n"
"    font-size: 11pt;\n"
"    font-weight: bold;\n"
"    border-radius: 16px;\n"
"    border-width: 2px;\n"
"    border-style: solid;\n"
"}\n"
"\n"
"/* ===== BOTONES AZULES ===== */\n"
"QPushButton#btnVentas,\n"
"QPushButton#btnDistribuidores {\n"
"    background-color: #1e73f1;\n"
"    color: white;\n"
"    border-color: white;\n"
"}\n"
"\n"
"QPushButton#btnVentas:hover,\n"
"QPushButton#btnDistribuidores:hover {\n"
"    background-color: #1558c0;\n"
"}\n"
"\n"
"QPushButton#btnVentas:pressed,\n"
"QPushButton#btnDistribuidores:pressed {\n"
"    background-color: #0d47a1;\n"
"}\n"
"\n"
"/* ===== BOTONES BLANCOS ===== */\n"
"QPushButton#btnInventario,\n"
"QPushButton#btnActualizarProductos {\n"
"    background-color: white;\n"
"    color: #1e73f1;\n"
"    border-color: #1e73f1;\n"
"}\n"
"\n"
"QPushButton#btnInventario:hover,\n"
"QPushButton"
                        "#btnActualizarProductos:hover {\n"
"    background-color: #e3f2fd;\n"
"}\n"
"\n"
"QPushButton#btnInventario:pressed,\n"
"QPushButton#btnActualizarProductos:pressed {\n"
"    background-color: #bbdefb;\n"
"}\n"
"   ", None))
        self.actionCredenciales_API.setText(QCoreApplication.translate("MenuPrincipal", u"Credenciales API", None))
        self.actionReporte_Ventas.setText(QCoreApplication.translate("MenuPrincipal", u"Reporte Ventas", None))
        self.actionInventario.setText(QCoreApplication.translate("MenuPrincipal", u"Inventario", None))
        self.actionActualizar_Productos.setText(QCoreApplication.translate("MenuPrincipal", u"Actualizar Productos", None))
        self.actionLista_de_Distribuidores.setText(QCoreApplication.translate("MenuPrincipal", u"Lista de Distribuidores", None))
        self.actionSistema.setText(QCoreApplication.translate("MenuPrincipal", u"Sistema", None))
        self.actionClaro.setText(QCoreApplication.translate("MenuPrincipal", u"Claro", None))
        self.actionOscuro.setText(QCoreApplication.translate("MenuPrincipal", u"Oscuro", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MenuPrincipal", u"Acerca de", None))
        self.labelMenu.setStyleSheet(QCoreApplication.translate("MenuPrincipal", u"\n"
"background-color: #1e73f1;\n"
"color: white;\n"
"font-size: 18pt;\n"
"font-weight: bold;\n"
"border-radius: 10px;\n"
"padding: 16px;\n"
"       ", None))
        self.labelMenu.setText(QCoreApplication.translate("MenuPrincipal", u"Men\u00fa", None))
        self.btnVentas.setText(QCoreApplication.translate("MenuPrincipal", u"Reporte Ventas", None))
        self.btnInventario.setText(QCoreApplication.translate("MenuPrincipal", u"Inventario", None))
        self.btnActualizarProductos.setText(QCoreApplication.translate("MenuPrincipal", u"Actualizar Productos", None))
        self.btnDistribuidores.setText(QCoreApplication.translate("MenuPrincipal", u"Lista de Distribuidores", None))
        self.menuWoo.setTitle(QCoreApplication.translate("MenuPrincipal", u"WooCommerce", None))
        self.menuModulos.setTitle(QCoreApplication.translate("MenuPrincipal", u"M\u00f3dulos", None))
        self.menuHerramientas.setTitle(QCoreApplication.translate("MenuPrincipal", u"Herramientas", None))
        self.menuAyuda.setTitle(QCoreApplication.translate("MenuPrincipal", u"Ayuda", None))
    # retranslateUi

