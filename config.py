import os
from dotenv import load_dotenv
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ADMINS = ['your-email@example.com']

    TELEGRAM_TOKEN = '761524778:AAERCT1vyEuNAjB15KcjT8vYpeW0Nq9sZGs'
    PROXY_URL = "http://127.0.0.1:8118"
    PROXYS_URL = "https://127.0.0.1:8118"

    CHAT_IDS = "341729967"  # группа OZONDS
    CHAT_ID = -341729967

    USER = 565696328

    SERVICES_LOG_LEVEL = logging.INFO
    SERVICES_BOT_LOG_LEVEL = logging.INFO


