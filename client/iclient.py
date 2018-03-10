"""файл для запуска клиентского приложения в цикле"""
import argparse
import asyncio
import signal
import sys

import time
from PyQt5 import Qt
#from PyQt5.QtCore import QEventLoop
from quamash import QEventLoop  # asyncio works fine with pyqt5 loop

from client.client_proto import ChatClientProtocol
from client.ui.windows import LoginWindow, ContactsWindow
from client.client_config import DB_PATH, PORT


class ConsoleClientApp:
    """Console Client"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame), loop.stop)

        # ask about login/password
        usr = input('username: ')
        passwrd = input('password: ')
        tasks = []

        _client = ChatClientProtocol(db_path=self.db_path,
                                     loop=loop,
                                     tasks=tasks,
                                     username=usr or self.args["user"],
                                     password=passwrd or self.args["password"])
        coro = loop.create_connection(lambda: _client, self.args["addr"], self.args["port"])
        transport, protocol = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C
        try:
            task = asyncio.ensure_future(_client.get_from_console())  # create Task from coroutine
            tasks.append(task)
            loop.run_until_complete(task)

        except KeyboardInterrupt:
            pass
        except Exception as e:
            # todo need to destroy get_from_console task somehow
            print(e)

        finally:
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

        # Each client will create a new protocol instance
        auth = []
        _client = ChatClientProtocol(self.db_path, loop, authenticated=auth)

        # create Contacts window
        wnd = ContactsWindow(client_instance=_client)
        _client.gui_instance = wnd  # reference from protocol to GUI, for msg update

        # login into account
        login_wnd = LoginWindow()
        #login_wnd.show()
        #if login_wnd.exec_() == QtWidgets.QDialog.Accepted:
        #wnd.show()
        login_wnd.exec_()

        with loop:
            # connect to our server
            coro = loop.create_connection(lambda: _client, self.args["addr"], self.args["port"])
            server = loop.run_until_complete(coro)

            # auth
            _client.user = login_wnd.username
            _client.password = login_wnd.password
            _client.send_auth(_client.user, login_wnd.password)
            time.sleep(3)

            from sys import stdout
            stdout.write(str(wnd.is_auth))
            stdout.write(str(_client.gui_instance.is_auth))
            stdout.write(str(_client.user))

            # start GUI client
            wnd.show()
            _client.get_from_gui()  #asyncio.ensure_future(_client.get_from_gui(loop))

            # Serve requests until Ctrl+C
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass

            #loop.run_until_complete(server.wait_closed())


            # else:
            #     print('wrong users credentials')


def parse_args():
    parser = argparse.ArgumentParser(description="Client settings")
    parser.add_argument("--user", default="user1", type=str)
    parser.add_argument("--password", default="123", type=str)
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
