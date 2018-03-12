import asyncio
import hashlib
import binascii
from sys import stdout

from aiogbclient.utils.client_messages import JimClientMessage
from aiogbclient.utils.mixins import ConvertMixin, DbInterfaceMixin


class ClientAuth(ConvertMixin, DbInterfaceMixin):
    """Authentication server"""

    def __init__(self, db_path, username=None, password=None):
        super().__init__(db_path)
        self.username = username
        self.password = password

    def authenticate(self):
        """authentication method, which verify user in DB"""

        # check user in DB
        if self.username and self.password:
            usr = self.get_client_by_username(self.username)
            dk = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'),
                                     'salt'.encode('utf-8'), 100000)
            hashed_password = binascii.hexlify(dk)

            if usr:
                # existing user
                if hashed_password == usr.password:
                    # add client's history row
                    # self.add_client_history(self.username)
                    return True
                else:
                    return False
            else:
                # new user
                print('new user')
                self.add_client(self.username, hashed_password)
                # add client's history row
                # self.add_client_history(self.username)
                return True
        else:
            return False


class ChatClientProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, loop, tasks=None, username=None, password=None, gui_instance=None, **kwargs):
        super().__init__(db_path)
        self.user = username
        self.password = password
        self.tasks = tasks
        self.jim = JimClientMessage()
        self.gui_instance = gui_instance

        self.conn_is_open = False
        self.loop = loop
        self.sockname = None
        self.transport = None
        self.output = None

    def connection_made(self, transport):
        """ Called when connection is initiated """
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.send_auth(self.user, self.password)
        self.conn_is_open = True

    def send_auth(self, user, password):
        """send authenticate message to the server"""
        if user and password:
            self.transport.write(self._dict_to_bytes(self.jim.auth(user, password)))

    def connection_lost(self, exc):
        """ Disconnect from the server"""

        # todo хз как убить задачу
        try:
            self.conn_is_open = False
            for task in self.tasks:
                task.cancel()
        except:
            pass
        finally:
            self.loop.stop()
            self.loop.close()

    def data_received(self, data):
        """
        Receive data from server and send output message to console/gui
        :param data: json-like dict in bytes
        :return:
        """
        msg = self._bytes_to_dict(data)
        if msg:
            try:
                if msg['action'] == 'msg':
                    self.output(msg)

                elif msg['action'] == 'list':
                    self.output(msg['contact_list'])

                elif msg['action'] == 'probe':
                    if self.gui_instance:
                        self.gui_instance.is_auth = True
                    # when server sent probe msg -> auth is complete
                    self.transport.write(self._dict_to_bytes(
                        self.jim.presence(self.user,
                                          status="Connected from {0}:{1}".format(*self.sockname))))

                elif msg['action'] == 'response':
                    if msg['code'] == 200:
                        pass

                    elif msg['code'] == 402:
                        self.connection_lost(asyncio.CancelledError)
                    else:
                        self.output(msg)

            except Exception as e:
                print(e)

    def send(self, request):
        """
            Send json-like message
        :param request: dict message
        :return:
        """
        if request:
            msg = self._dict_to_bytes(request)
            self.transport.write(msg)

    def send_msg(self, to_user, content):
        """
        send msg request to user from contact's list
        :param to_user: receiver
        :param content: text msg
        :return:
        """
        if to_user and content:
            request = self.jim.message(self.user, to_user, content)
            self.transport.write(self._dict_to_bytes(request))

    async def get_from_console(self):
        """
        Recieve messages from Console
        :param loop:
        :return:
        """
        while not self.conn_is_open:
            pass

        self.output = self.output_to_console
        self.output("{2} connected to {0}:{1}\n".format(*self.sockname, self.user))

        while True:
            content = await self.loop.run_in_executor(None, input)  # Get stdin/stdout forever
            request = ''
            args_ = content.split(' ')

            if args_[0] == 'list':
                if len(args_) > 1:
                    if args_[1] == 'add':
                        request = self.jim.list_(self.user, status='add', person=args_[2])
                    elif args_[1] == 'del':
                        request = self.jim.list_(self.user, status='del', person=args_[2])
                else:
                    request = self.jim.list_(self.user)
            elif args_[0] == 'quit':
                self.connection_lost(asyncio.CancelledError)
            else:
                # if message to another person
                if len(args_) < 2:
                    print('wrong message or receivers name')
                else:
                    request = self.jim.message(sender=self.user,
                                               receiver=args_[0],
                                               text=' '.join(args_[1:]))
            if request:
                self.send(request)

    def output_to_console(self, data):
        """
            print output data to terminal
        :param data: msg dictionary
        :return:
        """
        _data = data
        try:
            if _data['from'] == self.user:
                _data['message'] = 'Me to {}: '.format(_data['to']) + _data['message']
            else:
                _data['message'] = '{}: '.format(_data['from']) + _data['message']
            stdout.write(str(_data['message']) + '\n')
        except:
            stdout.write(str(_data) + '\n')

    def get_from_gui(self):
        self.output = self.output_to_gui
        # await loop.run_in_executor(None, self.output)  # Run GUI in executor

    def output_to_gui(self, msg, response=False):
        """
         send update signal to GUI client
        :param response: raw response from server {'response':200}
        :type msg: message dictionary
        :return:
        """
        try:
            if self.gui_instance:
                if response:
                    self.gui_instance.is_auth = True

                if self.user == msg['to']:
                    self.gui_instance.chat_ins()

        except Exception as e:
            print(e)
