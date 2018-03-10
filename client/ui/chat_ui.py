# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChatMainWindow(object):
    def setupUi(self, ChatMainWindow):
        ChatMainWindow.setObjectName("ChatMainWindow")
        ChatMainWindow.resize(462, 386)
        self.centralwidget = QtWidgets.QWidget(ChatMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.chat_window = QtWidgets.QListWidget(self.centralwidget)
        self.chat_window.setObjectName("chat_window")
        self.verticalLayout.addWidget(self.chat_window)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.send_text = QtWidgets.QLineEdit(self.centralwidget)
        self.send_text.setObjectName("send_text")
        self.horizontalLayout.addWidget(self.send_text)
        self.send_btn = QtWidgets.QPushButton(self.centralwidget)
        self.send_btn.setObjectName("send_btn")
        self.horizontalLayout.addWidget(self.send_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        ChatMainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ChatMainWindow)
        self.statusbar.setObjectName("statusbar")
        ChatMainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ChatMainWindow)
        QtCore.QMetaObject.connectSlotsByName(ChatMainWindow)

    def retranslateUi(self, ChatMainWindow):
        _translate = QtCore.QCoreApplication.translate
        ChatMainWindow.setWindowTitle(_translate("ChatMainWindow", "Chat Window"))
        self.send_btn.setText(_translate("ChatMainWindow", "Send"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ChatMainWindow = QtWidgets.QMainWindow()
    ui = Ui_ChatMainWindow()
    ui.setupUi(ChatMainWindow)
    ChatMainWindow.show()
    sys.exit(app.exec_())

