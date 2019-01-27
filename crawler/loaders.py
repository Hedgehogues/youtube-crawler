import json
from copy import deepcopy
from enum import Enum
import requests

from crawler import utils


class Tab(Enum):
    Channels = 'channels'
    HomePage = 'featured'
    Videos = 'videos'
    About = 'about'


class BaseLoader:
    def __init__(self):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        cache_control = 'no-cache'
        x_youtube_client_name = '1'
        x_youtube_client_version = '2.20190124'

        self._headers = {
            'user-agent': user_agent,
            'cache-control': cache_control,
            'x-youtube-client-name': x_youtube_client_name,
            'x-youtube-client-version': x_youtube_client_version,
        }

    def _get_resp_text(self, url, params=None, headers=None, method='GET'):
        try:
            params = {} if params is None else params
            headers = self._headers if headers is None else headers
            resp = requests.request(method, url, headers=headers, params=params)
        except Exception as e:
            raise utils.RequestError("Connection is failed", e)
        utils.check_resp(resp)
        return resp.text


class Reloader(BaseLoader):
    def __init__(self):
        super().__init__()
        self._base_url = 'https://www.youtube.com/browse_ajax/'

    def load(self, next_page_token):
        headers = deepcopy(self._headers)
        query_params = {
            'ctoken': next_page_token['ctoken'],
            'continuation': next_page_token['ctoken'],
            'itct': next_page_token['itct'],
        }

        config = self._get_resp_text(self._base_url, headers=headers, params=query_params)
        try:
            return json.loads(config)
        except Exception as e:
            raise utils.JsonSerializableError("Reload page config serialize is failed", e)


class Loader(BaseLoader):
    def __init__(self):
        super().__init__()
        self._base_url = 'https://www.youtube.com/channel/'
        self.data_config = 'window["ytInitialData"] = '
        self.player_config = 'window["ytInitialPlayerResponse"] = (\n        '

    def load(self, channel_id, tab=Tab.HomePage, query_params=None):
        text = self._get_resp_text(self._base_url + channel_id + '/' + tab.value, params=query_params)

        player_config = self.__get_player_config(text)
        data_config = self.__get_data_config(text)

        return player_config, data_config

    def __get_data_config(self, text):
        try:
            start_ind = text.find(self.data_config)+len(self.data_config)
            finish_ind = start_ind + text[start_ind:].find(';\n')
            config = text[start_ind:finish_ind]
        except Exception as e:
            raise utils.JsonExtractionError("Data config extraction is failed", e)
        try:
            return json.loads(config)
        except Exception as e:
            raise utils.JsonSerializableError("Data config serialize is failed", e)

    def __get_player_config(self, text):
        try:
            start_ind = text.find(self.player_config)+len(self.player_config)
            finish_ind = start_ind + text[start_ind:].find(');\n')
            config = text[start_ind:finish_ind]
        except Exception as e:
            raise utils.JsonExtractionError("Player config extraction is failed", e)
        try:
            return json.loads(config)
        except Exception as e:
            raise utils.JsonSerializableError("Player config serialize is failed", e)
