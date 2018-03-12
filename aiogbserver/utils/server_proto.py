import asyncio
import hashlib
import binascii
from functools import wraps

from aiogbserver.utils.server_messages import JimServerMessage
from aiogbserver.utils.mixins import ConvertMixin, DbInterfaceMixin


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
        """EOF(end-of-file)"""
        # print('EOF(end-of-file) received')
        self.transport.close()

    def connection_lost(self, exc):
        """Transport Error , which means the client is disconnected."""

        if isinstance(exc, ConnectionResetError):
            #del self.connections[self.transport]
            #del self.users[self.connections[self.transport]['username']]
            print('ConnectionResetError')
            print(self.connections)
            print(self.users)

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
            self.set_user_offline(u)
            print('{} disconnected'.format(u))

    def _login_required(func):
        """Login required decorator, which accepts only authorized clients"""

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            is_auth = self.get_user_status(self.user)
            # print('is_auth status: {}'.format(is_auth))
            if is_auth:
                result = func(self, *args, **kwargs)
                return result
            else:
                resp_msg = self.jim.response(code=501, error='login required')
                self.users[self.user]['transport'].write(self._dict_to_bytes(resp_msg))

        return wrapper

    def authenticate(self, username, password):
        # check user in DB
        if username and password:
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
        else:
            return False

    @_login_required
    def action_list(self, data):
        """
         Receive internal request to show/add/del contacts
        :param data: msg dict
        :return:
        """
        if data['user']['status'] == 'show':
            contacts = self.get_contacts(data['user']['account_name'])
            if contacts:
                data['contact_list'] = ','.join([contact.contact.username for contact in contacts])

            self.users[data['user']['account_name']]['transport'].write(self._dict_to_bytes(data))

        elif data['user']['status'] == 'add':
            if data['user']['contact']:
                self.add_contact(data['user']['account_name'], data['user']['contact'])

        elif data['user']['status'] == 'del':
            if data['user']['contact']:
                self.del_contact(data['user']['account_name'], data['user']['contact'])

    @_login_required
    def action_msg(self, data):
        """
         Receive message from another user
        :param data: msg dict
        :return:
        """
        try:
            if data['from']:  # send msg to sender's chat
                print(data)

                # save msg to DB history messages
                self._cm.add_client_message(data['from'], data['to'], data['message'])

                self.users[data['from']]['transport'].write(self._dict_to_bytes(data))

            if data['to'] and data['from'] != data['to']:  # send msg to receiver's chat
                try:
                    self.users[data['to']]['transport'].write(self._dict_to_bytes(data))
                except KeyError:
                    # resp_msg = self.jim.response(code=404, error='user is not connected')
                    # self.users[data['from']]['transport'].write(self._dict_to_bytes(resp_msg))
                    print('{} is not connected yet'.format(data['to']))

        except Exception as e:
            resp_msg = self.jim.response(code=500, error=e)
            self.transport.write(self._dict_to_bytes(resp_msg))

    def data_received(self, data):
        """The protocol expects a json message in bytes"""

        _data = self._bytes_to_dict(data)
        print(_data)
        if _data:
            try:
                if _data['action'] == 'msg':
                    self.user = _data['from']
                    self.action_msg(_data)

                elif _data['action'] == 'list':
                    self.user = _data['user']['account_name']
                    self.action_list(_data)

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
                            self.set_user_online(_data['user']['account_name'])

                        resp_msg = self.jim.probe(self.user)
                        self.users[_data['user']['account_name']]['transport'].write(self._dict_to_bytes(resp_msg))
                    else:
                        resp_msg = self.jim.response(code=402, error='wrong login/password')
                        self.transport.write(self._dict_to_bytes(resp_msg))

            except Exception as e:
                resp_msg = self.jim.response(code=500, error=e)
                self.transport.write(self._dict_to_bytes(resp_msg))

        else:
            resp_msg = self.jim.response(code=500, error='You sent a message without a name or data')
            self.transport.write(self._dict_to_bytes(resp_msg))
