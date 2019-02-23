import os

from crawler.cache import DBSqlLiteCache
from tests.utils import BaseTestClass, SubTest


class TestDBSqlLiteCache(BaseTestClass):
    __db_path = 'data/test.sqlite'

    @staticmethod
    def __check_exist_file(filename):
        if os.path.exists(filename):
            return True
        return False

    @staticmethod
    def __remove_filename(filename):
        if os.path.exists(filename):
            os.remove(filename)

    @staticmethod
    def __create_filename(filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()

    def __create_subtest_constructor(self, i, hard, mws_before, mws_after, exception=None):
        mws_after.append(lambda: self.__remove_filename(self.__db_path))
        return SubTest(
            name="Test %d" % i,
            args={'path': self.__db_path, 'hard': hard},
            object=DBSqlLiteCache,
            ignore_want=True,
            exception=exception,
            middlewares_before=mws_before,
            middlewares_after=mws_after,
        )

    def setUp(self):
        self.tests = [
            self.__create_subtest_constructor(
                1,
                False,
                [],
                [lambda: self.__check_exist_file(self.__db_path)]
            ),
            self.__create_subtest_constructor(
                2,
                False,
                [lambda: self.__create_filename(self.__db_path)],
                [],
                FileExistsError
            ),
            self.__create_subtest_constructor(
                3,
                True,
                [lambda: self.__create_filename(self.__db_path)],
                [lambda: self.__check_exist_file(self.__db_path)]
            ),
        ]

    def test___init__(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj(**kwargs))
