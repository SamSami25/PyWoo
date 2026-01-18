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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QWidget)

class Ui_Dialog_urlWoocommerce(object):
    def setupUi(self, Dialog_urlWoocommerce):
        if not Dialog_urlWoocommerce.objectName():
            Dialog_urlWoocommerce.setObjectName(u"Dialog_urlWoocommerce")
        Dialog_urlWoocommerce.resize(552, 335)
        Dialog_urlWoocommerce.setStyleSheet(u"")
        self.lb_nombre = QLabel(Dialog_urlWoocommerce)
        self.lb_nombre.setObjectName(u"lb_nombre")
        self.lb_nombre.setGeometry(QRect(10, 10, 531, 51))
        self.lb_nombre.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 87 12pt \"Arial Black\"\n"
"border-radius: 10px; \n"
"padding: 8px 12px;")
        self.lb_nombre.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.lb_fondoblanco = QLabel(Dialog_urlWoocommerce)
        self.lb_fondoblanco.setObjectName(u"lb_fondoblanco")
        self.lb_fondoblanco.setGeometry(QRect(10, 70, 529, 171))
        self.lb_fondoblanco.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.pbt_guardar = QPushButton(Dialog_urlWoocommerce)
        self.pbt_guardar.setObjectName(u"pbt_guardar")
        self.pbt_guardar.setGeometry(QRect(30, 250, 100, 31))
        self.pbt_guardar.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.pbt_conexion = QPushButton(Dialog_urlWoocommerce)
        self.pbt_conexion.setObjectName(u"pbt_conexion")
        self.pbt_conexion.setGeometry(QRect(180, 250, 172, 31))
        self.pbt_conexion.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.pbt_salir = QPushButton(Dialog_urlWoocommerce)
        self.pbt_salir.setObjectName(u"pbt_salir")
        self.pbt_salir.setGeometry(QRect(410, 250, 100, 31))
        self.pbt_salir.setStyleSheet(u"background-color: rgb(28, 115, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial Black\";\n"
"border-radius: 8px;\n"
"padding: 6px 12px;")
        self.lb_blancocomentario = QLabel(Dialog_urlWoocommerce)
        self.lb_blancocomentario.setObjectName(u"lb_blancocomentario")
        self.lb_blancocomentario.setGeometry(QRect(10, 290, 529, 31))
        self.lb_blancocomentario.setStyleSheet(u"background-color: qlineargradient(spread:pad, x1:0.6875, y1:0.216, x2:1, y2:0, stop:1 rgba(255, 255, 255, 255));\n"
"border-radius: 9px;\n"
"padding: 10px 12px;\n"
"\n"
"")
        self.lnEdit_url = QLineEdit(Dialog_urlWoocommerce)
        self.lnEdit_url.setObjectName(u"lnEdit_url")
        self.lnEdit_url.setGeometry(QRect(150, 100, 351, 21))
        font = QFont()
        font.setFamilies([u"Consolas"])
        font.setPointSize(10)
        self.lnEdit_url.setFont(font)
        self.lb_url = QLabel(Dialog_urlWoocommerce)
        self.lb_url.setObjectName(u"lb_url")
        self.lb_url.setGeometry(QRect(40, 100, 61, 20))
        self.lb_url.setStyleSheet(u"font: 9pt \"Arial\";")
        self.lb_url.setTextFormat(Qt.PlainText)
        self.lb_csecret = QLabel(Dialog_urlWoocommerce)
        self.lb_csecret.setObjectName(u"lb_csecret")
        self.lb_csecret.setGeometry(QRect(40, 180, 101, 20))
        self.lb_csecret.setStyleSheet(u"font: 9pt \"Arial\";")
        self.lnEdit_cs = QLineEdit(Dialog_urlWoocommerce)
        self.lnEdit_cs.setObjectName(u"lnEdit_cs")
        self.lnEdit_cs.setGeometry(QRect(150, 180, 351, 20))
        self.lnEdit_cs.setFont(font)
        self.lb_ckey = QLabel(Dialog_urlWoocommerce)
        self.lb_ckey.setObjectName(u"lb_ckey")
        self.lb_ckey.setGeometry(QRect(40, 140, 91, 20))
        self.lb_ckey.setStyleSheet(u"font: 9pt \"Arial\";")
        self.lnEdit_ck = QLineEdit(Dialog_urlWoocommerce)
        self.lnEdit_ck.setObjectName(u"lnEdit_ck")
        self.lnEdit_ck.setGeometry(QRect(150, 140, 351, 20))
        self.lnEdit_ck.setFont(font)

        self.retranslateUi(Dialog_urlWoocommerce)

        QMetaObject.connectSlotsByName(Dialog_urlWoocommerce)
    # setupUi

    def retranslateUi(self, Dialog_urlWoocommerce):
        Dialog_urlWoocommerce.setWindowTitle(QCoreApplication.translate("Dialog_urlWoocommerce", u"Dialog", None))
        self.lb_nombre.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Credenciales API WooCommerce", None))
        self.lb_fondoblanco.setText("")
        self.pbt_guardar.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Guardar", None))
        self.pbt_conexion.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Probar Conexi\u00f3n", None))
        self.pbt_salir.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Salir", None))
        self.lb_blancocomentario.setText("")
        self.lnEdit_url.setPlaceholderText(QCoreApplication.translate("Dialog_urlWoocommerce", u"https://e-commerce.com", None))
        self.lb_url.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"URL", None))
        self.lb_csecret.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Consumer Secret ", None))
        self.lnEdit_cs.setPlaceholderText(QCoreApplication.translate("Dialog_urlWoocommerce", u"cs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", None))
        self.lb_ckey.setText(QCoreApplication.translate("Dialog_urlWoocommerce", u"Consumer Key ", None))
        self.lnEdit_ck.setPlaceholderText(QCoreApplication.translate("Dialog_urlWoocommerce", u"ck_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", None))
    # retranslateUi

