from datetime import datetime as dt
from sqlalchemy.exc import IntegrityError

from aiogbserver.database.db_connector import DataAccessLayer
from aiogbserver.database.models import Client, History, Messages, Contacts


class ClientMessages:
    def __init__(self, conn_string, base, echo):
        """создать подключение к БД"""
        self.dal = DataAccessLayer(conn_string, base, echo=echo)
        self.dal.connect()
        self.dal.session = self.dal.Session()

    def add_client(self, username, password, info=None):
        """Добавление клиента"""
        if self.get_client_by_username(username):
            return 'Username {} already exists'.format(username)
        else:
            new_user = Client(username=username, password=password, info=info)
            self.dal.session.add(new_user)
            self.dal.session.commit()
            print('Client added: {}'.format(new_user))

    def get_client_by_username(self, username):
        """Получение клиента по имени"""
        client = self.dal.session.query(Client).filter(Client.username == username).first()
        return client

    def add_contact(self, client_username, contact_username):
        """Добавление контакта"""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                new_contact = Contacts(client_id=client.id, contact_id=contact.id)
                try:
                    self.dal.session.add(new_contact)
                    self.dal.session.commit()
                    print('Contact added: {}'.format(new_contact))
                except IntegrityError as err:
                    print('IntegrityError error: {}'.format(err))
                    self.dal.session.rollback()
            else:
                return 'Client {} does not exists'.format(client_username)
        else:
            return 'Contact {} does not exists'.format(contact_username)

    def del_contact(self, client_username, contact_username):
        """Добавление контакта"""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                remove_contact = self.dal.session.query(Contacts) \
                    .filter((Contacts.client_id == client.id)
                            & (Contacts.contact_id == contact.id)) \
                    .first()
                self.dal.session.delete(remove_contact)
                self.dal.session.commit()
                print('Contact removed: {}'.format(remove_contact))
            else:
                return 'Client {} does not exists'.format(client_username)
        else:
            return 'Contact {} does not exists'.format(contact_username)

    def get_contacts(self, client_username):
        """Получение контактов клиента"""
        client = self.get_client_by_username(client_username)
        if client:
            return self.dal.session.query(Contacts)\
                    .join(Client, Contacts.client_id == Client.id)\
                    .filter(Client.username == client_username).all()
        return 'Client {} does not exists'.format(client_username)

    def get_all_clients(self):
        """Получение списка всех зарегистрированных пользователей"""
        return self.dal.session.query(Client).all()

    def add_client_history(self, client_username, ip_addr='8.8.8.8'):
        """добавление истории клиента"""
        client = self.get_client_by_username(client_username)
        if client:
            new_history = History(ip_addr=ip_addr, client_id=client.id)
            try:
                self.dal.session.add(new_history)
                self.dal.session.commit()
                print('History added: {}'.format(new_history))
            except IntegrityError as err:
                print('IntegrityError error: {}'.format(err))
                self.dal.session.rollback()

        return 'Client {} does not exists'.format(client_username)

    def get_client_history(self, client_username):
        """получение истории входов клиента на сервер"""
        client = self.get_client_by_username(client_username)
        if client:
            return self.dal.session.query(History)\
                .filter(History.client_id == client.id).all()
        return 'Client {} does not exists'.format(client_username)

    def add_client_message(self, client_username, contact_username, text_msg):
        """бекап сообщения клиента"""
        client = self.get_client_by_username(client_username)
        contact = self.get_client_by_username(contact_username)
        if client and contact:
            new_msg = Messages(client_id=client.id, contact_id=contact.id, message=text_msg, time=dt.now())
            try:
                self.dal.session.add(new_msg)
                self.dal.session.commit()
                print('New message added: {}'.format(new_msg))
            except IntegrityError as err:
                print('IntegrityError error: {}'.format(err))
                self.dal.session.rollback()
        return 'Client {} does not exists'.format(client_username)

    def get_client_messages(self, client_username):
        """Получение всех сообщений от клиента"""
        client = self.get_client_by_username(client_username)
        if client:
            return self.dal.session.query(Messages)\
                .filter(Messages.client_id == client.id).all()
        return 'Client {} does not exists'.format(client_username)

    def set_user_online(self, client_username):
        """
         Set status to online
        :param client_username:
        :return:
        """
        client = self.get_client_by_username(client_username)
        if client:
            client.online_status = True
            self.dal.session.commit()
        return 'Client {} does not exists'.format(client_username)

    def set_user_offline(self, client_username):
        """
         Set status to offline
        :param client_username:
        :return:
        """
        client = self.get_client_by_username(client_username)
        if client:
            client.online_status = False
            self.dal.session.commit()
        return 'Client {} does not exists'.format(client_username)

    def get_user_status(self, client_username):
        client = self.get_client_by_username(client_username)
        return client.online_status
