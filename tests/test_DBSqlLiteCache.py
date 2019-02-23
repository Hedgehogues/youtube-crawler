import os
import sqlite3

from crawler.cache import DBSqlLiteCache
from tests.utils import BaseTestClass, SubTest


class TestDBSqlLiteCache(BaseTestClass):
    __db_path = 'data/test.sqlite'

    def __check_exist_file(self, filename):
        self.assertTrue(os.path.exists(filename))

    @staticmethod
    def __remove_filename(filename):
        if os.path.exists(filename):
            os.remove(filename)

    @staticmethod
    def __create_filename(filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()

    def __create_subtest_constructor(self, i, hard, mws_before, mws_after, exception=None):
        mws_before = [lambda: self.__remove_filename(self.__db_path)] + mws_before
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
        self.constructor_tests = [
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

        self.update_channels_tests = [
            SubTest(
                name="Test 1",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        }
                    ],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path, hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path)
                ],
            ),
        ]

    def __check_db_count_rows(self, assert_count, table_name):
        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()
        c.execute('select * from %s' % table_name)
        x = c.fetchall()
        self.assertEqual(assert_count, len(x))
        c.close()
        conn.close()

    def test___init__(self):
        for test in self.constructor_tests:
            self.apply_test(test, lambda obj, kwargs: obj(**kwargs))

    def test_update_channels(self):
        for test in self.update_channels_tests:
            self.apply_test(test, lambda obj, kwargs: obj.update_channels(**kwargs))
