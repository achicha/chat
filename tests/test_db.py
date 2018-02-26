from database.controller import ClientMessages
from database.models import CBase


class TestDatabase:
    def setup_class(self):
        """class setup"""
        self.cm = ClientMessages('sqlite:///:memory:', CBase, echo=False)

    def test_add_client(self):
        """add new client"""
        self.cm.add_client('user_1', info='some info about user_1')
        self.cm.add_client('user_2', info='some info about user_2')
        self.cm.add_client('user_3')
        self.cm.add_client('user_4')

        # get_client_by_username
        user1 = self.cm.get_client_by_username('user_1')
        user2 = self.cm.get_client_by_username('user_2')

        assert user1.username == 'user_1'
        assert user2.info == 'some info about user_2'

    def test_add_contact(self):
        """add contacts"""
        self.cm.add_contact('user_1', 'user_2')
        self.cm.add_contact('user_2', 'user_3')
        self.cm.add_contact('user_2', 'user_1')
        self.cm.add_contact('user_3', 'user_1')

        # get_contacts
        user1_contacts = self.cm.get_contacts('user_1')[0]
        assert user1_contacts.contact.username == 'user_2'

    def test_del_contact(self):
        """remove contacts"""
        self.cm.add_contact('user_4', 'user_2')
        user4_contacts = self.cm.get_contacts('user_4')[0]
        assert user4_contacts.contact.username == 'user_2'

        self.cm.del_contact('user_4', 'user_2')
        removed_user4_contacts = self.cm.get_contacts('user_4')
        assert removed_user4_contacts == []

    def test_add_client_history(self):
        """add client's history"""
        self.cm.add_client_history('user_2', '8.8.8.8')

        # get history
        history = self.cm.get_client_history('user_2')[0]
        assert history.client.username == 'user_2'

    def test_add_client_message(self):
        """add client's message"""
        self.cm.add_client_message('user_1', 'user_2', 'msg from 1 to 2')

        # get message
        msg = self.cm.get_client_messages('user_1')[0]
        assert msg.client.username == 'user_1'
