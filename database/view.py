from database.controller import ClientMessages
from database.models import CBase
from pprint import pprint as print

# todo CBase неправильно импортировать тут. патчить модели от сюда?


cm = ClientMessages('sqlite:///client_contacts.db', CBase, echo=False)

# add new client
cm.add_client('user_1', info='some info about user_1')
cm.add_client('user_2', info='some info about user_2')
cm.add_client('user_3')
cm.add_client('user_4')

# get_client_by_username
user1 = cm.get_client_by_username('user_1')
assert user1.username == 'user_1'

# add contact
cm.add_contact('user_1', 'user_2')
cm.add_contact('user_2', 'user_3')
cm.add_contact('user_2', 'user_1')
cm.add_contact('user_3', 'user_1')
contact42 = cm.add_contact('user_4', 'user_2')

# get_contacts
ans = cm.get_contacts('user_2')
for i in ans:
    print(i.contact)


# del contact
cm.del_contact('user_4', 'user_2')

# add client's history
cm.add_client_history('user_2', '8.8.8.8')

# get client's history
history = cm.get_client_history('user_2')
print(history)

# add client's message
cm.add_client_message('user_1', 'user_2', 'msg from 1 to 2')

# get client's messages
msgs = cm.get_client_messages('user_1')
print(msgs)
