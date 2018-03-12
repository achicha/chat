from pytest import raises
import socket
import json
from aiogbserver.utils.mixins import dict_to_bytes, bytes_to_dict, get_msg, send_msg


# МОДУЛЬНОЕ ТЕСТИРОВАНИЕ
def test_dict_to_bytes():
    with raises(TypeError):
        dict_to_bytes('abc')
    assert dict_to_bytes({'test': 'test'}) == b'{"test": "test"}'


def test_bytes_to_dict():
    with raises(TypeError):
        bytes_to_dict(100)
    with raises(TypeError):
        bytes_to_dict(b'["abc"]')
    assert bytes_to_dict(b'{"test": "test"}') == {'test': 'test'}


# ИНТЕГРАЦИОННОЕ ТЕСТИРОВАНИЕ

# Класс заглушка для сокета
class ClientSocket():
    """Класс-заглушка для операций с сокетом"""
    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, n):
        # Наш класс заглушка будет всегда отправлять одинаковый ответ при вызов sock.recv
        message = {'response': 200}
        jmessage = json.dumps(message)
        bmessage = jmessage.encode('utf-8')
        return bmessage

    def send(self, bmessage):
        # можно переопределить метод send просто pass
        pass


def test_get_msg(monkeypatch):
    # подменяем настоящий сокет нашим классом заглушкой
    monkeypatch.setattr("socket.socket", ClientSocket)
    # зоздаем сокет, он уже был подменен
    sock = socket.socket()
    # теперь можем протестировать работу метода
    assert get_msg(sock) == {'response': 200}


def test_send_msg(monkeypatch):
    # подменяем настоящий сокет нашим классом заглушкой
    monkeypatch.setattr("socket.socket", ClientSocket)
    # создаем сокет, он уже был подменен
    sock = socket.socket()
    # т.к. возвращаемого значения нету, можно просто проверить, что метод отрабатывает без ошибок
    assert send_msg(sock, {'test': 'test'}) is None
    # и проверяем, чтобы обязательно передавали словарь на всякий пожарный
    with raises(TypeError):
        send_msg(sock, 'test')
