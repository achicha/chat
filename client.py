import socket
from datetime import datetime as dt
from utils import send_msg, get_msg, script_args
from log_config import log
import time


def presense_msg():
    # сообщение присутствия
    data = {
        "action": "presence",
        "time": dt.now().timestamp(),
        "type": "status",
        "user": {
            "account_name": "C0deMaver1ck",
            "status": "Yep, I am here!"
        }
    }
    return data


def client_msg(user1, user2):
    """
    client -> client message
    :param user1: account name to
    :param user2: account name from
    :return:
    """
    data = {
        "action": "msg",
        "time": dt.now().timestamp(),
        "to": user1,
        "from": user2,
        "encoding": 'utf-8',
        "message": "some_message"
    }

    return data


@log
def jim_client(addr, port):
    """
    Клиент
    :param addr: IP адрес сервера
    :param port: порт сервера
    :return:
    """

    try:
        # открываем соединение с сервером
        conn = socket.socket()
        conn.connect((addr, port))

        # todo убрать пробный цикл
        for i in range(5):
            # посылаем сообщение
            send_msg(conn, client_msg(conn.getsockname(), '2'))
            # получаем ответ от сервера
            data = get_msg(conn)
            print(data)

            time.sleep(5)

    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    addr, port = script_args()
    jim_client(addr, port)
