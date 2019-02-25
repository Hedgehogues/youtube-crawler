import os
import sqlite3

from crawler import utils
from crawler.cache import DBSqlLiteCache
from tests import MockLogger
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

        self.set_channels_tests = [
            SubTest(
                name="Test 1",
                description="All fields are not None",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': 0,
                            'full_description': 'X',
                            'short_description': 'Y',
                        }
                    ],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'1', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'1', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'1')
                ],
            ),
            SubTest(
                name="Test 2",
                description="Some fields are None",
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
                object=DBSqlLiteCache(path=self.__db_path+'2', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'2', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'2')
                ],
            ),
            SubTest(
                name="Test 3",
                description="Two channel per transaction",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        },
                        {
                            'channel_id': 'Y',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        }
                    ],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'3', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'3', 2, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'3')
                ],
            ),
            SubTest(
                name="Test 4",
                description="Duplicate channel id into inputs",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        },
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
                object=DBSqlLiteCache(path=self.__db_path+'4', hard=True, logger=MockLogger()),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'4', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'4')
                ],
            ),
            SubTest(
                name="Test 5",
                description="Two channel per transaction",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        },
                        {
                            'channel_id': 'Y',
                            'priority': 0,
                            'full_description': None,
                            'short_description': None,
                        }
                    ],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'5', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.__set_rows_channels(self.__db_path+'5', ['X', 'P'], 'channels')
                ],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'5', 3, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'5')
                ],
            ),
            SubTest(
                name="Test 6",
                description="Invalid fields exception",
                args={
                    'channels': [None],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'6', hard=True, logger=MockLogger()),
                exception=Exception,
                middlewares_after=[lambda: self.__remove_filename(self.__db_path+'6')],
            ),
            SubTest(
                name="Test 7",
                description="Invalid database type",
                args={
                    'channels': [
                        {
                            'channel_id': 'X',
                            'priority': [],
                            'full_description': None,
                            'short_description': None,
                        }
                    ],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'7', hard=True, logger=MockLogger()),
                exception=sqlite3.Error,
                middlewares_after=[
                    lambda: self.__remove_filename(self.__db_path+'7')
                ],
            ),
            SubTest(
                name="Test 8",
                description="Empty",
                args={
                    'channels': [],
                    'scrapped': False,
                    'valid': False
                },
                object=DBSqlLiteCache(path=self.__db_path+'8', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'8', 0, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'8')
                ],
            ),
            SubTest(
                name="Test 9",
                description="Base_channel fail should not be changed",
                fail=True,
                args={'channels_id': []},
                object=DBSqlLiteCache(path=self.__db_path+'8', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'7', 0, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'8')
                ],
            ),
        ]

        self.set_base_channels_tests = [
            SubTest(
                name="Test 1",
                description="All fields are not None",
                args={'channels_id': ['X']},
                object=DBSqlLiteCache(path=self.__db_path+'1', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'1', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'1')
                ],
            ),
            SubTest(
                name="Test 2",
                description="Some fields are None",
                args={'channels_id': ['X']},
                object=DBSqlLiteCache(path=self.__db_path+'2', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'2', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'2')
                ],
            ),
            SubTest(
                name="Test 3",
                description="Two channel per transaction",
                args={'channels_id': ['X', 'Y']},
                object=DBSqlLiteCache(path=self.__db_path+'3', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'3', 2, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'3')
                ],
            ),
            SubTest(
                name="Test 4",
                description="Duplicate channel id into inputs",
                args={'channels_id': ['X', 'X']},
                object=DBSqlLiteCache(path=self.__db_path+'4', hard=True, logger=MockLogger()),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'4', 1, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'4')
                ],
            ),
            SubTest(
                name="Test 5",
                description="Two channel per transaction",
                args={'channels_id': ['X', 'Y']},
                object=DBSqlLiteCache(path=self.__db_path+'5', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.__set_rows_channels(self.__db_path+'5', ['X', 'P'], 'channels')
                ],
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'5', 3, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'5')
                ],
            ),
            SubTest(
                name="Test 6",
                description="Invalid fields exception",
                args={'channels_id': [None]},
                object=DBSqlLiteCache(path=self.__db_path+'6', hard=True, logger=MockLogger()),
                exception=Exception,
                middlewares_after=[lambda: self.__remove_filename(self.__db_path+'6')],
            ),
            SubTest(
                name="Test 7",
                description="Empty",
                args={'channels_id': []},
                object=DBSqlLiteCache(path=self.__db_path+'7', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'7', 0, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'7')
                ],
            ),
            SubTest(
                name="Test 8",
                description="Existing entries should not be updated",
                fail=True,
                args={'channels_id': []},
                object=DBSqlLiteCache(path=self.__db_path+'8', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.__check_db_count_rows(self.__db_path+'7', 0, 'channels'),
                    lambda: self.__remove_filename(self.__db_path+'8')
                ],
            ),
        ]

    @staticmethod
    def __set_rows_channels(db_path, channel_ids, table_name):
        conn = sqlite3.connect(db_path)
        for channel_id in channel_ids:
            conn.execute('insert into %s(channel_id) values(?)' % table_name, (channel_id))
        conn.commit()
        conn.close()

    def __check_db_count_rows(self, db_path, assert_count, table_name):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('select count(*) from %s' % table_name)
        res = c.fetchone()
        if res is None:
            self.fail()
        self.assertEqual(assert_count, res[0])
        c.close()
        conn.close()

    def test___init__(self):
        for test in self.constructor_tests:
            self.apply_test(test, lambda obj, kwargs: obj(**kwargs))

    def test_set_channels(self):
        for test in self.set_channels_tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_channels(**kwargs))

    def test_set_base_channels(self):
        for test in self.set_base_channels_tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_base_channels(**kwargs))
