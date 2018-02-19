import socket
from datetime import datetime as dt
from utils import send_msg, get_msg, script_args
from log_config import log


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

        # сообщение присутствия
        presence_data = {
            "action": "presence",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                    "account_name": "C0deMaver1ck",
                    "status": "Yep, I am here!"
                    }
            }

        send_msg(conn, presence_data)

        # получаем ответ от сервера
        data = get_msg(conn)
        print(data)
    except Exception as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    addr, port = script_args()
    jim_client(addr, port)
