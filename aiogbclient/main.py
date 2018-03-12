"""файл для запуска клиентского приложения в цикле"""
import argparse
import asyncio
import signal
import sys

from PyQt5 import Qt, QtWidgets
#from PyQt5.QtCore import QEventLoop
from quamash import QEventLoop  # asyncio works fine with pyqt5 loop

from aiogbclient.utils.client_proto import ChatClientProtocol, ClientAuth
from aiogbclient.ui.windows import LoginWindow, ContactsWindow
from aiogbclient.client_config import DB_PATH, PORT


class ConsoleClientApp:
    """Console Client"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        # create event loop
        loop = asyncio.get_event_loop()
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame), loop.stop)

        # authentication process
        auth = ClientAuth(db_path=self.db_path)
        while True:
            usr = self.args["user"] or input('username: ')
            passwrd = self.args["password"] or input('password: ')
            auth.username = usr
            auth.password = passwrd
            is_auth = auth.authenticate()
            if is_auth:
                break
            else:
                print('wrong username/password')

        # Each client will create a new protocol instance
        tasks = []
        client_ = ChatClientProtocol(db_path=self.db_path,
                                     loop=loop,
                                     tasks=tasks,
                                     username=usr,
                                     password=passwrd)
        # connect to our server
        try:
            coro = loop.create_connection(lambda: client_, self.args["addr"], self.args["port"])
            transport, protocol = loop.run_until_complete(coro)
        except ConnectionRefusedError:
            print('Error. wrong server')
            exit(1)

        # Serve requests until Ctrl+C
        try:
            task = asyncio.ensure_future(client_.get_from_console())  # create Task from coroutine
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

        # create event loop
        app = Qt.QApplication(sys.argv)
        loop = QEventLoop(app)
        asyncio.set_event_loop(loop)  # NEW must set the event loop

        # authentication process
        auth_ = ClientAuth(db_path=self.db_path)
        login_wnd = LoginWindow(auth_instance=auth_)

        if login_wnd.exec_() == QtWidgets.QDialog.Accepted:
            # Each client will create a new protocol instance
            client_ = ChatClientProtocol(db_path=self.db_path,
                                         loop=loop,
                                         username=login_wnd.username,
                                         password=login_wnd.password)

            # create Contacts window
            wnd = ContactsWindow(client_instance=client_, user_name=login_wnd.username)
            client_.gui_instance = wnd  # reference from protocol to GUI, for msg update

            with loop:
                # cleaning old instances
                del auth_
                del login_wnd

                # connect to our server
                try:
                    coro = loop.create_connection(lambda: client_, self.args["addr"], self.args["port"])
                    server = loop.run_until_complete(coro)
                except ConnectionRefusedError:
                    print('Error. wrong server')
                    exit(1)

                # start GUI client
                wnd.show()
                client_.get_from_gui()  # asyncio.ensure_future(client_.get_from_gui(loop))

                # Serve requests until Ctrl+C
                try:
                    loop.run_forever()
                except KeyboardInterrupt:
                    pass
                except Exception:
                    pass


if __name__ == '__main__':
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
