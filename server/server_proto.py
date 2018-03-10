import asyncio
import hashlib
import binascii

from server.server_messages import JimServerMessage
from utils.mixins import ConvertMixin, DbInterfaceMixin


class ChatServerProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    """ A Server Protocol listening for subscriber messages """

    def __init__(self, db_path, connections, users):
        super().__init__(db_path)
        self.connections = connections
        self.users = users
        self.jim = JimServerMessage()

        # useful temp variables
        self.user = None
        self.transport = None

    def connection_made(self, transport):
        """ Called when connection is initiated """

        self.connections[transport] = {'peername': transport.get_extra_info('peername'),
                                       'username': '',
                                       'transport': transport
                                       }
        self.transport = transport

    def eof_received(self):
        print('EOF(end-of-file) received')
        self.transport.close()

    def connection_lost(self, exc):
        """Transport Error or EOF(end-of-file), which
        means the client is disconnected."""

        if isinstance(exc, ConnectionResetError):
            del self.connections[self.transport]
            del self.users[self.connections[self.transport]['username']]

            print(self.connections)
            print(self.users)
        else:
            print(exc)
            # remove closed connections
            rm_con = []
            for con in self.connections:
                if con._closing:
                    rm_con.append(con)

            for i in rm_con:
                del self.connections[i]

            # remove from users
            rm_user = []
            for k, v in self.users.items():
                for con in rm_con:
                    if v['transport'] == con:
                        rm_user.append(k)

            for u in rm_user:
                del self.users[u]
                print('{} disconnected'.format(u))

    def _login_required(self, username):
        """check user's credentials or add new user to DB"""
        # add client's history row
        # self.add_client_history(username)
        pass

    def authenticate(self, username, password):
        # check user in DB
        usr = self.get_client_by_username(username)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),
                                 'salt'.encode('utf-8'), 100000)
        hashed_password = binascii.hexlify(dk)

        if usr:
            # existing user
            if hashed_password == usr.password:
                # add client's history row
                self.add_client_history(username)
                return True
            else:
                return False
        else:
            # new user
            print('new user')
            self.add_client(username, hashed_password)
            # add client's history row
            self.add_client_history(username)
            return True

    def data_received(self, data):
        """The protocol expects a json message:

        and will return the following json message

        """
        _data = self._bytes_to_dict(data)
        if _data:
            try:
                if _data['action'] == 'msg':
                    if _data['from']:  # send msg to sender's chat
                        print(_data)

                        # save msg to DB history messages
                        self._cm.add_client_message(_data['from'], _data['to'], _data['message'])

                        self.users[_data['from']]['transport'].write(self._dict_to_bytes(_data))

                    if _data['to'] and _data['from'] != _data['to']:  # send msg to receiver's chat
                        try:
                            self.users[_data['to']]['transport'].write(self._dict_to_bytes(_data))
                        except KeyError:
                            print('{} is not connected yet'.format(_data['to']))

                elif _data['action'] == 'list':
                    if _data['user']['status'] == 'show':
                        contacts = self.get_contacts(_data['user']['account_name'])
                        if contacts:
                            _data['contact_list'] = ','.join([contact.contact.username for contact in contacts])

                        self.users[_data['user']['account_name']]['transport'].write(self._dict_to_bytes(_data))

                    elif _data['user']['status'] == 'add':
                        if _data['user']['contact']:
                            self.add_contact(_data['user']['account_name'], _data['user']['contact'])

                    elif _data['user']['status'] == 'del':
                        if _data['user']['contact']:
                            self.del_contact(_data['user']['account_name'], _data['user']['contact'])

                elif _data['action'] == 'presence':  # received presence msg
                    if _data['user']['account_name']:

                        print(self.user, _data['user']['status'])
                        resp_msg = self.jim.response(code=200)
                        self.transport.write(self._dict_to_bytes(resp_msg))
                    else:
                        resp_msg = self.jim.response(code=500, error='wrong presence msg')
                        self.transport.write(self._dict_to_bytes(resp_msg))

                elif _data['action'] == 'authenticate':
                    # todo complete this
                    if self.authenticate(_data['user']['account_name'], _data['user']['password']):

                        # add new user to temp variables
                        if _data['user']['account_name'] not in self.users:
                            self.user = _data['user']['account_name']
                            self.connections[self.transport]['username'] = self.user
                            self.users[_data['user']['account_name']] = self.connections[self.transport]

                        resp_msg = self.jim.probe(self.user)
                        self.users[_data['user']['account_name']]['transport'].write(self._dict_to_bytes(resp_msg))
                    else:
                        resp_msg = self.jim.response(code=402, error='wrong login/password')
                        self.transport.write(self._dict_to_bytes(resp_msg))

                elif _data['action'] == 'quit':
                    print('disconnect')
                    # todo quit

            except Exception as e:
                resp_msg = self.jim.response(code=500, error=e)
                self.transport.write(self._dict_to_bytes(resp_msg))

        else:
            resp_msg = self.jim.response(code=500, error='You sent a message without a name or data')
            self.transport.write(self._dict_to_bytes(resp_msg))
