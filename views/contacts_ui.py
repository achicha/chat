# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contacts.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ContactsWindow(object):
    def setupUi(self, ContactsWindow):
        ContactsWindow.setObjectName("ContactsWindow")
        ContactsWindow.resize(295, 508)
        self.centralwidget = QtWidgets.QWidget(ContactsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.all_contacts = QtWidgets.QListWidget(self.centralwidget)
        self.all_contacts.setObjectName("all_contacts")
        self.verticalLayout.addWidget(self.all_contacts)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.new_contact_name = QtWidgets.QLineEdit(self.centralwidget)
        self.new_contact_name.setObjectName("new_contact_name")
        self.horizontalLayout_2.addWidget(self.new_contact_name)
        self.add_new_contact_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_new_contact_btn.setObjectName("add_new_contact_btn")
        self.horizontalLayout_2.addWidget(self.add_new_contact_btn)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.delete_contact_btn = QtWidgets.QPushButton(self.centralwidget)
        self.delete_contact_btn.setObjectName("delete_contact_btn")
        self.verticalLayout.addWidget(self.delete_contact_btn)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        ContactsWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ContactsWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 295, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        ContactsWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ContactsWindow)
        self.statusbar.setObjectName("statusbar")
        ContactsWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(ContactsWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(ContactsWindow)
        QtCore.QMetaObject.connectSlotsByName(ContactsWindow)

    def retranslateUi(self, ContactsWindow):
        _translate = QtCore.QCoreApplication.translate
        ContactsWindow.setWindowTitle(_translate("ContactsWindow", "My Contacts"))
        self.label.setText(_translate("ContactsWindow", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; color:#729fcf;\">All Contacts</span></p></body></html>"))
        self.add_new_contact_btn.setText(_translate("ContactsWindow", "Add Contact"))
        self.delete_contact_btn.setText(_translate("ContactsWindow", "Delete Contact"))
        self.menuFile.setTitle(_translate("ContactsWindow", "File"))
        self.actionExit.setText(_translate("ContactsWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ContactsWindow = QtWidgets.QMainWindow()
    ui = Ui_ContactsWindow()
    ui.setupUi(ContactsWindow)
    ContactsWindow.show()
    sys.exit(app.exec_())

