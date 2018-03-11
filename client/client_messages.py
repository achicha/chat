from datetime import datetime as dt


class JimClientMessage:
    """Client's requests protocol"""
    def auth(self, username, password):
        """
        Authorization message

        :param username:
        :param password:
        :return: dict with data
        """
        data = {
            "action": "authenticate",
            "time": dt.now().timestamp(),
            "user": {
                "account_name": username,
                "password": password
            }
        }
        return data

    def presence(self, sender, status="Yep, I am here!"):
        """
        Presence message, which notify server that client is online.
        :param sender: username
        :param status: some text
        :return: dict with data
        """
        data = {
            "action": "presence",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def quit(self, sender, status="disconnect"):
        """
        Quit message, which notify server that client want to disconnect

        :param sender: username
        :param status: some text
        :return: dict with data
        """
        data = {
            "action": "quit",
            "time": dt.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def list_(self, sender, status="show", person=''):
        """
        List message, which can add/delete/show contacts from user's ContactList

        :param sender: username
        :param status: possible statuses are: show/add/del
        :param person: user from contact list
        :return: dict with data
        """
        data = {
            "action": "list",
            "time": dt.now().timestamp(),
            "type": "status",
            "contact_list": 'No contacts yet',
            "user": {
                "account_name": sender,
                "status": status,
                "contact": person
            }
        }
        return data

    def message(self, sender, receiver='user1', text='some msg text'):
        """
        Simple message between two client's (client -> client)

        :param sender: username
        :param receiver: account name. message to
        :param text: message's text
        :return: dict with data
        """
        data = {
            "action": "msg",
            "time": dt.now().timestamp(),
            "to": receiver,
            "from": sender,
            "encoding": 'utf-8',
            "message": text
        }

        return data
