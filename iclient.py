"""файл для запуска клиентского приложения в цикле"""
import sys
import os

from PyQt5 import Qt, QtWidgets

from views.windows import LoginWindow, ContactsWindow
from config import DB_PATH
from database.controller import ClientMessages
from database.models import CBase

# create Application
app = Qt.QApplication(sys.argv)

# login into account
login_wnd = LoginWindow()

if login_wnd.exec_() == QtWidgets.QDialog.Accepted:
    # show user's contacts if login was correct
    contacts_wnd = ContactsWindow(db_path=DB_PATH, user_name=login_wnd.username)

    #cm = ClientMessages(db_path, CBase, echo=False)

    contacts_wnd.show()
    sys.exit(app.exec_())
