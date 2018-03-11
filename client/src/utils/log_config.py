import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler
from functools import wraps


# create log path
LOG_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'logs')
os.makedirs(LOG_PATH, 0o777, exist_ok=True)

# create logger
LOGGER_NAME = sys.argv[0].split('/')[-1].split('.')[0]  # use script's name
logger = logging.getLogger(LOGGER_NAME)


# create formatter
class CustomFormatter(logging.Formatter):
    """Custom formatter, overrides if it exists:
        funcName with value of real_funcName,
        module with value of real_module
    """
    def format(self, record):
        if hasattr(record, 'real_funcName'):
            record.funcName = record.real_funcName
        if hasattr(record, 'real_module'):
            record.module = record.real_module
        return super(CustomFormatter, self).format(record)


_format = CustomFormatter("%(asctime)-10s %(levelname)s %(module)s.%(funcName)s() >>> %(message)s")


# create FileHandler
log_fn = os.path.join(LOG_PATH, LOGGER_NAME)
file_handler = TimedRotatingFileHandler(log_fn, when='d', interval=1,
                                        backupCount=7, encoding='utf-8', delay=False, utc=True, atTime=None)
file_handler.suffix = "%Y-%m-%d.log"
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(_format)

# create ErrorHandler
error_handler = logging.StreamHandler(sys.stderr)
error_handler.setLevel(logging.CRITICAL)
error_handler.setFormatter(_format)

# add handlers
logger.addHandler(file_handler)
logger.addHandler(error_handler)

# set logger level
logging.getLogger(LOGGER_NAME).setLevel(logging.DEBUG)


def log(func):
    """декоратор @log, фиксирующий обращение к декорируемой функции:
    сохраняет имя функции и её аргументы.
    """
    @wraps(func)
    def call(*args, **kwargs):
        # Calling decorated function
        res = func(*args, **kwargs)
        params = {
            'fname': func.__name__,
            'args': args,
            'kwargs': kwargs
        }
        logger.info('fname: %(fname)s, args: %(args)s, kwargs: %(kwargs)s', params,
                    extra={'real_funcName': func.__name__,
                           'real_module': func.__module__})  # use extra to override decorated args
        return res
    return call


if __name__ == '__main__':
    # test
    @log
    def f(a,b):
        return a+b

    import time
    for i in range(3):
        f(2,3)
        logger.info('hi there!')
        time.sleep(5)

