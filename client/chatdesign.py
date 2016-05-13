# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chatdesign.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(459, 374)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.hamTab = QtGui.QWidget()
        self.hamTab.setObjectName(_fromUtf8("hamTab"))
        self.gridLayout = QtGui.QGridLayout(self.hamTab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidget = QtGui.QListWidget(self.hamTab)
        self.listWidget.setMaximumSize(QtCore.QSize(450, 300))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.gridLayout.addWidget(self.listWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.hamTab, _fromUtf8(""))
        self.spamTab = QtGui.QWidget()
        self.spamTab.setObjectName(_fromUtf8("spamTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.spamTab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.listWidget_Spam = QtGui.QListWidget(self.spamTab)
        self.listWidget_Spam.setObjectName(_fromUtf8("listWidget_Spam"))
        self.gridLayout_2.addWidget(self.listWidget_Spam, 0, 0, 1, 1)
        self.tabWidget.addTab(self.spamTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "True messenger", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.hamTab), _translate("MainWindow", "Conversation", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spamTab), _translate("MainWindow", "Spam Inbox", None))
        self.pushButton.setText(_translate("MainWindow", "Send", None))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p>To inform the app of incorrect classification, choose the message </p><p>and click this button:</p></body></html>", None))
        self.pushButton_2.setText(_translate("MainWindow", "Correct classification", None))

