import unittest
from collections import namedtuple

from crawler.loaders import BaseLoader
import crawler.loaders as loaders


class MockRequests:
    Resp = namedtuple('resp', ['status_code', 'text'])

    def __init__(self, answ, url, headers=None, params=None, method='GET'):
        self.method = method
        self.url = url
        self.headers = headers if headers is None else headers
        self.params = {} if params is None else params
        self.answ = answ

    def request(self, method, url, headers, params):
        if method != self.method or url != self.url or headers != self.headers or params != self.params:
            return self.Resp(status_code=404, text=self.answ)
        return self.Resp(status_code=200, text=self.answ)


class TestBaseLoader(unittest.TestCase):
    def setUp(self):
        user_agent = \
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        cache_control = 'no-cache'
        x_youtube_client_name = '1'
        x_youtube_client_version = '2.20190124'

        headers = {
            'user-agent': user_agent,
            'cache-control': cache_control,
            'x-youtube-client-name': x_youtube_client_name,
            'x-youtube-client-version': x_youtube_client_version,
        }

        self.url = 'http://test.ru'
        self.answ = 'OK'
        self.params = {}
        self.headers = headers
        self.method = 'GET'

    def test__get_resp_text_0(self):
        """
        This test checks correct answer for get-request
        :return:
        """
        self.headers = {}
        self.method = 'GET'
        loaders.requests = MockRequests(
            answ=self.answ, url=self.url, params=self.params, headers=self.headers, method=self.method
        )
        resp_text = BaseLoader()._get_resp_text(
            url=self.url, params=self.params, headers=self.headers, method=self.method
        )
        self.assertEqual(resp_text, self.answ)

    def test__get_resp_text_1(self):
        """
        This test checks correct answer for post-request
        :return:
        """
        self.headers = {}
        self.method = 'POST'
        loaders.requests = MockRequests(
            answ=self.answ, url=self.url, params=self.params, headers=self.headers, method=self.method
        )
        resp_text = BaseLoader()._get_resp_text(
            url=self.url, params=self.params, headers=self.headers, method=self.method
        )
        self.assertEqual(resp_text, self.answ)

    def test__get_resp_text_3(self):
        """
        This test checks exception generate
        :return:
        """
        self.method = 'POST'
        loaders.requests = MockRequests(
            answ=self.answ, url=self.url, params=self.params, headers=self.headers, method=self.method
        )
        self.assertRaises(
            Exception,
            BaseLoader()._get_resp_text,
            url=self.url, params=self.params, headers={}, method=self.method
        )
