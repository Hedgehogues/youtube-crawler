from crawler.filter import Filter, ChannelLanguage
from crawler.loaders import Tab
from tests.utils import BaseTestClass, SubTest


class TestScrapper(BaseTestClass):
    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description="Strong ru. Tab.About found. Tab.HomePage not found. Tab.Video not found",
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
                name="Test 2",
                description="English. Tab.About found. Tab.HomePage not found. Tab.Video not found",
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
                name="Test 3",
                description="Tab.About not found. Tab.HomePage not found. Tab.Video not found",
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr=10),
                want=ChannelLanguage.UNDEFINED,
            ),
            SubTest(
                name="Test 4",
                description="Strong ru. Tab.About not found. Tab.HomePage found. Tab.Video not found",
                args={
                    'descr': {
                        Tab.About: [],
                        Tab.HomePage: [{'videos': {'general': {'description_parts': 'Привет, как у тебя дела?'}}}],
                        Tab.Videos: [],
                    }
                },
                object=Filter(len_descr=10),
                want=ChannelLanguage.STRONG_RU,
            ),
        ]

    def test_parse(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.apply(**kwargs))
