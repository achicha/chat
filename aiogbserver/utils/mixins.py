import json

from aiogbserver.server_config import ENCODING
from aiogbserver.database.controller import ClientMessages
from aiogbserver.database.models import CBase


class ConvertMixin:
    def _dict_to_bytes(self, msg_dict):
        """
        Преобразование словаря в байты
        :param msg_dict: словарь
        :return: bytes
        """
        # Проверям, что пришел словарь
        if isinstance(msg_dict, dict):
            jmessage = json.dumps(msg_dict)  # Преобразуем словарь в json
            bmessage = jmessage.encode(ENCODING)  # Переводим json в байты
            return bmessage
        else:
            raise TypeError

    def _bytes_to_dict(self, msg_bytes):
        """
        Получение словаря из байтов
        :param msg_bytes: сообщение в виде байтов
        :return: словарь сообщения
        """
        # Если переданы байты
        if isinstance(msg_bytes, bytes):

            jmessage = msg_bytes.decode(ENCODING)  # Декодируем
            message = json.loads(jmessage)  # Из json делаем словарь

            # Если там был словарь
            if isinstance(message, dict):
                return message              # Возвращаем сообщение
            else:
                raise TypeError             # Нам прислали неверный тип
        else:
            raise TypeError                 # Передан неверный тип


class DbInterfaceMixin:
    def __init__(self, db_path):
        self._cm = ClientMessages(db_path, CBase, echo=False)  # init DB

    def add_client(self, username, info=None):
        return self._cm.add_client(username, info)

    def get_client_by_username(self, username):
        return self._cm.get_client_by_username(username)

    def add_contact(self, client_username, contact_username):
        return self._cm.add_contact(client_username, contact_username)

    def del_contact(self, client_username, contact_username):
        return self._cm.del_contact(client_username, contact_username)

    def get_contacts(self, client_username):
        return self._cm.get_contacts(client_username)

    def get_all_clients(self):
        return self._cm.get_all_clients()

    def add_client_history(self, client_username, ip_addr='8.8.8.8'):
        return self._cm.add_client_history(client_username, ip_addr)

    def get_client_history(self, client_username):
        return self._cm.get_client_history(client_username)

    def add_client_message(self, client_username, contact_username, text_msg):
        return self._cm.add_client_message(client_username, contact_username, text_msg)

    def get_client_messages(self, client_username):
        return self._cm.get_client_messages(client_username)

    def set_user_offline(self, client_username):
        return self._cm.set_user_offline(client_username)

    def set_user_online(self, client_username):
        return self._cm.set_user_online(client_username)

    def get_user_status(self, client_username):
        return self._cm.get_user_status(client_username)
