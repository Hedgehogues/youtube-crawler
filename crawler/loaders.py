import json
import requests
from copy import deepcopy
from enum import Enum
import youtube_dl

from crawler import utils
from crawler.utils import ReloadTokenError


class Tab(Enum):
    Channels = 'channels'
    HomePage = 'featured'
    Videos = 'videos'
    About = 'about'


class BaseLoader:
    def __init__(self):
        user_agent = \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
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
        if len(next_page_token['ctoken']) == 0:
            raise ReloadTokenError("ctoken length equal 0")
        if len(next_page_token['itct']) == 0:
            raise ReloadTokenError("itct length equal 0")
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

        data_config = self.__extractor(text, self.data_config, "Data config serialize is failed", ';\n')
        player_config = self.__extractor(text, self.player_config, "Player config serialize is failed", ');\n')

        return player_config, data_config

    @staticmethod
    def __extractor(text, config, msg, pattern_found):
        start_ind = text.find(config)+len(config)
        finish_ind = start_ind + text[start_ind:].find(pattern_found)
        config = text[start_ind:finish_ind]
        try:
            return json.loads(config)
        except Exception as e:
            raise utils.JsonSerializableError(msg, e)


class YoutubeDlLoader:
    def __init__(self, ydl_params=None):
        self._base_url = 'https://www.youtube.com/watch'

        ydl = youtube_dl.YoutubeDL({'listsubtitles': True})
        self._video_descr_extractor = ydl.get_info_extractor(youtube_dl.gen_extractors()[1125].ie_key())

        audio_ydl_params = ydl_params
        if audio_ydl_params is None:
            audio_ydl_params = {
                'writeautomaticsub': True,
                'outtmpl': 'data/videos/youtube/%(channel_id)s/%(id)s.wav',
                'format': 'bestaudio/best',
                'prefer-avconv': True,
                'subtitleslangs': ['ru'],
                'ext': 'wav',
                'simulate': False,
                'max_sleep_interval': 2,
                'sleep_interval': 1,
                'ignoreerrors': False,
            }
        self._audio_ydl = youtube_dl.YoutubeDL(audio_ydl_params)

    def load(self, video_id):
        # TODO: реализовать обкачку видео, инорфмацию по которым скачали
        # TODO: логгировать все статусы обкачки для того, чтобы можно было возобновить обкачку с прежнего места
        # TODO: заменить на кастомные обкачки, так как youtube-dl использует 2 обращения (за субтитрами и за видео)

        try:
            url = self._base_url + '?v=%s' % video_id
            descr = self._video_descr_extractor.extract(url)
            if 'ru' not in descr['automatic_captions']:
                return {}

            self._audio_ydl.download([url])
            return descr
        except Exception as e:
            raise utils.DownloadError(msg="Downloading was failed. VideoId: %s" % video_id, e=e)
