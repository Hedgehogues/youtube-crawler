import requests
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler
import os
from config import Config


def init_logging(config_class=Config):
    print(f"init_logging")
    # if not appl.debug and not appl.testing:
    #     print("app_init 2")
    #     if appl.config['LOG_TO_STDOUT']:
    #         print("app_init 2.1")
    #         stream_handler = logging.StreamHandler()
    #         stream_handler.setLevel(config_class.SERVICES_LOG_LEVEL)
    #         appl.logger.addHandler(stream_handler)
    #     else:
    #         print("app_init 2.2")
    #         if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #         # file_handler = RotatingFileHandler(f'logs/telegramgate_{len(appl.logger.handlers)}.log', maxBytes=10240, backupCount=10)
    #         file_handler = TimedRotatingFileHandler(f'logs/telegramgate_{len(appl.logger.handlers)}.log', when='H', backupCount=10)
    #         file_handler.setFormatter(logging.Formatter(
    #             '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d] %(funcName)s'))
    #         file_handler.setLevel(config_class.SERVICES_LOG_LEVEL)
    #         appl.logger.addHandler(file_handler)
    #
    #     print("app_init 3")
    # print(f" logger.handlers.size={len(appl.logger.handlers)}")
    #
    # appl.logger.setLevel(config_class.SERVICES_LOG_LEVEL)
    # appl.logger.info('\tTelegramGate СТАРТ')
    print("init_logging exit")

    return
    # return



def send_totelegram():

    tg.app.logger.info("totelegramfrom1c")
    if rq.remote_user is None:
        remote_user = dbg_user
    else:
        remote_user = rq.remote_user
    user = remote_user.split("@")
    tg.app.logger.info("totelegramfrom1c")
    items = rq.args
    tg.app.logger.debug(f"\titems\n{items}")
    address = None
    if "userid" in rq.args.keys():
        address = rq.args['userid']
    else:
        address = tg.app.config['CHAT_ID']
    text = f"1C документооборот:\n{rq.args['info']}\n{rq.args['message']}"
    proxies = {
        "http": tg.app.config['PROXY_URL'],
        "https": tg.app.config['PROXYS_URL'],
    }
    requests.get(f"https://api.telegram.org/bot{tg.app.config['TELEGRAM_TOKEN']}"
                 f"/sendMessage?chat_id={address}&text={text}", proxies=proxies)
    response = jsonify(dict())
    response.status_code = 200
    return response


print("telegrameGate 1")

if __name__ == '__main__':
    print(f" user ID={Config.USER}")
    init_logging(Config)

