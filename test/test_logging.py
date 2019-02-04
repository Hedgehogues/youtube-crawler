import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import os
from config import Config

nameModule = "nameModule"


def init_logging1(config_class=Config):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger(nameModule)
    logger.setLevel(logging.INFO)

    # file_handler = RotatingFileHandler(f'logs/telegramgate_{len(appl.logger.handlers)}.log', maxBytes=10240, backupCount=10)
    file_handler = TimedRotatingFileHandler(f'logs/test.log', when='H', backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: [in %(pathname)s:%(lineno)d] %(funcName)s  %(message)s'))
    file_handler.setLevel(config_class.SERVICES_LOG_LEVEL)
    logger.addHandler(file_handler)

    logger.setLevel(config_class.SERVICES_LOG_LEVEL)

    return


def out_log_messages(log_level):
    log = logging.getLogger(nameModule)
    log.critical(f' ======================= log level={log_level}')
    log.setLevel(log_level)
    log.info("This is an info message")
    # Сообщение отладочное
    log.debug('This is a debug message')
    # Сообщение информационное
    log.info('This is an info message')
    # Сообщение предупреждение
    log.warning('This is a warning')
    # Сообщение ошибки
    log.error('This is an error message')
    # Сообщение критическое
    log.critical('FATAL!!!')
    log.log(1, 'low level message')
    log.debug("debug message")
    log.info("info message")
    log.warning("warn message")
    log.error("error message")
    try:
        a = 1/0
    except:
        log.exception("exception message")
    log.critical("critical message")

if __name__ == '__main__':
    init_logging1(Config)
    log = logging.getLogger(nameModule)
    out_log_messages(logging.INFO)
    out_log_messages(logging.DEBUG)
    out_log_messages(logging.ERROR)

