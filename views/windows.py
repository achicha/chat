from PyQt5 import Qt, QtCore, QtGui, QtWidgets

from views.login_ui import Ui_Login_Dialog as login_ui_class
from views.contacts_ui import Ui_ContactsWindow as contacts_ui_class
from views.chat_ui import Ui_ChatMainWindow as chat_ui_class
from views.server_monitor_ui import Ui_ServerWindow as server_ui_class

from database.controller import ClientMessages
from database.models import CBase


class LoginWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.username = None

        self.ui = login_ui_class()
        self.ui.setupUi(self)

    def on_login_btn_pressed(self):
        """
        сахар для добавления слота: self.ui.login_btn.pressed.connect(self.press)
        """
        self.username = self.ui.username_text.text()
        if self.username:
            # тут можно сделать проверку на логин\пароль
            self.accept()
            print(self.username)
            print('login pressed')
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')


class ContactsWindow(QtWidgets.QMainWindow):
    def __init__(self, db_path, user_name, parent=None):
        super().__init__(parent)

        self.ui = contacts_ui_class()
        self.ui.setupUi(self)
        self.ui.actionExit.triggered.connect(self.actionExit)

        self.cm = ClientMessages(db_path, CBase, echo=False)
        self.username = user_name
        self.after_start()

    def keyPressEvent(self, event):
        """обрабатываем нажатие на клавиатуре"""
        if event.key() == QtCore.Qt.Key_Enter:
            # here accept the event and do something
            self.on_add_new_contact_btn_pressed()
            event.accept()
        else:
            event.ignore()

    def after_start(self):
        """do appropriate things after starting the App"""

        if not self.cm.get_client_by_username(self.username):
            self.cm.add_client(self.username)  # add new client
        else:
            self.update_contacts(self.username)  # update list
        # add client's history row
        self.cm.add_client_history(self.username)

    def update_contacts(self, client_username):
        """обновление контакт листа"""
        contacts = self.cm.get_contacts(client_username)
        self.ui.all_contacts.clear()
        self.ui.all_contacts.addItems([contact.contact.username for contact in contacts])

    def on_add_new_contact_btn_pressed(self):
        contact_username = self.ui.new_contact_name.text()

        if contact_username:
            _resp = self.cm.add_contact(self.username, contact_username)
            if not _resp:
                # если контакт успешно добавлен
                self.update_contacts(self.username)
                self.ui.new_contact_name.clear()
            else:
                print(_resp)

    def on_delete_contact_btn_pressed(self):
        try:
            selected_contact = self.ui.all_contacts.currentItem().text()
        except AttributeError:
            print('wrong contact')

        _resp = self.cm.del_contact(self.username, selected_contact)

        if not _resp:
            # контакт успешно удален
            self.update_contacts(self.username)
        else:
            print(_resp)

    def on_all_contacts_itemDoubleClicked(self):
        chat_wnd = ChatWindow(self)
        chat_wnd.show()

    def actionExit(self):
        print('exit')
        self.close()


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = chat_ui_class()
        self.ui.setupUi(self)

        self.parent_window = parent   # bind parent's window attributes
        self.contact_username = self.parent_window.ui.all_contacts.currentItem().text()
        self.username = self.parent_window.username
        self.cm = self.parent_window.cm
        self.update_chat()

    def keyPressEvent(self, event):
        """обрабатываем нажатие на клавиатуре"""
        if event.key() == QtCore.Qt.Key_Enter:
            # here accept the event and do something
            self.on_send_btn_pressed()
            event.accept()
        elif event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            event.ignore()

    def update_chat(self):
        """получаем все новые сообщения из БД"""
        self.ui.chat_window.clear()
        client_msgs = [c for c in self.cm.get_client_messages(self.username) if c.contact.username == self.contact_username]
        contact_msgs = [c for c in self.cm.get_client_messages(self.contact_username) if c.contact.username == self.username]
        msgs = sorted(client_msgs + contact_msgs, key=lambda x: x.time)  # all messages between client and contact

        for msg in msgs[:20]:  # show last 20 messages
            sender = msg.client.username
            if msg.client.username == self.username:
                sender = 'me'

            self.ui.chat_window.addItem('{} from {}: {}'.format(msg.time.strftime("%Y-%m-%d %H:%M:%S"),
                                                                sender, msg.message))

    def on_send_btn_pressed(self):
        """записываем сообщение в БД"""
        msg = self.ui.send_text.text()
        print('1', msg)
        if msg:
            self.cm.add_client_message(self.username, self.contact_username, msg)   # add msg to DB
            self.update_chat()
            self.ui.send_text.clear()


class ServerMonitorWindow(QtWidgets.QMainWindow):
    def __init__(self, db_path, parent=None):
        super().__init__(parent)

        self.ui = server_ui_class()
        self.ui.setupUi(self)
        self.ui.refresh_action.triggered.connect(self.refresh_action)

        self.cm = ClientMessages(db_path, CBase, echo=False)
        self.after_start()

    def after_start(self):
        """do appropriate things after starting the App"""
        self.update_clients()

    def update_clients(self):
        """обновление контакт листа"""
        contacts = self.cm.get_all_clients()
        self.ui.clients_list.clear()
        self.ui.clients_list.addItems([contact.username for contact in contacts])

    def update_history_messages(self, username):
        self.ui.msg_history_list.clear()
        msgs = self.cm.get_client_history(username)
        _resp = [m.time.strftime("%Y-%m-%d %H:%M:%S") + '_' + m.ip_addr + '_' + m.client.username for m in msgs]
        self.ui.msg_history_list.addItems(_resp)

    def on_clients_list_itemDoubleClicked(self):
        selected_client = self.ui.clients_list.currentItem().text()
        self.update_history_messages(selected_client)
        self.ui.tabWidgetClients.setCurrentIndex(1)  # set history tab active

    def refresh_action(self):
        """refresh from menu
        QAction.triggered only work with direct connect() method,
        otherwise it will be triggered twice."""
        print('refresh')
        self.update_clients()