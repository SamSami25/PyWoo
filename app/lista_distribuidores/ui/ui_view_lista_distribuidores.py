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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QTableView, QVBoxLayout,
    QWidget)
import iconos_rc

class Ui_ListaDistribuidores(object):
    def setupUi(self, ListaDistribuidores):
        if not ListaDistribuidores.objectName():
            ListaDistribuidores.setObjectName(u"ListaDistribuidores")
        ListaDistribuidores.resize(1250, 720)
        icon = QIcon()
        icon.addFile(u":/assets/icons/distribuidores.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ListaDistribuidores.setWindowIcon(icon)
        self.centralwidget = QWidget(ListaDistribuidores)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutMain = QVBoxLayout(self.centralwidget)
        self.layoutMain.setSpacing(16)
        self.layoutMain.setObjectName(u"layoutMain")
        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")

        self.layoutMain.addWidget(self.labelTitulo)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.btnGenerar = QPushButton(self.centralwidget)
        self.btnGenerar.setObjectName(u"btnGenerar")

        self.hboxLayout.addWidget(self.btnGenerar)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.spacerItem)

        self.btnExportar = QPushButton(self.centralwidget)
        self.btnExportar.setObjectName(u"btnExportar")

        self.hboxLayout.addWidget(self.btnExportar)


        self.layoutMain.addLayout(self.hboxLayout)

        self.layoutProgreso = QHBoxLayout()
        self.layoutProgreso.setObjectName(u"layoutProgreso")
        self.lblProcesando = QLabel(self.centralwidget)
        self.lblProcesando.setObjectName(u"lblProcesando")
        self.lblProcesando.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.layoutProgreso.addWidget(self.lblProcesando)

        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.layoutProgreso.addWidget(self.progressBar)


        self.layoutMain.addLayout(self.layoutProgreso)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabSimples = QWidget()
        self.tabSimples.setObjectName(u"tabSimples")
        self.vboxLayout = QVBoxLayout(self.tabSimples)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.tableSimples = QTableView(self.tabSimples)
        self.tableSimples.setObjectName(u"tableSimples")

        self.vboxLayout.addWidget(self.tableSimples)

        self.tabWidget.addTab(self.tabSimples, "")
        self.tabVariados = QWidget()
        self.tabVariados.setObjectName(u"tabVariados")
        self.vboxLayout1 = QVBoxLayout(self.tabVariados)
        self.vboxLayout1.setObjectName(u"vboxLayout1")
        self.tableVariados = QTableView(self.tabVariados)
        self.tableVariados.setObjectName(u"tableVariados")

        self.vboxLayout1.addWidget(self.tableVariados)

        self.tabWidget.addTab(self.tabVariados, "")

        self.layoutMain.addWidget(self.tabWidget)

        self.hboxLayout1 = QHBoxLayout()
        self.hboxLayout1.setObjectName(u"hboxLayout1")
        self.btnVolver = QPushButton(self.centralwidget)
        self.btnVolver.setObjectName(u"btnVolver")

        self.hboxLayout1.addWidget(self.btnVolver)

        self.labelEstado = QLabel(self.centralwidget)
        self.labelEstado.setObjectName(u"labelEstado")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelEstado.sizePolicy().hasHeightForWidth())
        self.labelEstado.setSizePolicy(sizePolicy)
        self.labelEstado.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstado.setWordWrap(True)

        self.hboxLayout1.addWidget(self.labelEstado)

        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout1.addItem(self.spacerItem1)


        self.layoutMain.addLayout(self.hboxLayout1)

        ListaDistribuidores.setCentralWidget(self.centralwidget)

        self.retranslateUi(ListaDistribuidores)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ListaDistribuidores)
    # setupUi

    def retranslateUi(self, ListaDistribuidores):
        ListaDistribuidores.setWindowTitle(QCoreApplication.translate("ListaDistribuidores", u"Lista de Distribuidores", None))
        ListaDistribuidores.setStyleSheet(QCoreApplication.translate("ListaDistribuidores", u"\n"
"QMainWindow {\n"
"    background-color: #f6f7fb;\n"
"    font-family: Segoe UI;\n"
"}\n"
"\n"
"/* ---------- T\u00cdTULO ---------- */\n"
"QLabel#labelTitulo {\n"
"    background-color: #1e73f1;\n"
"    color: white;\n"
"    font-size: 14pt;\n"
"    font-weight: bold;\n"
"    padding: 10px;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"/* ---------- BOTONES (BASE) ---------- */\n"
"QPushButton {\n"
"    border-radius: 8px;\n"
"    padding: 6px 14px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}\n"
"\n"
"/* BOT\u00d3N PRIMARIO */\n"
"QPushButton#btnGenerar {\n"
"    background-color: #1e73f1;\n"
"}\n"
"QPushButton#btnGenerar:hover {\n"
"    background-color: #1558c0;\n"
"}\n"
"QPushButton#btnGenerar:pressed {\n"
"    background-color: #0d47a1;\n"
"}\n"
"\n"
"/* BOT\u00d3N EXPORTAR */\n"
"QPushButton#btnExportar {\n"
"    background-color: #90caf9;\n"
"    color: #0d47a1;\n"
"}\n"
"QPushButton#btnExportar:hover {\n"
"    background-color: #64b5f6;\n"
"}\n"
"QPushButton#btnExportar:pressed {\n"
"    ba"
                        "ckground-color: #42a5f5;\n"
"}\n"
"\n"
"/* BOT\u00d3N VOLVER */\n"
"QPushButton#btnVolver {\n"
"    background-color: #9e9e9e;\n"
"}\n"
"QPushButton#btnVolver:hover {\n"
"    background-color: #757575;\n"
"}\n"
"QPushButton#btnVolver:pressed {\n"
"    background-color: #616161;\n"
"}\n"
"\n"
"/* ---------- PROGRESO ---------- */\n"
"QLabel#lblProcesando {\n"
"    color: #555555;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QProgressBar {\n"
"    border-radius: 6px;\n"
"    background: #e0e0e0;\n"
"}\n"
"QProgressBar::chunk {\n"
"    background-color: #1e73f1;\n"
"}\n"
"\n"
"/* ---------- MENSAJE ESTADO ---------- */\n"
"QLabel#labelEstado {\n"
"    background-color: #ffffff;\n"
"    border-radius: 6px;\n"
"    padding: 6px 10px;\n"
"    color: #333333;\n"
"}\n"
"\n"
"/* ---------- TABS ---------- */\n"
"QTabWidget::pane {\n"
"    border: none;\n"
"}\n"
"   ", None))
        self.labelTitulo.setText(QCoreApplication.translate("ListaDistribuidores", u"Lista de Distribuidores", None))
        self.btnGenerar.setText(QCoreApplication.translate("ListaDistribuidores", u"Generar Lista", None))
        self.btnExportar.setText(QCoreApplication.translate("ListaDistribuidores", u"Exportar", None))
        self.lblProcesando.setText(QCoreApplication.translate("ListaDistribuidores", u"Procesando:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSimples), QCoreApplication.translate("ListaDistribuidores", u"Productos Simples", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabVariados), QCoreApplication.translate("ListaDistribuidores", u"Productos Variados", None))
        self.btnVolver.setText(QCoreApplication.translate("ListaDistribuidores", u"Volver al Men\u00fa", None))
        self.labelEstado.setText("")
    # retranslateUi

