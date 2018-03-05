import asyncio, json, argparse
from sys import stdout

from Messages import JimRequestMessage
from abase import ConvertMixin, DbInterfaceMixin


class ChatClientProtocol(asyncio.Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, loop, user, **kwargs):
        super().__init__(db_path)
        self.user = user
        self.jim = JimRequestMessage()

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


def parse_args():
    parser = argparse.ArgumentParser(description="Client settings")
    parser.add_argument("--user", default="user_2", type=str)
    parser.add_argument("--addr", default="127.0.0.1", type=str)
    parser.add_argument("--port", default=50000, type=int)
    parser.add_argument("--gui", default=True, type=bool)
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    loop = asyncio.get_event_loop()
    _client = ChatClientProtocol(loop, args["user"])
    coro = loop.create_connection(lambda: _client, args["addr"], args["port"])
    server = loop.run_until_complete(coro)

    if args["gui"]:
        asyncio.ensure_future(_client.getmsgs(loop))
    else:
        asyncio.ensure_future(_client.getgui(loop))

    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
