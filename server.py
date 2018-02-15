from socket import socket, AF_INET, SOCK_STREAM
from utils import send_msg, get_msg, script_args
from config import *


def presence_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return: Словарь ответа
    """
    # Делаем проверки
    if ACTION in presence_message \
            and presence_message[ACTION] == PRESENCE \
            and TIME in presence_message \
            and isinstance(presence_message[TIME], (float, int)):

        # Если всё хорошо шлем ОК
        return {RESPONSE: 200}
    else:
        # Шлем код ошибки
        return {RESPONSE: 400, ERROR: 'Не верный запрос'}


def jim_server(addr, port, backlog=5, timeout=5):
    """
    Сервер
    :param addr: ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса)
    :param port: <port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт 14900)
    :param backlog: сколько запросов одновременно может обслуживать сервер. (default=5)
    :param timeout: таймаут, если данные не придут, то будет выслан пустой объект bytes. (default=5)
    :return:
    """
    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind((addr, port))  # Присваивает адрес и порт
    sock.listen(backlog)  # Переходит в режим ожидания запросов

    try:
        while True:
            try:
                conn, addr = sock.accept()  # Принять запрос на соединение от клиента
                print('Got connection from', addr)
                conn.settimeout(timeout)

                data = get_msg(conn)        # принять данные
                if not data:
                    print("No data")
                    conn.close()

                response = presence_response(data)  # проверить присутствие
                send_msg(conn, response)
            except:
                pass
            finally:
                conn.close()
    finally:
        sock.close()


if __name__ == '__main__':
    addr, port = script_args()
    jim_server(addr, port)
