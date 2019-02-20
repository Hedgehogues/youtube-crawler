from collections import Counter
from enum import Enum

from crawler.scrapper import Scrapper
from tests import MockLogger
from tests.utils import BaseTestClass, SubTest


class MockTab(Enum):
    TEST0 = "test0"
    TEST1 = "test1"
    TEST2 = "test2"


class MockClientServer:
    def __init__(self, available_pages=None):
        self.available_pages = {} if available_pages is None else available_pages
        self.tabs = Counter()

    def is_cur_page_last(self, tab):
        if tab not in self.available_pages:
            raise Exception()
        if self.tabs[tab] + 1 >= self.available_pages[tab]:
            return True
        self.tabs[tab] += 1
        return False


class MockLoader:
    def __init__(self, client):
        self.client = client

    def load(self, channel_id, tab, query_params):
        token = None
        if not self.client.is_cur_page_last(tab):
            token = tab
        return {'Player': True}, {'Load': True, 'Token': token}


class MockReloader:
    def __init__(self, client):
        self.client = client

    def load(self, next_page_token):
        token = None
        if not self.client.is_cur_page_last(next_page_token):
            token = next_page_token
        return {'Load': True, 'Token': token}


class MockParser:
    def __init__(self, tab, max_pages):
        self.tab = tab
        self.max_page = max_pages

    def parse(self, player_config, data_config):
        return {
                   'player_config': player_config,
                   'data_config': data_config,
               }, data_config['Token']

    def reload_parse(self, data_config):
        return {'data_config': data_config}, data_config['Token']


class TestScrapper(BaseTestClass):
    """
    Token save information about next page
    """

    @staticmethod
    def __create_scrapper(available_pages, max_pages):
        client = MockClientServer(available_pages=available_pages)
        scrapper = Scrapper(
            loader=MockLoader(client),
            reloader=MockReloader(client),
            parsers=[MockParser(tab=tab, max_pages=max_pages[tab]) for tab in max_pages],
            logger=MockLogger()
        )
        for k in max_pages:
            scrapper.query_params[k] = k
        return scrapper

    def setUp(self):
        channel_id = "test_channel"

        self.tests = [
            # There are not parsers
            SubTest(
                name="Test 1",
                description="There aren't any parsers. Function does execute and return after that",
                configuration={'available_pages': [], 'max_pages': []},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={},
                    max_pages={},
                ),
                want={},
                exception=None,
            ),
            # One parsers
            SubTest(
                name="Test 2",
                description="One parser",
                configuration={'available_pages': [1], 'max_pages': [1]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 1},
                    max_pages={MockTab.TEST0: 1},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}}
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 3",
                description="One parser",
                configuration={'available_pages': [1], 'max_pages': [2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 1},
                    max_pages={MockTab.TEST0: 2},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}}
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 4",
                description="One parser",
                configuration={'available_pages': [2], 'max_pages': [2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 2},
                    max_pages={MockTab.TEST0: 2},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 5",
                description="One parser",
                configuration={'available_pages': [2], 'max_pages': [3]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 2},
                    max_pages={MockTab.TEST0: 3},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 6",
                description="One parser",
                configuration={'available_pages': [3], 'max_pages': [2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 3},
                    max_pages={MockTab.TEST0: 2},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                    ]
                },
                exception=None,
            ),
            # Two parsers
            SubTest(
                name="Test 7",
                description="Two parser. The same configuration",
                configuration={'available_pages': [1, 1], 'max_pages': [1, 1]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 1, MockTab.TEST1: 1},
                    max_pages={MockTab.TEST0: 1, MockTab.TEST1: 1},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 8",
                description="Two parser. The same configuration",
                configuration={'available_pages': [1, 1], 'max_pages': [2, 2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 1, MockTab.TEST1: 1},
                    max_pages={MockTab.TEST0: 2, MockTab.TEST1: 1},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}}
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}}
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 9",
                description="Two parser. The same configuration",
                configuration={'available_pages': [2, 2], 'max_pages': [2, 2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 2, MockTab.TEST1: 2},
                    max_pages={MockTab.TEST0: 2, MockTab.TEST1: 2},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 10",
                description="Two parser. The same configuration",
                configuration={'available_pages': [2, 2], 'max_pages': [3, 3]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 2, MockTab.TEST1: 2},
                    max_pages={MockTab.TEST0: 3, MockTab.TEST1: 3},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 11",
                description="Two parser. The same configuration",
                configuration={'available_pages': [3, 3], 'max_pages': [2, 2]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 3, MockTab.TEST1: 3},
                    max_pages={MockTab.TEST0: 2, MockTab.TEST1: 2},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 12",
                description="Two parser. Different configuration",
                configuration={'available_pages': [3, 4], 'max_pages': [2, 4]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 3, MockTab.TEST1: 4},
                    max_pages={MockTab.TEST0: 2, MockTab.TEST1: 4},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ]
                },
                exception=None,
            ),
            SubTest(
                name="Test 13",
                description="Three parser",
                configuration={'available_pages': [3, 4, 1], 'max_pages': [2, 4, 1]},
                args={'channel_id': channel_id},
                object=self.__create_scrapper(
                    available_pages={MockTab.TEST0: 3, MockTab.TEST1: 4, MockTab.TEST2: 1},
                    max_pages={MockTab.TEST0: 2, MockTab.TEST1: 4, MockTab.TEST2: 1},
                ),
                want={
                    MockTab.TEST0: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST0}},
                    ],
                    MockTab.TEST1: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': MockTab.TEST1}},
                        {'data_config': {'Load': True, 'Token': None}},
                    ],
                    MockTab.TEST2: [
                        {'player_config': {'Player': True}, 'data_config': {'Load': True, 'Token': None}},
                    ],
                },
                exception=None,
            ),
        ]

    def test_parse(self):
        for i in range(len(self.tests)):
            self._apply_test(i)
