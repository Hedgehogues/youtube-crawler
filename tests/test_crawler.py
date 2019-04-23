import logging

from crawler import utils
from crawler.crawler import YoutubeCrawler
from crawler.utils import CrawlerError
from tests import full_descr_mock
from tests.utils import BaseTestClass, SubTest


class CacheMock:
    def __init__(self, get_best_channel_id, max_count_replace):
        self.__max_count_replace = max_count_replace
        self.__count_replace = 0
        self.__get_best_channel_id = get_best_channel_id

    def set_base_channels(self, channel_ids):
        pass

    def get_best_channel_id(self):
        if self.__count_replace == self.__max_count_replace:
            return None
        self.__count_replace += 1
        return self.__get_best_channel_id

    def set_channels(self, channel, scrapped=True, valid=True):
        if channel['full_descr'] is not None and type(channel['full_descr']) != str:
            raise utils.CacheError
        if channel['full_descr'] is not None and type(channel['short_descr']) != str:
            raise utils.CacheError


class DownloaderMock:
    pass


class ScrapperMock:

    def parse(self, _):
        return full_descr_mock


class TestScrapper(BaseTestClass):
    """
    """

    @staticmethod
    def __create_crawler(max_attempts, max_count_replace):
        crawler = YoutubeCrawler(
            cache=CacheMock(
                get_best_channel_id="MyChannelId",
                max_count_replace=max_count_replace,
            ),
            scraper=ScrapperMock(),
            ydl_loader=DownloaderMock(),
            max_attempts=max_attempts,
        )
        return crawler

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description="Channel ids is not list",
                args={'channel_ids': "MyChannelId"},
                object=self.__create_crawler(2, 2),
                want={},
                exception=CrawlerError,
            ),
            SubTest(
                name="Test 2",
                description="There are not any best channels",
                args={'channel_ids': ["MyChannelId"]},
                object=self.__create_crawler(2, 0),
                want=None,
                exception=None,
            ),
            # SubTest(
            #     name="Test 3",
            #     description="Channel ids is not list",
            #     args={'channel_ids': ["MyChannelId"]},
            #     object=self.__create_crawler(2, 2),
            #     want={},
            #     exception=None,
            # ),
        ]

    def test_parse(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.process(**kwargs))
