# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'server_monitor.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ServerWindow(object):
    def setupUi(self, ServerWindow):
        ServerWindow.setObjectName("ServerWindow")
        ServerWindow.resize(801, 496)
        self.centralwidget = QtWidgets.QWidget(ServerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidgetClients = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetClients.setObjectName("tabWidgetClients")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.clients_list = QtWidgets.QListWidget(self.tab)
        self.clients_list.setObjectName("clients_list")
        self.gridLayout_3.addWidget(self.clients_list, 0, 0, 1, 1)
        self.tabWidgetClients.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.msg_history_list = QtWidgets.QListWidget(self.tab_2)
        self.msg_history_list.setObjectName("msg_history_list")
        self.gridLayout.addWidget(self.msg_history_list, 0, 0, 1, 1)
        self.tabWidgetClients.addTab(self.tab_2, "")
        self.gridLayout_2.addWidget(self.tabWidgetClients, 0, 0, 1, 1)
        ServerWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ServerWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 22))
        self.menubar.setObjectName("menubar")
        self.menuactions = QtWidgets.QMenu(self.menubar)
        self.menuactions.setObjectName("menuactions")
        ServerWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ServerWindow)
        self.statusbar.setObjectName("statusbar")
        ServerWindow.setStatusBar(self.statusbar)
        self.refresh_action = QtWidgets.QAction(ServerWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../Downloads/if_sync_126579.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_action.setIcon(icon)
        self.refresh_action.setObjectName("refresh_action")
        self.menuactions.addAction(self.refresh_action)
        self.menubar.addAction(self.menuactions.menuAction())

        self.retranslateUi(ServerWindow)
        self.tabWidgetClients.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ServerWindow)

    def retranslateUi(self, ServerWindow):
        _translate = QtCore.QCoreApplication.translate
        ServerWindow.setWindowTitle(_translate("ServerWindow", "Server Monitoring"))
        self.tabWidgetClients.setTabText(self.tabWidgetClients.indexOf(self.tab), _translate("ServerWindow", "Клиенты"))
        self.tabWidgetClients.setTabText(self.tabWidgetClients.indexOf(self.tab_2), _translate("ServerWindow", "История соединений"))
        self.menuactions.setTitle(_translate("ServerWindow", "actions"))
        self.refresh_action.setText(_translate("ServerWindow", "refresh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ServerWindow = QtWidgets.QMainWindow()
    ui = Ui_ServerWindow()
    ui.setupUi(ServerWindow)
    ServerWindow.show()
    sys.exit(app.exec_())

