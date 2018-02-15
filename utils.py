import json
import sys
from config import ENCODING, PORT


def dict_to_bytes(msg_dict):
    """
    Преобразование словаря в байты
    :param msg_dict: словарь
    :return: bytes
    """
    # Проверям, что пришел словарь
    if isinstance(msg_dict, dict):
        jmessage = json.dumps(msg_dict)         # Преобразуем словарь в json
        bmessage = jmessage.encode(ENCODING)    # Переводим json в байты
        return bmessage
    else:
        raise TypeError


def bytes_to_dict(msg_bytes):
    """
    Получение словаря из байтов
    :param msg_bytes: сообщение в виде байтов
    :return: словарь сообщения
    """
    # Если переданы байты
    if isinstance(msg_bytes, bytes):
        jmessage = msg_bytes.decode(ENCODING)   # Декодируем
        message = json.loads(jmessage)          # Из json делаем словарь
        # Если там был словарь
        if isinstance(message, dict):
            # Возвращаем сообщение
            return message
        else:
            # Нам прислали неверный тип
            raise TypeError
    else:
        # Передан неверный тип
        raise TypeError


def send_msg(sock, msg):
    """
    Отправка сообщения
    :param sock: сокет
    :param msg: словарь сообщения
    :return: None
    """
    bmsg = dict_to_bytes(msg)                   # Словарь переводим в байты
    sock.send(bmsg)                             # Отправляем


def get_msg(sock):
    """
    Получение сообщения
    :param sock: сокет
    :return: словарь ответа
    """
    # Получаем байты
    bresp = sock.recv(1024)
    resp = bytes_to_dict(bresp)                 # переводим байты в словарь
    return resp


def script_args():
    # Получаем аргументы скрипта
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
    return addr, port
