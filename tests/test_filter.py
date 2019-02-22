from crawler.filter import Filter, ChannelLanguage
from crawler.loaders import Tab
from tests.utils import BaseTestClass, SubTest


class TestScrapper(BaseTestClass):
    """
    This filter implements with assumption that About page and HomePage has the same languages.
    If this fact is not correct, it was got collision and result is not defined.
    """

    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description="Undefined",
                args={
                    'descr': {}
                },
                object=Filter(),
                want=ChannelLanguage.UNDEFINED,
            ),
            SubTest(
                name="Test 2",
                description="Strong ru",
                configuration={"Tab.About found": True, "Tab.HomePage found": False, "Tab.Video found": False},
                args={
                    'descr': {
                        Tab.About: [{'description': 'Привет, как у тебя дела?'}],
                        Tab.HomePage: [],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr=10),
                want=ChannelLanguage.STRONG_RU,
            ),
            SubTest(
                name="Test 3",
                description="English. Tab.About found. Tab.HomePage not found. Tab.Video not found",
                configuration={"Tab.About found": True, "Tab.HomePage found": False, "Tab.Video found": False},
                args={
                    'descr': {
                        Tab.About: [{'description': 'Hello! How are you'}],
                        Tab.HomePage: [],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr=10),
                want=ChannelLanguage.FOREIGN,
            ),
            SubTest(
                name="Test 4",
                description="Strong ru",
                configuration={"Tab.About found": False, "Tab.HomePage found": True, "Tab.Video found": False},
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [{'videos': {'general': {'description_parts': ['Тег', 'Тег', 'Мой новый тег']}}}],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr_parts=10),
                want=ChannelLanguage.STRONG_RU,
            ),
            SubTest(
                name="Test 5",
                description="Strong ru",
                configuration={"Tab.About found": False, "Tab.HomePage found": True, "Tab.Video found": False},
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [{'videos': {'general': {'description_parts': ['Tag', 'Tag', 'My new tag']}}}],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr_parts=10),
                want=ChannelLanguage.FOREIGN,
            ),
            SubTest(
                name="Test 6",
                configuration={"Tab.About found": False, "Tab.HomePage found": False, "Tab.Video found": True},
                description="Weak ru",
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [],
                        Tab.Videos: [
                            {'title': 'My new title'},
                            {'title': 'Мой новый заголовой'},
                            {'title': 'Мой новый заголовой'},
                        ],
                    }
                },
                object=Filter(),
                want=ChannelLanguage.WEAK_RU,
            ),
            SubTest(
                name="Test 7",
                configuration={"Tab.About found": True, "Tab.HomePage found": False, "Tab.Video found": False},
                description="Weak ru",
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [],
                        Tab.Videos: [
                            {'title': 'My new title'},
                            {'title': 'My new title'},
                            {'title': 'Мой новый заголовой'},
                        ],
                    }
                },
                object=Filter(),
                want=ChannelLanguage.FOREIGN,
            ),
        ]

    def test_parse(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.apply(**kwargs))
