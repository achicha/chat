import socket
import sys
from random import random

import time

from protocols.messages_proto import JimRequestMessage, JimResponseMessage
from config import PORT, OK
from log_config import log


@log
class Client:
    def __init__(self, addr, port, login):
        """
           Клиент
           :param addr: IP адрес сервера
           :param port: порт сервера
           :return:
        """
        self.login = login
        self.request = JimRequestMessage(login)
        self.response = JimResponseMessage()
        # открываем соединение с сервером
        self.connector = socket.socket()
        self.connector.connect((addr, port))

    def read_messages(self):
        """
        Клиент читает входящие сообщения в бесконечном цикле
        :param sock: сокет клиента
        """
        while True:
            # читаем сообщение
            print('Читаю', self.connector.getsockname())
            message = self.request.get(self.connector)
            print(message)

    def write_messages(self, text):
        """
        Клиент пишет сообщение в бесконечном цикле
        :param sock: client's socket
        :param text: message text
        :return:
        """
        while True:
            print('Пишу', self.connector.getsockname())
            # Создаем jim сообщение
            message = self.request.request('#all', text)
            # отправляем на сервер
            self.request.send(self.connector, message)
            time.sleep(3)

    def __del__(self):
        self.connector.close()


if __name__ == '__main__':
    """Получаем аргументы скрипта"""
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''   # "127.0.0.1"
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = PORT
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)
    # client's mode (read or write)
    try:
        mode = sys.argv[3]
    except IndexError:
        mode = 'r'

    client = Client(addr, port, str(random()))  # random number as client's name

    # presence msg
    presence_request_data = client.request.presence()
    client.request.send(client.connector, presence_request_data)
    presence_response = client.response.get(client.connector)
    if presence_response['response'] == OK:

        # в зависимости от режима мы будем или слушать или отправлять сообщения
        if mode == 'r':
            client.read_messages()
        elif mode == 'w':
            client.write_messages('some_msg_text')
        else:
            raise Exception('Не верный режим чтения/записи')
