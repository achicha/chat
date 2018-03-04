import asyncio
import json
import argparse
from datetime import datetime

from Messages import JimRequestMessage
from abase import MyMixin


class ChatServerProtocol(asyncio.Protocol, MyMixin):
    """ A Server Protocol listening for subscriber messages """
    def __init__(self, connections, users):
        self.connections = connections
        self.users = users
        self.jim = JimRequestMessage()
        #self.user = None

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
        #self.jim.response(500, err)
        print(err)

    def _login_required(self, username):
        """check user's credentials or add new user to DB"""
        # todo this
        # 1. check DB
        # 2. add new user
        # 3. user exist
        pass

    def data_received(self, data):
        """The protocol expects a json message:

        and will return the following json message

        """
        _data = self._bytes_to_dict(data)

        if _data:
            if not self.connections[self.transport]['username']:
                # when first message received

                # add new user
                self.connections[self.transport]['username'] = _data['user']['account_name']
                self.users[_data['user']['account_name']] = self.connections[self.transport]

                # check user
                self._login_required(self.connections[self.transport]['username'])

                if _data['action'] == 'presence':
                    # received presence msg
                    # msg = '{} connected {}'.format(self.connections[self.transport]['username'],
                    #                                self.connections[self.transport]['peername'])
                    # print(msg)
                    print(_data['user']['account_name'], _data['user']['status'])
                    resp_msg = self.jim.response(code=200)
                    self.transport.write(self._dict_to_bytes(resp_msg))

                else:
                    resp_msg = self.jim.response(code=500, error='wrong presence msg')
                    self.transport.write(self._dict_to_bytes(resp_msg))
            else:
                # chat
                if _data['from']:
                    # send msg to sender's chat
                    _data['message'] = 'Me: ' + _data['message']
                    self.transport.write(self._dict_to_bytes(_data))
                if _data['to'] and _data['from'] != _data['to']:
                    # send msg to receiver's chat
                    print(_data['to'])

        else:
            resp_msg = self.jim.response(code=500, error='You sent a message without a name or data')
            self.transport.write(self._dict_to_bytes(resp_msg))

    # def make_msg(self, message, author, *event):
    #     """create json response to client"""
    #     msg = dict()
    #     msg["content"] = message
    #     msg["author"] = author
    #     time = datetime.utcnow()
    #     msg["timestamp"] = "{hour}:{minute}:{sec}".format(hour=str(time.hour).zfill(2),
    #                                                       minute=str(time.minute).zfill(2),
    #                                                       sec=str(time.second).zfill(2))
    #     if event:
    #         msg["event"] = event[0]
    #     else:
    #         msg["event"] = "message"
    #     return json.dumps(msg).encode()


def parse_args():
    parser = argparse.ArgumentParser(description="Server settings")
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    connections = dict()
    users = dict()
    loop = asyncio.get_event_loop()

    # Each client will create a new protocol instance
    coro = loop.create_server(lambda: ChatServerProtocol(connections, users), args["addr"], args["port"])
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
    main()
