from crawler import utils
from tests import MockTab
from tests.utils import BaseTestClass, SubTest
import crawler.parsers as parsers


class MockJq:
    def __init__(self, fd):
        pass

    @staticmethod
    def transform(data_config):
        return data_config


class TestReloaderParser(BaseTestClass):
    __jq_path = 'data/jq_test.jq'

    def setUp(self):
        parsers.jq = MockJq
        self.tests_parse = [
            SubTest(
                name="Test 1",
                description="Invalid data_config. Problem with itct field",
                args={'data_config': {}, 'is_reload': False},
                object=parsers.ReloaderParser(
                    max_page=1,
                    tab=MockTab.TEST0,
                    jq_load_path=self.__jq_path,
                    jq_reload_path=self.__jq_path,
                ),
                exception=utils.ParserError,
            ),
            SubTest(
                name="Test 2",
                description="Invalid data_config. Problem with ctoken field",
                args={'data_config': {'next_page_token': {'itct': 'token'}}, 'is_reload': False},
                object=parsers.ReloaderParser(
                    max_page=1,
                    tab=MockTab.TEST0,
                    jq_load_path=self.__jq_path,
                    jq_reload_path=self.__jq_path,
                ),
                exception=utils.ParserError,
            ),
            SubTest(
                name="Test 3",
                description="Valid data config.",
                args={'data_config': {'next_page_token': {'itct': 'token', 'ctoken': 'token'}, MockTab.TEST0: []}, 'is_reload': False},
                object=parsers.ReloaderParser(
                    max_page=1,
                    tab=MockTab.TEST0,
                    jq_load_path=self.__jq_path,
                    jq_reload_path=self.__jq_path,
                ),
                want=([], {'ctoken': 'token', 'itct': 'token'}),
            ),
            SubTest(
                name="Test 4",
                description="Valid data config. There is not ctoken",
                args={'data_config': {'next_page_token': {'itct': 'token', 'ctoken': None}, MockTab.TEST0: []}, 'is_reload': False},
                object=parsers.ReloaderParser(
                    max_page=1,
                    tab=MockTab.TEST0,
                    jq_load_path=self.__jq_path,
                    jq_reload_path=self.__jq_path,
                ),
                want=([], None),
            ),
            SubTest(
                name="Test 5",
                description="Valid data config. There is not ctoken",
                args={'data_config': {'next_page_token': {'itct': None, 'ctoken': 'token'}, MockTab.TEST0: []}, 'is_reload': False},
                object=parsers.ReloaderParser(
                    max_page=1,
                    tab=MockTab.TEST0,
                    jq_load_path=self.__jq_path,
                    jq_reload_path=self.__jq_path,
                ),
                want=([], None),
            ),
        ]

        self.tests_is_final_page = []

    def test_parse(self):
        for i in range(len(self.tests_parse)):
            self.apply_test(i, lambda obj, kwargs: obj.parse(**kwargs))

    def test_is_final_page(self):
        for i in range(len(self.tests_is_final_page)):
            self.apply_test(i, lambda obj, kwargs: obj.is_final_page(**kwargs))
