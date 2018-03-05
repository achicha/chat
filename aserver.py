import asyncio
import argparse

from Messages import JimRequestMessage
from abase import ConvertMixin, DbInterfaceMixin
from config import DB_PATH


class ChatServerProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    """ A Server Protocol listening for subscriber messages """
    def __init__(self, db_path, connections, users):
        super().__init__(db_path)
        self.connections = connections
        self.users = users
        self.jim = JimRequestMessage()

        # useful temp variables
        self.user = None
        self.transport = None

    def connection_made(self, transport):
        """ Called when connection is initiated """

        self.connections[transport] = {'peername': transport.get_extra_info('sockname'),
                                       'username': '',
                                       'transport': transport
                                       }
        self.transport = transport

    def connection_lost(self, exc):
        """Transport Error or EOF(end-of-file), which
        means the client is disconnected."""

        if isinstance(exc, ConnectionResetError):
            del self.connections[self.transport]
            print(self.connections)
        else:
            print(exc)
        err = "{} disconnected".format(self.connections[self.transport]['peername'])
        print(err)

    def _login_required(self, username):
        """check user's credentials or add new user to DB"""
        # add user to DB if not exist
        if not self.get_client_by_username(username):
            self.add_client(username)  # add new client

        # add client's history row
        self.add_client_history(username)

    def data_received(self, data):
        """The protocol expects a json message:

        and will return the following json message

        """
        _data = self._bytes_to_dict(data)

        if _data:
            try:
                if _data['from']:
                    print(_data)
                    # save msg to DB history messages
                    self._cm.add_client_message(_data['from'], _data['to'], _data['message'])
                    # send msg to sender's chat
                    _data['message'] = 'Me: ' + _data['message']
                    self.users[_data['from']]['transport'].write(self._dict_to_bytes(_data))

                if _data['to'] and _data['from'] != _data['to']:
                    # send msg to receiver's chat
                    self.users[_data['to']]['transport'].write(self._dict_to_bytes(_data))
                    print(_data['to'])

            except Exception as e:
                if _data['user']['account_name']:
                    # when first message received

                    # add new user to temp variables
                    print(_data['user']['account_name'], self.transport)
                    self.user = _data['user']['account_name']
                    self.connections[self.transport]['username'] = self.user
                    self.users[_data['user']['account_name']] = self.connections[self.transport]

                    # check user in DB
                    self._login_required(self.user)

                    if _data['action'] == 'presence':
                        # received presence msg
                        print(self.user, _data['user']['status'])
                        resp_msg = self.jim.response(code=200)
                        self.transport.write(self._dict_to_bytes(resp_msg))

                    else:
                        resp_msg = self.jim.response(code=500, error='wrong presence msg')
                        self.transport.write(self._dict_to_bytes(resp_msg))

        else:
            resp_msg = self.jim.response(code=500, error='You sent a message without a name or data')
            self.transport.write(self._dict_to_bytes(resp_msg))


class ConsoleApp:
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


if __name__ == "__main__":
    def parse_args():
        parser = argparse.ArgumentParser(description="Server settings")
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=50000, type=int)
        args = vars(parser.parse_args())
        return args


    app = ConsoleApp(parse_args(), DB_PATH)
    app.main()
