import requests
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from config import Config


log_to_file = "toFile"
log_to_telegram = "toTelegram"


class TelegramHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        return self.send_totelegram(log_entry)

    def send_totelegram(self, message):
        address = Config.CHAT_ID  # Сообщение придёт в группу
        address = Config.USER  # Сообщение придёт в бот
        text = f"Сообщение в Телеграм:\n{message}"
        proxies = {
            "http": Config.PROXY_URL,
            "https": Config.PROXYS_URL,
        }
        print(f"TELEGRAM_TOKEN={Config.TELEGRAM_TOKEN}")
        print(f"v={address}")
        cont = requests.get(f"https://api.telegram.org/bot{Config.TELEGRAM_TOKEN}"
                            f"/sendMessage?chat_id={address}&text={text}", proxies=proxies).content
        return cont



def init_logging(config_class=Config):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    logger = logging.getLogger(log_to_file)
    logger.setLevel(logging.INFO)

    # Настройка логгера в файл. Логирование будет выполняться в папку log. Имя файла test.log
    # Каждый час будет создаваться новый файл. (Можно использовать другие стратегии)
    #  http://python-lab.blogspot.com/2013/03/blog-post.html
    #  https://docs.python.org/3/library/logging.html#logging.Logger
    file_handler = TimedRotatingFileHandler(f'logs/test.log', when='H', backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: [in %(pathname)s:%(lineno)d] %(funcName)s  %(message)s'))
    file_handler.setLevel(config_class.SERVICES_LOG_LEVEL)
    logger.addHandler(file_handler)

    logger.setLevel(config_class.SERVICES_LOG_LEVEL)

    host = f"api.telegram.org"
    address = Config.CHAT_ID
    text = "Ура заработало!!!!"
    url = f"bot{Config.TELEGRAM_TOKEN}/sendMessage?chat_id={address}&text={text}"
    telegram_handler = TelegramHandler()
    telegram_logger = logging.getLogger(log_to_telegram)
    telegram_logger.addHandler(telegram_handler)
    telegram_logger.setLevel(logging.INFO)

    return


if __name__ == '__main__':
    print(f" user ID={Config.USER}")
    init_logging(Config)
    log = logging.getLogger(log_to_file)
    log_telegram = logging.getLogger(log_to_telegram)
    log_telegram.info("Привет")



