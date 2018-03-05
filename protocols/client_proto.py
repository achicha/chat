import asyncio
from sys import stdout

from protocols.messages_proto import JimRequestMessage
from protocols.mixins import ConvertMixin, DbInterfaceMixin


class ChatClientProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, loop, user, gui_instance=None, **kwargs):
        super().__init__(db_path)
        self.user = user
        self.jim = JimRequestMessage()
        self.gui_instance = gui_instance

        self.conn_is_open = False
        self.loop = loop
        self.sockname = None
        self.transport = None

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
        """received bytes, return dict"""
        if data:
            msg = self._bytes_to_dict(data)
            print(msg)
            # self.output(str(msg))
            try:
                if self.gui_instance and self.user == msg['to']:
                    print('gui instance')
                    # todo send to receiver GUI chat. чтото не работает
                    print(self.gui_instance.chat_wnd)
                    self.gui_instance.chat_wnd[self.user]()
            except Exception as e:
                print(e)

    def send(self, to_user=None, content='basic text'):
        """received dict, return bytes"""
        if content:
            if not to_user:
                to_user = self.user
            request = self.jim.request(sender=self.user,
                                       receiver=to_user,
                                       text=content)
            msg = self._dict_to_bytes(request)
            self.transport.write(msg)

    async def getmsgs(self, loop):
        # self.output = self.stdoutput
        # self.output("Connected to {0}:{1}\n".format(*self.sockname))
        while True:
            content = await loop.run_in_executor(None, input, "{}: ".format(self.user))  # Get stdout input forever
            self.send(content=content)

    # async def getgui(self, loop):
    #     def executor():
    #         while not self.is_open:
    #             pass
    #         #self.gui = Gui(None, self)
    #         self.output = self.tkoutput  # Set client output to tk window
    #         self.output("Connected to {0}:{1}\n".format(*self.sockname))
    #         #self.gui.mainloop()
    #         self.transport.close()  # If window closed, close connection
    #         self.loop.stop()
    #
    #     await loop.run_in_executor(None, executor)  # Run GUI in executor for simultanity
    #
    # def tkoutput(self, data):
    #     stdout.write(data)
    #     #return self.gui.text1.insert(1.0, data)

    def stdoutput(self, data):
        """print in terminal
        data -> dict"""
        stdout.write(str(data))