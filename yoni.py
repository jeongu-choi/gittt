# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'yoniuHxiop.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QRadioButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(765, 600)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"background:rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.H_beam = QRadioButton(self.centralwidget)
        self.H_beam.setObjectName(u"H_beam")
        self.H_beam.setGeometry(QRect(100, 340, 56, 20))
        self.H_beam.setStyleSheet(u"QRadioButton::indicator {\n"
"    background-color: lightblue;\n"
"    border: 1px solid black;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: black;\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: black; /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    background: none; /* \ubc30\uacbd\uc0c9 \uc81c\uac70 */\n"
"    border: none; /* \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"}\n"
"")
        self.H_beam.setChecked(False)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(110, 140, 91, 41))
        self.label_2.setStyleSheet(u"\n"
"font : 15pt ;\n"
"color : black;\n"
"")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(24, 342, 71, 16))
        self.label_5.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"font : 11pt ;\n"
"color : black;\n"
"font-weight: bold")
        self.Load = QLineEdit(self.centralwidget)
        self.Load.setObjectName(u"Load")
        self.Load.setGeometry(QRect(210, 140, 531, 41))
        self.Load.setStyleSheet(u"background-color: rgb(208, 208, 208);\n"
"font : 10pt ;\n"
"color : black")
        self.Load.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(110, 220, 91, 31))
        self.label.setStyleSheet(u"\n"
"font : 15pt ;\n"
"color : black")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Bridge_Length = QLineEdit(self.centralwidget)
        self.Bridge_Length.setObjectName(u"Bridge_Length")
        self.Bridge_Length.setGeometry(QRect(210, 210, 531, 41))
        self.Bridge_Length.setStyleSheet(u"background-color: rgb(208, 208, 208);\n"
"font : 10pt ;\n"
"color : black")
        self.Bridge_Length.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.I_beam = QRadioButton(self.centralwidget)
        self.I_beam.setObjectName(u"I_beam")
        self.I_beam.setGeometry(QRect(160, 340, 50, 20))
        self.I_beam.setStyleSheet(u"QRadioButton::indicator {\n"
"    background-color: lightblue;\n"
"    border: 1px solid black;\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 7px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked {\n"
"    background-color: green;\n"
"}\n"
"\n"
"QRadioButton {\n"
"    color: black; /* \ud14d\uc2a4\ud2b8 \uc0c9\uc0c1 \ubcc0\uacbd */\n"
"    background: none; /* \ubc30\uacbd\uc0c9 \uc81c\uac70 */\n"
"    border: none; /* \ud14c\ub450\ub9ac \uc81c\uac70 */\n"
"}\n"
"")
        self.I_beam.setChecked(True)
        self.pixmap = QLabel(self.centralwidget)
        self.pixmap.setObjectName(u"pixmap")
        self.pixmap.setGeometry(QRect(20, 370, 181, 141))
        self.pixmap.setStyleSheet(u"")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(40, 30, 151, 61))
        self.label_6.setStyleSheet(u"font: 18pt \"\ub9d1\uc740 \uace0\ub515\";\n"
"color:black;\n"
"border: 3px dashed rgb(106, 76, 255)")
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(220, 30, 511, 61))
        self.label_7.setStyleSheet(u"font: 26pt \"\ub9d1\uc740 \uace0\ub515\";\n"
"color:black;\n"
"border: 3px dashed rgb(106, 76, 255)")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warren_truss = QLabel(self.centralwidget)
        self.warren_truss.setObjectName(u"warren_truss")
        self.warren_truss.setGeometry(QRect(240, 310, 461, 241))
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 320, 211, 201))
        self.label_12.setStyleSheet(u"background-color: rgb(255, 255, 255)")
        MainWindow.setCentralWidget(self.centralwidget)
        self.label_12.raise_()
        self.H_beam.raise_()
        self.label_2.raise_()
        self.label_5.raise_()
        self.Load.raise_()
        self.label.raise_()
        self.Bridge_Length.raise_()
        self.I_beam.raise_()
        self.pixmap.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.warren_truss.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 765, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.H_beam.setText(QCoreApplication.translate("MainWindow", u" H \ube54", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\uad50\ub7c9\uae38\uc774", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\ubd80\uc7ac\uc885\ub958", None))
        self.Load.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\ud558\uc911", None))
        self.Bridge_Length.setText("")
        self.I_beam.setText(QCoreApplication.translate("MainWindow", u" I \ube54", None))
        self.pixmap.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"IC-PBL", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Truss \uad6c\uc870\uc124\uacc4", None))
        self.warren_truss.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

