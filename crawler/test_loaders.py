import json
import unittest
from collections import namedtuple

from crawler import utils
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
        dheaders = set(self.headers.items()) - set(headers.items())
        dparams = set(self.params.items()) - set(params.items())
        if method != self.method or url != self.url or len(dheaders) != 0 or len(dparams) != 0:
            return self.Resp(status_code=404, text=self.answ)
        return self.Resp(status_code=200, text=self.answ)


class TestLoaderBaseClass(unittest.TestCase):
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

        self.url = 'https://test.ru'
        self.answ = '{"Ok": true}'
        self.params = {'test': 'test'}
        self.headers = headers
        self.method = 'GET'

        loaders.requests = MockRequests(
            answ=self.answ, url=self.url, params=self.params, headers=self.headers, method=self.method
        )


class TestReloader(TestLoaderBaseClass):

    def test_load_0(self):
        """
        This test checks correct loading next page with VALID json.
        Token was found and token CORRECT.
        :return:
        """
        loaders.requests.url = 'https://www.youtube.com/browse_ajax/'
        next_page_token = {'ctoken': '123', 'itct': '456'}
        loaders.requests.params = {
            'ctoken': next_page_token['ctoken'],
            'continuation': next_page_token['ctoken'],
            'itct': next_page_token['itct'],
        }
        resp_text = loaders.Reloader().load(next_page_token)
        self.assertEqual(resp_text, json.loads(self.answ))

    def test_load_1(self):
        """
        This test checks correct loading next page with INVALID json.
        Token was found and token CORRECT.
        :return:
        """
        loaders.requests.url = 'https://www.youtube.com/browse_ajax/'
        next_page_token = {'ctoken': '123', 'itct': '456'}
        loaders.requests.params = {
            'ctoken': next_page_token['ctoken'],
            'continuation': next_page_token['ctoken'],
            'itct': next_page_token['itct'],
        }
        loaders.requests.answ += '1'
        self.assertRaises(utils.JsonSerializableError, loaders.Reloader().load, next_page_token)

    def test_load_2(self):
        """
        This test checks correct loading next page with VALID json.
        Token was not found - 1.
        :return:
        """
        loaders.requests.url = 'https://www.youtube.com/browse_ajax/'
        next_page_token = {'ctoken': '123', 'itct': ''}
        loaders.requests.params = {
            'ctoken': next_page_token['ctoken'],
            'continuation': next_page_token['ctoken'],
            'itct': next_page_token['itct'],
        }
        self.assertRaises(utils.ReloadTokenError, loaders.Reloader().load, next_page_token)

    def test_load_3(self):
        """
        This test checks correct loading next page with VALID json.
        Token was not found - 2.
        :return:
        """
        loaders.requests.url = 'https://www.youtube.com/browse_ajax/'
        next_page_token = {'ctoken': '', 'itct': '456'}
        loaders.requests.params = {
            'ctoken': next_page_token['ctoken'],
            'continuation': next_page_token['ctoken'],
            'itct': next_page_token['itct'],
        }
        self.assertRaises(utils.ReloadTokenError, loaders.Reloader().load, next_page_token)


class TestBaseLoader(TestLoaderBaseClass):

    def test__get_resp_text_0(self):
        """
        This test checks correct answer for get-request. Empty header
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
        This test checks correct answer for post-request. Empty header
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
        This test checks exception generate. Fill header
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
