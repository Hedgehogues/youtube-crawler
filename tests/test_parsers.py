from crawler import utils
from tests import MockTab
from tests.utils import BaseTestClass, SubTest
import crawler.parsers as parsers


mockTab = MockTab.TEST0


class MockJq:
    def __init__(self, s):
        self.s = s

    def transform(self, data_config):
        data_config[mockTab].append(self.s)
        return data_config


class MockOpen:
    def __init__(self, s):
        self.s = s

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read(self):
        return self.s


class TestReloaderParser(BaseTestClass):
    """Max page not use in tests_parse
    """

    __jq_load_path = 'load'
    __jq_reload_path = 'reload'

    def setUp(self):
        parsers.open = MockOpen
        parsers.jq = MockJq
        self.tests_parse = [
            SubTest(
                name="Test 1",
                description="Invalid data_config. Problem with itct field",
                args={
                    'data_config': {
                        MockTab.TEST0: []
                    },
                    'is_reload': False
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                exception=utils.ParserError,
            ),
            SubTest(
                name="Test 2",
                description="Invalid data_config. Problem with ctoken field",
                args={
                    'data_config': {
                        MockTab.TEST0: []
                    },
                    'is_reload': False
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                exception=utils.ParserError,
            ),
            SubTest(
                name="Test 3",
                description="Valid data config.",
                args={
                    'data_config': {
                        'next_page_token': {'itct': 'token', 'ctoken': 'token'},
                        MockTab.TEST0: []
                    },
                    'is_reload': False
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                want=([self.__jq_load_path], {'ctoken': 'token', 'itct': 'token'}),
            ),
            SubTest(
                name="Test 4",
                description="Valid data config. There is not ctoken",
                args={
                    'data_config': {
                        'next_page_token': {'itct': 'token', 'ctoken': None},
                        MockTab.TEST0: []
                    },
                    'is_reload': False
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                want=([self.__jq_load_path], None),
            ),
            SubTest(
                name="Test 5",
                description="Valid data config. There is not itct",
                args={
                    'data_config': {
                        'next_page_token': {'itct': None, 'ctoken': 'token'},
                        MockTab.TEST0: []
                    },
                    'is_reload': False
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                want=([self.__jq_load_path], None),
            ),
            SubTest(
                name="Test 6",
                description="Reload",
                args={
                    'data_config': {
                        'next_page_token': {'itct': None, 'ctoken': 'token'},
                        MockTab.TEST0: []
                    },
                    'is_reload': True,
                },
                object=parsers.ReloaderParser(
                    max_page=None,
                    tab=mockTab,
                    jq_load_path=self.__jq_load_path,
                    jq_reload_path=self.__jq_reload_path,
                ),
                want=([self.__jq_reload_path], None),
            ),
        ]

        self.tests_is_final_page = [
            self.__create_subtest_is_final_page(times=0, max_page=1, want=False, test_num=0),
            self.__create_subtest_is_final_page(times=0, max_page=2, want=False, test_num=1),
            self.__create_subtest_is_final_page(times=0, max_page=3, want=False, test_num=2),
            self.__create_subtest_is_final_page(times=1, max_page=None, want=False, test_num=3),
            self.__create_subtest_is_final_page(times=2, max_page=None, want=False, test_num=4),
            self.__create_subtest_is_final_page(times=3, max_page=None, want=False, test_num=5),
            self.__create_subtest_is_final_page(times=0, max_page=1, want=False, test_num=6),
            self.__create_subtest_is_final_page(times=1, max_page=1, want=True, test_num=7),
            self.__create_subtest_is_final_page(times=2, max_page=1, want=True, test_num=8),
            self.__create_subtest_is_final_page(times=3, max_page=1, want=True, test_num=9),
            self.__create_subtest_is_final_page(times=0, max_page=2, want=False, test_num=10),
            self.__create_subtest_is_final_page(times=1, max_page=2, want=False, test_num=11),
            self.__create_subtest_is_final_page(times=2, max_page=2, want=True, test_num=12),
            self.__create_subtest_is_final_page(times=3, max_page=2, want=True, test_num=13),
        ]

    def __create_subtest_is_final_page(self, times, max_page, want, test_num):
        object = parsers.ReloaderParser(
            max_page=max_page,
            tab=mockTab,
            jq_load_path=self.__jq_load_path,
            jq_reload_path=self.__jq_reload_path,
        )
        parse_kwargs = {
            'data_config': {
                'next_page_token': {'itct': None, 'ctoken': 'token'},
                MockTab.TEST0: [self.__jq_load_path]
            },
            'is_reload': False
        }
        for i in range(times):
            object.parse(**parse_kwargs)
        subtest = SubTest(
            name="Test %d" % test_num,
            object=object,
            want=want,
        )
        return subtest

    def test_parse(self):
        for test in self.tests_parse:
            self.apply_test(test, lambda obj, kwargs: obj.parse(**kwargs))

    def test_is_final_page(self):
        for test in self.tests_is_final_page:
            self.apply_test(test, lambda obj, kwargs: obj.is_final_page(**kwargs))
