import select
from socket import socket, AF_INET, SOCK_STREAM
import sys

from config import PORT
from Messages import JimResponseMessage
from log_config import log


@log
class Server:
    def __init__(self, addr, port, backlog=15, timeout=0.2):
        """
        Create socket
        :param addr: ​​<addr> ​-​ ​I​P-адрес ​​для ​​прослушивания ​(​по ​у​молчанию ​с​лушает ​​все ​​доступные ​​адреса)
        :param port: <port> ​-​ ​​TCP-порт ​​для ​​работы ​(​по ​у​молчанию ​​использует ​​порт 14900)
        :param backlog: сколько запросов одновременно может обслуживать сервер. (default=5)
        :param timeout: таймаут, если данные не придут, то будет выслан пустой объект bytes. (default=0.2)
                        - проверить сокет на наличие подключений новых клиентов
                        - проверить сокет на наличие данных
        """
        self.sock = socket(AF_INET, SOCK_STREAM)    # Создает сокет TCP
        self.sock.bind((addr, port))                # Присваивает адрес и порт
        self.sock.listen(backlog)                   # Переходит в режим ожидания запросов
        self.sock.settimeout(timeout)               # Таймаут для операций с сокетом
        self.clients = []                           # список всех подключенных клиентов
        self.response = JimResponseMessage()      # messenger instance

    def read_requests(self, r_clients, w_clients, all_clients):
        """Чтение запросов из списка клиентов"""

        responses = {}  # Словарь ответов сервера вида {сокет: запрос}
        # todo Проверяем, правильно ли составлен запрос convert to dict and back.
        for sock in r_clients:
            try:
                data = self.response.get(sock)
                responses[sock] = data
            except:
                if sock not in w_clients: # не выкидываем клиентов, которые только пишут
                    print('Клиент read {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    all_clients.remove(sock)

        return responses

    def write_responses(self, requests, w_clients, all_clients):
        """
        Отправка сообщений тем клиентам, которые их ждут
        :param requests: список сообщений запросов
        :param w_clients: клиенты которые читают
        :param all_clients: все клиенты
        """

        for sock in w_clients:
            if sock in requests:
                try:
                    # отправляем сообщение всем подключенным клиентам
                    self.response.send(sock, requests[sock])

                except:  # Сокет недоступен, клиент отключился
                    print('Клиент write {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    all_clients.remove(sock)

    def listen_forever(self):
        """запускаем цикл обработки событий для всех клиентов"""

        while True:
            try:
                conn, addr = self.sock.accept()  # Проверка подключений
                # получаем сообщение от клиента
                msg = self.response.get(conn)
                # формируем ответ
                response = self.response.response(msg)
                # отправляем ответ клиенту
                self.response.send(conn, response)
            except OSError as e:
                pass  # timeout вышел
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                # Добавляем клиента в список
                self.clients.append(conn)
            finally:
                # Проверить наличие событий ввода-вывода
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = self.read_requests(r, w, self.clients)      # Получаем входные сообщения
                self.write_responses(requests, w, self.clients)     # Выполним отправку входящих сообщений

    def __del__(self):
        self.sock.close()


if __name__ == '__main__':
    """Получаем аргументы скрипта"""
    try:
        addr = sys.argv[1]
    except IndexError:
        addr = ''  # "127.0.0.1"
    try:
        port = int(sys.argv[2])
    except IndexError:
        port = PORT
    except ValueError:
        print('Порт должен быть целым числом')
        sys.exit(0)

    server = Server(addr, port)
    server.listen_forever()
