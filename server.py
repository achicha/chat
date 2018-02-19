from socket import socket, AF_INET, SOCK_STREAM
import queue
import select

from utils import send_msg, get_msg, script_args
from config import *
from log_config import log


@log
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


def new_listen_socket(addr, port, backlog=5, timeout=0.2):
    """
    Socket
    :param addr: ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса)
    :param port: <port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт 14900)
    :param backlog: сколько запросов одновременно может обслуживать сервер. (default=5)
    :param timeout: таймаут, если данные не придут, то будет выслан пустой объект bytes. (default=0.2)
            - проверить сокет на наличие подключений новых клиентов
            - проверить сокет на наличие данных
    :return:
    """
    sock = socket(AF_INET, SOCK_STREAM)  # Создает сокет TCP
    sock.bind((addr, port))         # Присваивает адрес и порт
    sock.listen(backlog)            # Переходит в режим ожидания запросов
    sock.settimeout(timeout)        # Таймаут для операций с сокетом
    return sock


@log
def jim_server(addr, port, backlog=5, timeout=0.2):
    """
    Сервер
    :param addr: ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса)
    :param port: <port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт 14900)
    :param backlog: сколько запросов одновременно может обслуживать сервер. (default=5)
    :param timeout: таймаут, если данные не придут, то будет выслан пустой объект bytes. (default=5)
    :return:
    """
    server = new_listen_socket(addr, port, 5, 1)

    inputs = [server]
    outputs = []
    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0)

        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                connection.setblocking(1)
                inputs.append(connection)
                print("Получен запрос на соединение с %s" % str(client_address))
                message_queues[connection] = queue.Queue()
            else:
                data = get_msg(s)
                if data:
                    message_queues[s].put(data)
                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                for i in inputs[1:]: # 1 element is our server
                    try:
                        send_msg(i, next_msg)
                    except Exception as e:
                        print(e)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == '__main__':
    addr, port = script_args()
    jim_server(addr, port)
