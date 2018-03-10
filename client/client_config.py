"""Константы для jim протокола, настройки"""
# Ключи
# import os

# ACTION = 'action'
# TIME = 'time'
# USER = 'user'
# ACCOUNT_NAME = 'account_name'
# RESPONSE = 'response'
# ERROR = 'error'
#
# # Значения
# PRESENCE = 'presence'
# MESSAGE = 'msg'
#
# # Коды ответов (будут дополняться)
# BASIC_NOTICE = 100
# OK = 200
# ACCEPTED = 202
# WRONG_REQUEST = 400  # неправильный запрос/json объект
# SERVER_ERROR = 500
#
# # Кортеж из кодов ответов
# RESPONSE_CODES = (BASIC_NOTICE, OK, ACCEPTED, WRONG_REQUEST, SERVER_ERROR)


PORT = 14908         # port. ибо достали зомби процессы :)
ENCODING = 'utf-8'   # Кодировка

#DB_PATH = DB_PROTOCOL + os.path.dirname(os.path.abspath(__file__)) + DB_NAME
DB_PATH = 'sqlite:////home/achicha/PyProjects/Github/chat/server/database/client_contacts.db'