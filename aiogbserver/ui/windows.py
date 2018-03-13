from PyQt5.QtWidgets import QMainWindow
from aiogbserver.ui.server_monitor_ui import Ui_ServerWindow as server_ui_class
# pyuic5 -x login.ui -o login_ui.py  # update UI file


class ServerMonitorWindow(QMainWindow):
    """Server Monitor Window (user interface)"""

    def __init__(self, parsed_args, server_instance, parent=None):
        super().__init__(parent)
        self.server_instance = server_instance
        self.parsed_args = parsed_args

        self.ui = server_ui_class()
        self.ui.setupUi(self)
        self.ui.refresh_action.triggered.connect(self.refresh_action)
        self.after_start()

    def closeEvent(self, event):
        """
        Close DB connection before exit (close window)
        :param event:
        :return:
        """
        self.server_instance._cm.dal.session.close()  # close DB connection

    def after_start(self):
        """do appropriate things after starting the App"""

        self.update_clients()

    def update_clients(self):
        """Update clients list"""

        contacts = self.server_instance.get_all_clients()
        self.ui.clients_list.clear()
        self.ui.clients_list.addItems([contact.username for contact in contacts])

    def update_history_messages(self, username):
        """
        Get all events from client's history.
        :param username:
        :return:
        """

        self.ui.msg_history_list.clear()
        msgs = self.server_instance.get_client_history(username)
        _resp = [m.time.strftime("%Y-%m-%d %H:%M:%S") + '_' + m.ip_addr + '_' + m.client.username for m in msgs]
        self.ui.msg_history_list.addItems(_resp)

    def on_clients_list_itemDoubleClicked(self):
        """Event, when double clicked on user in client's list
        -> update history and go to history tab"""
        selected_client = self.ui.clients_list.currentItem().text()
        self.update_history_messages(selected_client)
        self.ui.tabWidgetClients.setCurrentIndex(1)  # set history tab active

    def refresh_action(self):
        """refresh from menu
        QAction.triggered only work with direct connect() method,
        otherwise it will be triggered twice."""

        print('refresh')
        self.update_clients()
