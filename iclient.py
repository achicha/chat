"""файл для запуска клиентского приложения в цикле"""
import argparse
import asyncio
import sys

from PyQt5 import Qt, QtWidgets
#from PyQt5.QtCore import QEventLoop
from quamash import QEventLoop  # asyncio works fine with pyqt5 loop

from protocols.client_proto import ChatClientProtocol
from gui_views.windows import LoginWindow, ContactsWindow
from config import DB_PATH, PORT


class ConsoleClientApp:
    """Console Client"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        loop = asyncio.get_event_loop()
        _client = ChatClientProtocol(db_path=self.db_path, loop=loop, user=self.args["user"])
        coro = loop.create_connection(lambda: _client, self.args["addr"], self.args["port"])
        server = loop.run_until_complete(coro)

        asyncio.ensure_future(_client.getmsgs(loop))
        # Serve requests until Ctrl+C
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            loop.close()

        loop.close()


class GuiClientApp:
    """GUI Client"""
    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):

        # event loop
        app = Qt.QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)  # NEW must set the event loop

        # login into account
        login_wnd = LoginWindow()
        if login_wnd.exec_() == QtWidgets.QDialog.Accepted:

            # Each client will create a new protocol instance
            _client = ChatClientProtocol(self.db_path, loop, login_wnd.username)

            # create Contacts window
            wnd = ContactsWindow(client_instance=_client, user_name=login_wnd.username)
            _client.gui_instance = wnd  # reference from protocol to GUI, for msg update

            wnd.show()

            with loop:
                # connect to our server
                coro = loop.create_connection(lambda: _client, self.args["addr"], self.args["port"])
                server = loop.run_until_complete(coro)

                # start GUI client
                asyncio.ensure_future(_client.getmsgs(loop))

                # Serve requests until Ctrl+C
                try:
                    loop.run_forever()
                except KeyboardInterrupt:
                    loop.close()

                #loop.run_until_complete(server.wait_closed())
                loop.close()


def parse_args():
    parser = argparse.ArgumentParser(description="Client settings")
    parser.add_argument("--user", default="user_2", type=str)
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=PORT, type=int)
    parser.add_argument('--nogui', action='store_true')
    return vars(parser.parse_args())


args = parse_args()

if args['nogui']:
    # start consoles server
    a = ConsoleClientApp(args, DB_PATH)
    a.main()
else:
    # start GUI client
    a = GuiClientApp(args, DB_PATH)
    a.main()
