import json
from enum import Enum

import requests


class Tab(Enum):
    Channels = 'channels'
    HomePage = 'featured'
    Videos = 'videos'
    Community = 'community'
    About = 'about'


def check_resp(resp):
    if resp.status_code != 200:
        raise Exception("Status code exception: %d. Url: %s" % (resp.status_code, resp.url))


def none_exception(arg, text="None exception"):
    if arg is None:
        raise Exception(text)


class Loader:
    def __init__(self):
        self._base_url = 'https://www.youtube.com/channel/'
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        accept_lang = 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
        cookie = 'VISITOR_INFO1_LIVE=t3zCqZs-6NA; _ga=GA1.2.1862333059.1547989835; _gid=GA1.2.366404146.1547989835; PREF=f5=30&al=en&cvdm=list&f1=50000000; YSC=KCsXvfHQG-I; GPS=1'
        self._headers = {
            'user-agent': user_agent,
            'accept-language': accept_lang,
            'cookie': cookie,
        }
        self._query_string = {}
        self.data_config = 'window["ytInitialData"] = '
        self.player_config = 'window["ytInitialPlayerResponse"] = (\n        '

    def load(self, channel_id, tab=Tab.HomePage):
        text = self.__get_resp_text(self._base_url + channel_id + '/' + tab.value)

        player_config = self.__get_player_config(text)
        data_config = self.__get_data_config(text)

        return player_config, data_config

    def __get_data_config(self, text):
        start_ind = text.find(self.data_config)+len(self.data_config)
        finish_ind = start_ind + text[start_ind:].find(';\n')
        config = text[start_ind:finish_ind]
        return json.loads(config)

    def __get_player_config(self, text):
        start_ind = text.find(self.player_config)+len(self.player_config)
        finish_ind = start_ind + text[start_ind:].find(');\n')
        config = text[start_ind:finish_ind]
        return json.loads(config)

    def __get_resp_text(self, url, params=None, headers=None, method='GET'):
        params = self._query_string if params is None else params
        headers = self._headers if headers is None else headers
        resp = requests.request(method, url, headers=headers, params=params)
        check_resp(resp)
        return resp.text


l = Loader()
print(l.load('UCSoYSTOt1g_Vdo8xCJeQpHw', Tab.HomePage))
