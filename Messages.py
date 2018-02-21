from datetime import datetime as dt
from BaseJimMessage import BaseJimMessage
from config import *


class JimRequestMessage(BaseJimMessage):
    """Формирование запроса"""

    def __init__(self, sender):
        """
        :param sender: account name who send this message
        """
        self.sender = sender

    def presence(self, status="Yep, I am here!"):
        """
        Сформировать ​​presence-сообщение
        :return: Словарь сообщения
        """
        data = {
            "action": "presence",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": self.sender,
                "status": status
            }
        }
        return data

    def request(self, receiver='user1', text='need to use it later'):
        """
        client -> client message

        :param receiver: account name. message to
        :param text: message text
        :return: Словарь сообщения
        """
        data = {
            "action": "msg",
            "time": dt.now().timestamp(),
            "to": receiver,
            "from": self.sender,
            "encoding": 'utf-8',
            "message": text
        }

        return data


class JimResponseMessage(BaseJimMessage):
    """Формирование ответа клиенту"""

    def response(self, msg, code=None, error=None):
        """
        create response dictionary
        :param msg: request message in bytes
        :param code: http code
        :param error: error text
        :return: response dictionary
        """
        if ACTION not in msg:
            return {RESPONSE: code or 400,
                    ERROR: 'Не верный запрос. Action is not exist'}
        if TIME not in msg or not isinstance(msg[TIME], (float, int)):
            return {RESPONSE: code or 400,
                    ERROR: 'Не верный запрос. Wrong time'}
        if msg[ACTION] == PRESENCE:
            return {RESPONSE: code or 200,
                    ERROR: error}  # presence msg
        if msg[ACTION] == MESSAGE:
            return {RESPONSE: code or 200,
                    ERROR: error}  # client msg
