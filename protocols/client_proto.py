import asyncio
from sys import stdout
import hashlib, binascii

from protocols.messages_proto import JimRequestMessage
from protocols.mixins import ConvertMixin, DbInterfaceMixin


class ChatClientProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, loop, username, password, gui_instance=None, **kwargs):
        super().__init__(db_path)
        self.user = username
        self.password = password
        self.jim = JimRequestMessage()
        self.gui_instance = gui_instance

        self.conn_is_open = False
        self.loop = loop
        self.sockname = None
        self.transport = None
        self.output = None

        self.is_auth = self.client_auth()

    def connection_made(self, transport):
        """ Called when connection is initiated """
        self.sockname = transport.get_extra_info("sockname")
        self.transport = transport
        self.transport.write(self._dict_to_bytes(self.jim.presence(self.user,
                                                                   status="Connected from {0}:{1}".format(
                                                                       *self.sockname))))
        self.conn_is_open = True

    def connection_lost(self, exc):
        """ Disconnect from the server"""
        self.conn_is_open = False
        self.loop.stop()

    def data_received(self, data):
        """
        Receive data from server and send output message to console/gui
        :param data: json-like dict in bytes
        :return:
        """
        msg = self._bytes_to_dict(data)
        if msg:
            try:
                if msg['from']:
                    self.output(msg)
            except Exception as e:
                pass

    def client_auth(self):
        # check user in DB
        usr = self.get_client_by_username(self.user)
        if usr:
            # existing user
            dk = hashlib.pbkdf2_hmac('sha256',  self.password.encode('utf-8'),
                                     'salt'.encode('utf-8'), 100000)
            hashed_password = binascii.hexlify(dk)

            if hashed_password == usr.password:
                return True
            else:
                return False
        else:
            # new user
            dk = hashlib.pbkdf2_hmac('sha256', self.password.encode('utf-8'),
                                     'salt'.encode('utf-8'), 100000)
            hashed_password = binascii.hexlify(dk)

            self.add_client(self.user, hashed_password)
            return True

    def send(self, to_user=None, content='basic text'):
        """
            Send json-like message
        :param to_user:
        :param content:
        :return:
        """
        if content:
            if not to_user:
                to_user = self.user
            request = self.jim.request(sender=self.user,
                                       receiver=to_user,
                                       text=content)
            msg = self._dict_to_bytes(request)
            self.transport.write(msg)

    async def get_from_console(self, loop):
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
            content = await loop.run_in_executor(None, input)#, "{}: ".format(self.user))  # Get stdin/stdout forever
            self.send(content=content)

    def output_to_console(self, data):
        """
            print output data to terminal
        :param data: msg dictionary
        :return:
        """
        _data = data
        try:
            if _data['from'] == self.user:
                _data['message'] = 'Me: ' + _data['message']
            else:
                _data['message'] = '{}: '.format(_data['from']) + _data['message']
            stdout.write(str(_data['message']) + '\n')
        except:
            stdout.write(str(_data) + '\n')

    def get_from_gui(self):
        self.output = self.output_to_gui
        #await loop.run_in_executor(None, self.output)  # Run GUI in executor

    def output_to_gui(self, msg):
        """
         send update signal to GUI client
        :type msg: message dictionary
        :return:
        """
        try:
            if self.gui_instance and self.user == msg['to']:
                self.gui_instance.chat_ins()
        except Exception as e:
            print(e)
