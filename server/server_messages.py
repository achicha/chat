from datetime import datetime as dt


class JimServerMessage:
    """Формирование запроса сервера"""
    def response(self, code=None, error=None):
        """
        create response dictionary
        :param msg: request message in bytes
        :param code: http code
        :param error: error text
        :return: response dictionary
        """
        _data = {
            'action': 'response',
            'code': code,
            'time': dt.now().timestamp(),
            'error': error
        }
        return _data

    def probe(self, sender, status="Are you there?"):
        """
        Сформировать ​​presence-сообщение присутствие.
        Сервисное сообщение для извещения сервера о присутствии клиента​ ​ online;
        :return: Словарь сообщения
        """
        data = {
            "action": "probe",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data
