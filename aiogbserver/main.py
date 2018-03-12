"""файл для запуска серверного приложения в цикле"""
import argparse
import asyncio
import sys

from PyQt5 import Qt
#from PyQt5.QtCore import QEventLoop
from quamash import QEventLoop  # asyncio works fine with pyqt5 loop

from aiogbserver.server_config import DB_PATH, PORT
from aiogbserver.utils.server_proto import ChatServerProtocol
from aiogbserver.ui.windows import ServerMonitorWindow


class ConsoleServerApp:
    """Console server"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()
        loop = asyncio.get_event_loop()

        # Each client will create a new protocol instance
        self.ins = ChatServerProtocol(self.db_path, connections, users)

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


class GuiServerApp:
    """Gui server"""

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

        wnd = ServerMonitorWindow(server_instance=self.ins, parsed_args=self.args)
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


if __name__ == '__main__':
    def parse_args():
        parser = argparse.ArgumentParser(description="Server settings")
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=PORT, type=int)
        parser.add_argument('--nogui', action='store_true')
        return vars(parser.parse_args())


    args = parse_args()

    if args['nogui']:
        # start consoles server
        a = ConsoleServerApp(args, DB_PATH)
        a.main()
    else:
        # start GUI server
        a = GuiServerApp(args, DB_PATH)
        a.main()
