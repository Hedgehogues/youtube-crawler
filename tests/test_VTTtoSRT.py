import os

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

    def __check_file(self, i):
        path, filename = os.path.split(self.__test_file[i])
        fd = open('%s/%s' % (path, self.__prefix + filename + self.__srt))
        lines_got_srt = fd.readlines()
        fd.close()
        fd = open('%s/%s' % (path, filename + self.__srt))
        lines_want_srt = fd.readlines()
        fd.close()
        for item in zip(lines_want_srt, lines_got_srt):
            self.assertEqual(item[0], item[1])
        self.assertEqual(len(lines_want_srt), len(lines_got_srt))
        os.remove('%s/%s' % (path, self.__prefix + filename + self.__srt))

    def setUp(self):

        self.tests = [
            SubTest(
                name="Test 1",
                description='File: %s' % os.path.basename(self.__test_file[0]),
                args={'vtt_path': self.__test_file[0] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.__check_file(0)],
            ),
            SubTest(
                name="Test 2",
                description='File: %s' % os.path.basename(self.__test_file[1]),
                args={'vtt_path': self.__test_file[1] + self.__vtt},
                object=VTTtoSRT(prefix=self.__prefix),
                middlewares_after=[lambda: self.__check_file(1)],
            )
        ]

    def test_parse(self):
        for i in range(len(self.tests)):
            self.apply_test(i, lambda obj, kwargs: obj.transform(**kwargs))
