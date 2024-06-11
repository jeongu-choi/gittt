# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'secondwindowFaaUsE.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)
from PyQt5 import uic

form_class = uic.loadUiType("secondwindow.ui")[0]

class Ui_Form(form_class):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(383, 650)
        icon = QIcon()
        icon.addFile(u"gost.jpg", QSize(), QIcon.Normal, QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet(u"background:rgb(255, 255, 255);")
        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(0, 0, 151, 651))
        self.tableWidget.setStyleSheet(u"background:rgb(173, 173, 173)")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 0, 231, 651))
        self.label.setStyleSheet(u"border: 3px dashed rgb(255, 0, 0);\n"
"font : 15pt ;\n"
"color : black;\n"
"")

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"H_beam_table", None))
        self.label.setText(QCoreApplication.translate("Form", u"\uc140\uc744 \ub354\ube14\ud074\ub9ad \ud558\uc138\uc694!", None))
    # retranslateUi

