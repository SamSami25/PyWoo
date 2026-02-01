# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_credenciales_api.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QFormLayout,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import iconos_rc

class Ui_CredencialesApiWoo(object):
    def setupUi(self, CredencialesApiWoo):
        if not CredencialesApiWoo.objectName():
            CredencialesApiWoo.setObjectName(u"CredencialesApiWoo")
        CredencialesApiWoo.resize(720, 420)
        icon = QIcon()
        icon.addFile(u":/assets/icons/actualizar.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        CredencialesApiWoo.setWindowIcon(icon)
        self.verticalLayout_main = QVBoxLayout(CredencialesApiWoo)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.labelTitulo = QLabel(CredencialesApiWoo)
        self.labelTitulo.setObjectName(u"labelTitulo")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.labelTitulo.setFont(font)
        self.labelTitulo.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.labelTitulo)

        self.checkCredencialesCargadas = QCheckBox(CredencialesApiWoo)
        self.checkCredencialesCargadas.setObjectName(u"checkCredencialesCargadas")
        self.checkCredencialesCargadas.setEnabled(False)
        self.checkCredencialesCargadas.setChecked(True)

        self.verticalLayout_main.addWidget(self.checkCredencialesCargadas)

        self.line = QFrame(CredencialesApiWoo)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout_main.addWidget(self.line)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(14)
        self.labelStoreUrl = QLabel(CredencialesApiWoo)
        self.labelStoreUrl.setObjectName(u"labelStoreUrl")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labelStoreUrl)

        self.lineEditStoreUrl = QLineEdit(CredencialesApiWoo)
        self.lineEditStoreUrl.setObjectName(u"lineEditStoreUrl")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEditStoreUrl)

        self.labelConsumerKey = QLabel(CredencialesApiWoo)
        self.labelConsumerKey.setObjectName(u"labelConsumerKey")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labelConsumerKey)

        self.lineEditConsumerKey = QLineEdit(CredencialesApiWoo)
        self.lineEditConsumerKey.setObjectName(u"lineEditConsumerKey")
        self.lineEditConsumerKey.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEditConsumerKey)

        self.labelConsumerSecret = QLabel(CredencialesApiWoo)
        self.labelConsumerSecret.setObjectName(u"labelConsumerSecret")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.labelConsumerSecret)

        self.lineEditConsumerSecret = QLineEdit(CredencialesApiWoo)
        self.lineEditConsumerSecret.setObjectName(u"lineEditConsumerSecret")
        self.lineEditConsumerSecret.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEditConsumerSecret)


        self.verticalLayout_main.addLayout(self.formLayout)

        self.checkVerCredenciales = QCheckBox(CredencialesApiWoo)
        self.checkVerCredenciales.setObjectName(u"checkVerCredenciales")

        self.verticalLayout_main.addWidget(self.checkVerCredenciales)

        self.horizontalLayoutButtons = QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName(u"horizontalLayoutButtons")
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayoutButtons.addItem(self.spacerItem)

        self.btnProbarConexion = QPushButton(CredencialesApiWoo)
        self.btnProbarConexion.setObjectName(u"btnProbarConexion")

        self.horizontalLayoutButtons.addWidget(self.btnProbarConexion)

        self.btnCerrar = QPushButton(CredencialesApiWoo)
        self.btnCerrar.setObjectName(u"btnCerrar")

        self.horizontalLayoutButtons.addWidget(self.btnCerrar)

        self.btnGuardar = QPushButton(CredencialesApiWoo)
        self.btnGuardar.setObjectName(u"btnGuardar")

        self.horizontalLayoutButtons.addWidget(self.btnGuardar)


        self.verticalLayout_main.addLayout(self.horizontalLayoutButtons)


        self.retranslateUi(CredencialesApiWoo)

        QMetaObject.connectSlotsByName(CredencialesApiWoo)
    # setupUi

    def retranslateUi(self, CredencialesApiWoo):
        CredencialesApiWoo.setWindowTitle(QCoreApplication.translate("CredencialesApiWoo", u"Credenciales API WooCommerce", None))
        CredencialesApiWoo.setStyleSheet(QCoreApplication.translate("CredencialesApiWoo", u"\n"
"QDialog {\n"
"    background-color: #ffffff;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #222222;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #cfd8dc;\n"
"    border-radius: 6px;\n"
"    padding: 6px 8px;\n"
"    background-color: #ffffff;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #2979ff;\n"
"}\n"
"\n"
"QCheckBox {\n"
"    spacing: 6px;\n"
"}\n"
"\n"
"/* ---------- BOTONES (BASE) ---------- */\n"
"QPushButton {\n"
"    border-radius: 8px;\n"
"    padding: 6px 16px;\n"
"    font-weight: bold;\n"
"    color: white;\n"
"}\n"
"\n"
"/* BOT\u00d3N PRIMARIO - GUARDAR */\n"
"QPushButton#btnGuardar {\n"
"    background-color: #1e73f1;\n"
"}\n"
"QPushButton#btnGuardar:hover {\n"
"    background-color: #1558c0;\n"
"}\n"
"QPushButton#btnGuardar:pressed {\n"
"    background-color: #0d47a1;\n"
"}\n"
"\n"
"/* BOT\u00d3N SECUNDARIO - PROBAR */\n"
"QPushButton#btnProbarConexion {\n"
"    background-color: #90caf9;\n"
"    color: #0d47a1;\n"
""
                        "}\n"
"QPushButton#btnProbarConexion:hover {\n"
"    background-color: #64b5f6;\n"
"}\n"
"QPushButton#btnProbarConexion:pressed {\n"
"    background-color: #42a5f5;\n"
"}\n"
"\n"
"/* BOT\u00d3N CERRAR */\n"
"QPushButton#btnCerrar {\n"
"    background-color: #9e9e9e;\n"
"}\n"
"QPushButton#btnCerrar:hover {\n"
"    background-color: #757575;\n"
"}\n"
"QPushButton#btnCerrar:pressed {\n"
"    background-color: #616161;\n"
"}\n"
"\n"
"/* ---------- SEPARADOR ---------- */\n"
"QFrame#line {\n"
"    color: #e0e0e0;\n"
"}\n"
"   ", None))
        self.labelTitulo.setStyleSheet(QCoreApplication.translate("CredencialesApiWoo", u"\n"
"background-color: #1e73f1;\n"
"color: white;\n"
"padding: 10px;\n"
"border-radius: 8px;\n"
"      ", None))
        self.labelTitulo.setText(QCoreApplication.translate("CredencialesApiWoo", u"WooCommerce \u2013 Credenciales API", None))
        self.checkCredencialesCargadas.setText(QCoreApplication.translate("CredencialesApiWoo", u"Credenciales cargadas.", None))
        self.labelStoreUrl.setText(QCoreApplication.translate("CredencialesApiWoo", u"E-COMMERCE URL", None))
        self.lineEditStoreUrl.setPlaceholderText(QCoreApplication.translate("CredencialesApiWoo", u"https://e-commerce.com", None))
        self.labelConsumerKey.setText(QCoreApplication.translate("CredencialesApiWoo", u"Consumer Key", None))
        self.lineEditConsumerKey.setPlaceholderText(QCoreApplication.translate("CredencialesApiWoo", u"ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", None))
        self.labelConsumerSecret.setText(QCoreApplication.translate("CredencialesApiWoo", u"Consumer Secret", None))
        self.lineEditConsumerSecret.setPlaceholderText(QCoreApplication.translate("CredencialesApiWoo", u"cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", None))
        self.checkVerCredenciales.setText(QCoreApplication.translate("CredencialesApiWoo", u"Ver credenciales", None))
        self.btnProbarConexion.setText(QCoreApplication.translate("CredencialesApiWoo", u"Probar conexi\u00f3n", None))
        self.btnCerrar.setText(QCoreApplication.translate("CredencialesApiWoo", u"Cerrar", None))
        self.btnGuardar.setText(QCoreApplication.translate("CredencialesApiWoo", u"Guardar", None))
    # retranslateUi

