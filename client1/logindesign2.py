# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logindesign.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(497, 259)
        Dialog.setToolTip(_fromUtf8(""))
        Dialog.setStatusTip(_fromUtf8(""))
        Dialog.setWhatsThis(_fromUtf8(""))
        Dialog.setAccessibleName(_fromUtf8(""))
        Dialog.setAccessibleDescription(_fromUtf8(""))
        Dialog.setModal(True)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(110, 140, 101, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.userName = QtGui.QLineEdit(Dialog)
        self.userName.setGeometry(QtCore.QRect(240, 140, 133, 20))
        self.userName.setObjectName(_fromUtf8("userName"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 200, 156, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 0, 451, 131))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "TrueMessenger", None))
        self.label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Enter username</span></p></body></html>", None))
        self.userName.setPlaceholderText(_translate("Dialog", "Enter username here", None))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Welcome to TrueMessenger!</span></p><p><span style=\" font-size:9pt;\">TrueMessenger is a different take on the classical messenger app. TrueMessenger:<br/></span></p>\n"
"<ul>\n"
"<li>Marks suspicious incoming messages as spam \n"
"<li>Allows the user to inform the app when it has failed to correctly classify the message \n"
"</ul>\n"
"\n"
"\n"
"", None))

