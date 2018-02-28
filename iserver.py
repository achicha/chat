"""файл для запуска серверного приложения в цикле"""
import sys
import os

from PyQt5 import Qt, QtWidgets

from views.windows import ServerMonitorWindow
from config import DB_PATH

# create Application
app = Qt.QApplication(sys.argv)

# start server
server_wnd = ServerMonitorWindow(db_path=DB_PATH)

server_wnd.show()
sys.exit(app.exec_())
