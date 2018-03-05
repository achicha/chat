from datetime import datetime as dt


class JimRequestMessage:
    """Формирование запроса"""

    def presence(self, sender, status="Yep, I am here!"):
        """
        Сформировать ​​presence-сообщение
        :return: Словарь сообщения
        """
        data = {
            "action": "presence",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def request(self, sender, receiver='user1', text='some msg text'):
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
            "from": sender,
            "encoding": 'utf-8',
            "message": text
        }

        return data

    def response(self, code=None, error=None):
        """
        create response dictionary
        :param msg: request message in bytes
        :param code: http code
        :param error: error text
        :return: response dictionary
        """
        _data = {
            'response': code,
            'time': dt.now().timestamp(),
            'error': error
        }
        # if ACTION not in msg:
        #     return {RESPONSE: code or 400,
        #             ERROR: 'Не верный запрос. Action is not exist'}
        # if TIME not in msg or not isinstance(msg[TIME], (float, int)):
        #     return {RESPONSE: code or 400,
        #             ERROR: 'Не верный запрос. Wrong time'}
        # if msg[ACTION] == PRESENCE:
        #     return {RESPONSE: code or 200,
        #             ERROR: error}  # presence msg
        # if msg[ACTION] == MESSAGE:
        #     return {RESPONSE: code or 200,
        #             ERROR: error}  # client msg
        return _data

