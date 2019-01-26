import json
import re

import requests
import youtube_dl


class BaseYoutubeDL(youtube_dl.YoutubeDL):
    def __init__(self, params):
        super().__init__(params)
        self._headers = {
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'VISITOR_INFO1_LIVE=t3zCqZs-6NA; _ga=GA1.2.1862333059.1547989835; _gid=GA1.2.366404146.1547989835; PREF=f5=30&al=en&cvdm=list&f1=50000000; YSC=KCsXvfHQG-I; GPS=1',
        }
        self._query_string = {}
        self._urls_channels = []
        self._any_symbols = '.*?'
        self._numerics = '\d+'
        self._prefixes = {}
        self._suffixes = {}
        self._target = {}

    @staticmethod
    def _check_resp(resp):
        if resp.status_code != 200:
            raise Exception("")

    @staticmethod
    def _none_exception(arg):
        if arg is None:
            raise Exception("")

    def _extract_regexp_substr(self, text, name):
        start_str = 'window["ytInitialData"] = '
        finish_str = ';\n    window["ytInitialPlayerResponse"]'
        start_ind = text.find(start_str)
        finish_ind = text.find(finish_str)
        x = json.loads(text[start_ind + len(start_str):finish_ind])
        regexp_prefix = self._prefixes[name]
        regexp_suffix = self._suffixes[name]
        regexp_target = self._target[name]
        candidate_str = re.findall(regexp_prefix + regexp_target + regexp_suffix, text)
        if len(candidate_str) == 0:
            return None
        if len(candidate_str) != 1:
            raise Exception("")
        target_str = candidate_str[0][len(regexp_prefix):-len(regexp_suffix)]
        if len(target_str) == 0:
            raise Exception("")
        return target_str

    def _get_resp_text(self, url, params=None, headers=None, method='GET'):
        params = self._query_string if params is None else params
        headers = self._headers if headers is None else headers
        resp = requests.request(method, url, headers=headers, params=params)
        self._check_resp(resp)
        return resp.text
