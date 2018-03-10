import os


PORT = 14908         # port. ибо достали зомби процессы :)
ENCODING = 'utf-8'   # Кодировка

DB_PROTOCOL = 'sqlite:///'
DB_NAME = '/database/client_contacts.db'
DB_PATH = DB_PROTOCOL + os.path.dirname(os.path.abspath(__file__)) + DB_NAME