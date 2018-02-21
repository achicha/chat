import json
import sys
from config import ENCODING, PORT


class BaseJimMessage:

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

    def send(self, sock, msg):
        """
        Отправка сообщения
        :param sock: сокет
        :param msg: словарь сообщения
        :return: None
        """
        bmsg = self._dict_to_bytes(msg)     # Словарь переводим в байты
        sock.send(bmsg)                     # Отправляем

    def get(self, sock):
        """
        Получение сообщения
        :param sock: сокет
        :return: словарь ответа
        """
        bresp = sock.recv(8192)             # Получаем байты
        resp = self._bytes_to_dict(bresp)   # переводим байты в словарь
        return resp
