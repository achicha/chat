"""файл для запуска клиентского приложения в цикле"""
import argparse
import asyncio
import sys
import os

from PyQt5 import Qt, QtWidgets

from aclient import ChatClientProtocol
from views.windows import LoginWindow, ContactsWindow
from config import DB_PATH
from database.controller import ClientMessages
from database.models import CBase
from quamash import QEventLoop

# # create Application
# app = Qt.QApplication(sys.argv)
#
# # login into account
# login_wnd = LoginWindow()
#
# if login_wnd.exec_() == QtWidgets.QDialog.Accepted:
#     # show user's contacts if login was correct
#     contacts_wnd = ContactsWindow(db_path=DB_PATH, user_name=login_wnd.username)
#
#     #cm = ClientMessages(db_path, CBase, echo=False)
#
#     contacts_wnd.show()
#     sys.exit(app.exec_())


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
            wnd = ContactsWindow(server_instance=_client, user_name=login_wnd.username)
            wnd.show()

            with loop:
                # connect to our server
                coro = loop.create_connection(lambda: _client, self.args["addr"], self.args["port"])
                server = loop.run_until_complete(coro)

                # GUI or Console client
                if self.args["gui"]:
                    asyncio.ensure_future(_client.getmsgs(loop))
                else:
                    asyncio.ensure_future(_client.getgui(loop))

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
    parser.add_argument("--port", default=50000, type=int)
    parser.add_argument("--gui", default=True, type=bool)
    args = vars(parser.parse_args())
    return args


a = GuiClientApp(parse_args(), DB_PATH)
a.main()
