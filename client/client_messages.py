from datetime import datetime as dt


class JimClientMessage:
    """Формирование запроса клиента"""
    def auth(self, username, password):
        """
        Сообщение для авторизации пользователя на сервере
        :param username:
        :param password:
        :return:
        """
        data = {
            "action": "authenticate",
            "time": dt.now().timestamp(),
            "user": {
                "account_name": username,
                "password": password
            }
        }
        return data

    def presence(self, sender, status="Yep, I am here!"):
        """
        Сформировать ​​presence-сообщение присутствие.
        Сервисное сообщение для извещения сервера о присутствии клиента​ ​ online;
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

    def quit(self, sender, status="disconnect"):
        """
        Сформировать quit-сообщение. Клиент хочет отключится от сервера.
        :return: Словарь сообщения
        """
        data = {
            "action": "quit",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def list_(self, sender, status="my contacts list"):
        """
        Сформировать list-сообщение для запроса контактов.
        :return: Словарь сообщения
        """
        data = {
            "action": "list",
            "time": dt.now().timestamp(),
            "type": "status",
            "contact_list": [],
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def message(self, sender, receiver='user1', text='some msg text'):
        """
        client -> client message
        ​простое​ ​ сообщение​ ​ пользователю​ ​ или​ ​ в ​ ​ чат;

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
