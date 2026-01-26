# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_proceso.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

class Ui_ProcessDialog(object):
    def setupUi(self, ProcessDialog):
        if not ProcessDialog.objectName():
            ProcessDialog.setObjectName(u"ProcessDialog")
        ProcessDialog.resize(640, 520)
        ProcessDialog.setModal(True)
        self.verticalLayoutMain = QVBoxLayout(ProcessDialog)
        self.verticalLayoutMain.setSpacing(14)
        self.verticalLayoutMain.setObjectName(u"verticalLayoutMain")
        self.frameHeader = QFrame(ProcessDialog)
        self.frameHeader.setObjectName(u"frameHeader")
        self.vboxLayout = QVBoxLayout(self.frameHeader)
        self.vboxLayout.setObjectName(u"vboxLayout")
        self.lblTitulo = QLabel(self.frameHeader)
        self.lblTitulo.setObjectName(u"lblTitulo")
        self.lblTitulo.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.lblTitulo)

        self.lblSubtitulo = QLabel(self.frameHeader)
        self.lblSubtitulo.setObjectName(u"lblSubtitulo")
        self.lblSubtitulo.setAlignment(Qt.AlignCenter)

        self.vboxLayout.addWidget(self.lblSubtitulo)


        self.verticalLayoutMain.addWidget(self.frameHeader)

        self.progressBar = QProgressBar(ProcessDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayoutMain.addWidget(self.progressBar)

        self.label = QLabel(ProcessDialog)
        self.label.setObjectName(u"label")

        self.verticalLayoutMain.addWidget(self.label)

        self.textLog = QTextEdit(ProcessDialog)
        self.textLog.setObjectName(u"textLog")
        self.textLog.setReadOnly(True)

        self.verticalLayoutMain.addWidget(self.textLog)

        self.lblMensaje = QLabel(ProcessDialog)
        self.lblMensaje.setObjectName(u"lblMensaje")
        self.lblMensaje.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addWidget(self.lblMensaje)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.spacerItem)

        self.btnCancelar = QPushButton(ProcessDialog)
        self.btnCancelar.setObjectName(u"btnCancelar")

        self.hboxLayout.addWidget(self.btnCancelar)

        self.spacerItem1 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.hboxLayout.addItem(self.spacerItem1)


        self.verticalLayoutMain.addLayout(self.hboxLayout)

        self.lblNota = QLabel(ProcessDialog)
        self.lblNota.setObjectName(u"lblNota")
        self.lblNota.setAlignment(Qt.AlignCenter)

        self.verticalLayoutMain.addWidget(self.lblNota)


        self.retranslateUi(ProcessDialog)

        QMetaObject.connectSlotsByName(ProcessDialog)
    # setupUi

    def retranslateUi(self, ProcessDialog):
        ProcessDialog.setWindowTitle(QCoreApplication.translate("ProcessDialog", u"Procesando...", None))
        ProcessDialog.setStyleSheet(QCoreApplication.translate("ProcessDialog", u"\n"
"QDialog {\n"
"    background-color: #ffffff;\n"
"    font-family: Segoe UI;\n"
"}\n"
"\n"
"/* ---------- HEADER ---------- */\n"
"QFrame#frameHeader {\n"
"    background-color: #1e73f1;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QLabel#lblTitulo {\n"
"    font-size: 14pt;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}\n"
"\n"
"QLabel#lblSubtitulo {\n"
"    color: #e3f2fd;\n"
"    margin-top: 4px;\n"
"}\n"
"\n"
"/* ---------- PROGRESO ---------- */\n"
"QProgressBar {\n"
"    height: 22px;\n"
"    border-radius: 10px;\n"
"    background: #e0e0e0;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #4caf50;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"/* ---------- LOG ---------- */\n"
"QTextEdit#textLog {\n"
"    background-color: #1e1e1e;\n"
"    color: #ffffff;\n"
"    border-radius: 8px;\n"
"    padding: 8px;\n"
"    font-family: Consolas, monospace;\n"
"    font-size: 9.5pt;\n"
"}\n"
"\n"
"/* ---------- BOTON CANCELAR ---------- */\n"
"QPushButton#btnCancel"
                        "ar {\n"
"    background-color: #f44336;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 8px 22px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btnCancelar:hover {\n"
"    background-color: #d32f2f;\n"
"}\n"
"\n"
"QPushButton#btnCancelar:pressed {\n"
"    background-color: #b71c1c;\n"
"}\n"
"\n"
"/* ---------- TEXTOS ---------- */\n"
"QLabel#lblMensaje {\n"
"    color: #1e73f1;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLabel#lblNota {\n"
"    color: #666666;\n"
"    font-size: 9pt;\n"
"}\n"
"   ", None))
        self.lblTitulo.setText(QCoreApplication.translate("ProcessDialog", u"Generando Reporte de Ventas", None))
        self.lblSubtitulo.setText(QCoreApplication.translate("ProcessDialog", u"Procesando orden 1 de N...", None))
        self.label.setText(QCoreApplication.translate("ProcessDialog", u"Detalles del progreso:", None))
        self.lblMensaje.setText(QCoreApplication.translate("ProcessDialog", u"Por favor espere mientras se procesa la informaci\u00f3n...", None))
        self.btnCancelar.setText(QCoreApplication.translate("ProcessDialog", u"Cancelar", None))
        self.lblNota.setText(QCoreApplication.translate("ProcessDialog", u"Nota: Esta operaci\u00f3n puede tomar varios minutos dependiendo de la cantidad de datos.", None))
    # retranslateUi

