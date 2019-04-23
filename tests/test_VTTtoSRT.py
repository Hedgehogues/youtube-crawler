import logging
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

    def __check_file(self, test_file, ext, prefix):
        path, filename = os.path.split(test_file)
        fd = open('%s/%s' % (path, prefix + filename + ext))
        lines_got_srt = fd.readlines()
        fd.close()
        fd = open('%s/%s' % (path, filename + ext))
        lines_want_srt = fd.readlines()
        fd.close()
        for item in zip(lines_want_srt, lines_got_srt):
            self.assertEqual(item[0], item[1])
        self.assertEqual(len(lines_want_srt), len(lines_got_srt))
        os.remove('%s/%s' % (path, prefix + filename + ext))

    def setUp(self):
        logging.getLogger().setLevel(logging.CRITICAL)
        self.tests = [
            SubTest(
                name="Test 1",
                description='File: %s' % os.path.basename(self.__test_file[0]),
                args={'vtt_path': self.__test_file[0] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.__check_file(**self.__get_checkfile_args(0))],
            ),
            SubTest(
                name="Test 2",
                description='File: %s' % os.path.basename(self.__test_file[1]),
                args={'vtt_path': self.__test_file[1] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.__check_file(**self.__get_checkfile_args(1))],
            ),
            SubTest(
                name="Test 3",
                description='Fail vtt exception',
                args={'vtt_path': self.__test_file[0] + self.__vtt + '_'},
                object=VTTtoSRT(),
                exception=utils.ExtensionError,
            )
        ]

    def test_transform(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.transform(**kwargs))
