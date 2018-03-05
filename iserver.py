"""файл для запуска серверного приложения в цикле"""
# import sys
# import os
# from PyQt5 import Qt, QtWidgets
#
#
# from views.windows import ServerMonitorWindow
# from config import DB_PATH

# # create Application
# app = Qt.QApplication(sys.argv)
#
# # start server
# server_wnd = ServerMonitorWindow(db_path=DB_PATH)
#
# server_wnd.show()
# sys.exit(app.exec_())


import argparse
import asyncio
import sys
#from PyQt5.QtCore import QEventLoop
from quamash import QEventLoop
from PyQt5 import Qt, QtWidgets

from config import DB_PATH
from views.server_monitor_ui import Ui_ServerWindow as server_ui_class
from aserver import ChatServerProtocol
from views.windows import ServerMonitorWindow


class GuiApp:
    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()

        # Each client will create a new protocol instance
        self.ins = ChatServerProtocol(self.db_path, connections, users)

        # GUI
        app = Qt.QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)  # NEW must set the event loop

        wnd = ServerMonitorWindow(server_instance=self.ins, parsed_args=self.args, db_path=self.db_path)
        wnd.show()

        with loop:
            coro = loop.create_server(lambda: self.ins, self.args["addr"], self.args["port"])
            server = loop.run_until_complete(coro)

            # Serve requests until Ctrl+C
            print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass

            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Server settings")
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    args = vars(parser.parse_args())
    return args


a = GuiApp(parse_args(), DB_PATH)
a.main()

