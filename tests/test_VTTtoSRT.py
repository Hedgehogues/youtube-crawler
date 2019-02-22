import os

from crawler import utils
from crawler.vtt_to_srt import VTTtoSRT
from tests.utils import BaseTestClass, SubTest


class TestVTTtoSRT(BaseTestClass):
    __prefix = '_test_'
    __vtt = '.vtt'
    __srt = '.srt'
    __test_file = [
        'data/videos/_1anwjN9tPA/_1anwjN9tPA.ru',
        'data/videos/-6RG9SfBkP0/-6RG9SfBkP0.ru',
    ]

    def __get_checkfile_args(self, i):
        return {
            'test_file': self.__test_file[i],
            'ext': self.__srt,
            'prefix': self.__prefix,
        }

    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description='File: %s' % os.path.basename(self.__test_file[0]),
                args={'vtt_path': self.__test_file[0] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.check_file(**self.__get_checkfile_args(0))],
            ),
            SubTest(
                name="Test 2",
                description='File: %s' % os.path.basename(self.__test_file[1]),
                args={'vtt_path': self.__test_file[1] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.check_file(**self.__get_checkfile_args(1))],
            ),
            SubTest(
                name="Test 3",
                description='Fail vtt exception',
                args={'vtt_path': self.__test_file[0] + self.__vtt + '_'},
                object=VTTtoSRT(),
                exception=utils.ExtensionError,
            )
        ]

    def test_parse(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.transform(**kwargs))
