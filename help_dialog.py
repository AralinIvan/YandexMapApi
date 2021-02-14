# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(260, 170)
        Dialog.setStyleSheet("background-color: rgb(66, 66, 66);")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(230, 10, 18, 18))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.pushButton.setStyleSheet("QPushButton {\n"
"    background-color: rgb(255, 0, 0);\n"
"    border: 2px solid rgb(37, 39, 48);\n"
"    border-radius: 9px;\n"
"    color: #FFF;\n"
"    padding-left: 1px;\n"
"    padding-right: 1px;}\n"
"QPushButton:hover {background-color: rgb(170, 0, 0) }\n"
"QPushButton:hover:pressed {background-color: rgb(150, 150, 150)}")
        self.pushButton.setText("")
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setObjectName("pushButton")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 5, 240, 160))
        self.textBrowser.setStyleSheet("border: 1px solid rgb(37, 39, 48) ;\n"
"border-radius: 10px;\n"
"color: #FFF;\n"
"padding-left: 10px;\n"
"padding-right: 10px;\n"
"background-color: rgb(34, 36, 44);\n"
"")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.raise_()
        self.pushButton.raise_()
        self.pushButton.clicked.connect(self.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Все вводы производятся в градуссах</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Формат ввода:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Долгота - 111.11111</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Широта - 11.11111</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Масштаб - 11.11111, 11.11111</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Максимальные и минимальные значения:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Долгота - 179, -179</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Широта - 88, -88</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Максимальные значения:</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Масштаб(1) - 180</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Масштаб(2) - 90</p></body></html>"))