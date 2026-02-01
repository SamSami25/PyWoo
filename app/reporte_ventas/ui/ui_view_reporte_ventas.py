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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QProgressBar, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QTableView,
    QVBoxLayout, QWidget)
import iconos_rc

class Ui_ReporteVentas(object):
    def setupUi(self, ReporteVentas):
        if not ReporteVentas.objectName():
            ReporteVentas.setObjectName(u"ReporteVentas")
        ReporteVentas.resize(1150, 700)
        icon = QIcon()
        icon.addFile(u":/assets/icons/label_reporte_ventas.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ReporteVentas.setWindowIcon(icon)
        self.centralwidget = QWidget(ReporteVentas)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutMain = QVBoxLayout(self.centralwidget)
        self.layoutMain.setSpacing(16)
        self.layoutMain.setObjectName(u"layoutMain")
        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")

        self.layoutMain.addWidget(self.labelTitulo)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.lblDesde = QLabel(self.centralwidget)
        self.lblDesde.setObjectName(u"lblDesde")

        self.hboxLayout.addWidget(self.lblDesde)

        self.dateDesde = QDateEdit(self.centralwidget)
        self.dateDesde.setObjectName(u"dateDesde")
        self.dateDesde.setCalendarPopup(True)

        self.hboxLayout.addWidget(self.dateDesde)

        self.lblHasta = QLabel(self.centralwidget)
        self.lblHasta.setObjectName(u"lblHasta")

        self.hboxLayout.addWidget(self.lblHasta)

        self.dateHasta = QDateEdit(self.centralwidget)
        self.dateHasta.setObjectName(u"dateHasta")
        self.dateHasta.setCalendarPopup(True)

        self.hboxLayout.addWidget(self.dateHasta)

        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.spacerItem)

        self.btnGenerar = QPushButton(self.centralwidget)
        self.btnGenerar.setObjectName(u"btnGenerar")

        self.hboxLayout.addWidget(self.btnGenerar)

        self.btnExportar = QPushButton(self.centralwidget)
        self.btnExportar.setObjectName(u"btnExportar")

        self.hboxLayout.addWidget(self.btnExportar)


        self.layoutMain.addLayout(self.hboxLayout)

        self.hboxLayout1 = QHBoxLayout()
        self.hboxLayout1.setObjectName(u"hboxLayout1")

        self.layoutMain.addLayout(self.hboxLayout1)

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
        self.tabPedidos = QWidget()
        self.tabPedidos.setObjectName(u"tabPedidos")
        self.verticalLayoutTabPedidos = QVBoxLayout(self.tabPedidos)
        self.verticalLayoutTabPedidos.setObjectName(u"verticalLayoutTabPedidos")
        self.tableSimples = QTableView(self.tabPedidos)
        self.tableSimples.setObjectName(u"tableSimples")

        self.verticalLayoutTabPedidos.addWidget(self.tableSimples)

        self.tabWidget.addTab(self.tabPedidos, "")

        self.layoutMain.addWidget(self.tabWidget)

        self.hboxLayout2 = QHBoxLayout()
        self.hboxLayout2.setObjectName(u"hboxLayout2")
        self.btnVolver = QPushButton(self.centralwidget)
        self.btnVolver.setObjectName(u"btnVolver")

        self.hboxLayout2.addWidget(self.btnVolver)

        self.labelEstado = QLabel(self.centralwidget)
        self.labelEstado.setObjectName(u"labelEstado")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelEstado.sizePolicy().hasHeightForWidth())
        self.labelEstado.setSizePolicy(sizePolicy)
        self.labelEstado.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstado.setWordWrap(True)

        self.hboxLayout2.addWidget(self.labelEstado)

        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout2.addItem(self.spacerItem1)


        self.layoutMain.addLayout(self.hboxLayout2)

        ReporteVentas.setCentralWidget(self.centralwidget)

        self.retranslateUi(ReporteVentas)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ReporteVentas)
    # setupUi

    def retranslateUi(self, ReporteVentas):
        ReporteVentas.setWindowTitle(QCoreApplication.translate("ReporteVentas", u"Reporte de Ventas", None))
        ReporteVentas.setStyleSheet(QCoreApplication.translate("ReporteVentas", u"\n"
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
        self.labelTitulo.setText(QCoreApplication.translate("ReporteVentas", u"Reporte Ventas", None))
        self.lblDesde.setText(QCoreApplication.translate("ReporteVentas", u"Desde", None))
        self.lblHasta.setText(QCoreApplication.translate("ReporteVentas", u"Hasta", None))
        self.btnGenerar.setText(QCoreApplication.translate("ReporteVentas", u"Generar Reporte", None))
        self.btnExportar.setText(QCoreApplication.translate("ReporteVentas", u"Exportar", None))
        self.lblProcesando.setText(QCoreApplication.translate("ReporteVentas", u"Procesando:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPedidos), QCoreApplication.translate("ReporteVentas", u"Pedidos", None))
        self.btnVolver.setText(QCoreApplication.translate("ReporteVentas", u"Volver al Men\u00fa", None))
        self.labelEstado.setText("")
    # retranslateUi

