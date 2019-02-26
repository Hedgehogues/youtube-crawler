import sqlite3

from crawler.cache import DBSqlLiteCache
from tests import MockLogger
from tests.utils import BaseTestClass, SubTest


class TestDBSqlLiteCache(BaseTestClass):
    db_path = 'data/test.sqlite'

    @staticmethod
    def set_rows_channels(db_path, channel_ids, table_name, base_channel=False):
        conn = sqlite3.connect(db_path)
        query = 'insert into %s(channel_id, base_channel) values(?, ?)' % table_name
        for channel_id in channel_ids:
            conn.execute(query, (channel_id, base_channel))
        conn.commit()
        conn.close()

    def check_base_channel(self, db_path, base_channel_value, table_name, channel_id):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        query = 'select * from %s where channel_id=?' % table_name
        c.execute(query, (channel_id,))
        res = c.fetchone()
        self.assertIsNotNone(res)
        self.assertEqual(base_channel_value, bool(res[1]))
        c.close()
        conn.close()

    def check_db_count_rows(self, db_path, assert_count, table_name):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('select count(*) from %s' % table_name)
        res = c.fetchone()
        self.assertIsNotNone(res)
        self.assertEqual(assert_count, res[0])
        c.close()
        conn.close()


class TestDBSqlLiteCacheSetChannels(TestDBSqlLiteCache):

    def setUp(self):
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
                object=DBSqlLiteCache(path=self.db_path + '1', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '1', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '1')
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
                object=DBSqlLiteCache(path=self.db_path + '2', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '2', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '2')
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
                object=DBSqlLiteCache(path=self.db_path + '3', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '3', 2, 'channels'),
                    lambda: self.remove_filename(self.db_path + '3')
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
                object=DBSqlLiteCache(path=self.db_path + '4', hard=True, logger=MockLogger()),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '4', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '4')
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
                object=DBSqlLiteCache(path=self.db_path + '5', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '5', ['X', 'P'], 'channels')
                ],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '5', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '5')
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
                object=DBSqlLiteCache(path=self.db_path + '6', hard=True, logger=MockLogger()),
                exception=Exception,
                middlewares_after=[lambda: self.remove_filename(self.db_path + '6')],
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
                object=DBSqlLiteCache(path=self.db_path + '7', hard=True, logger=MockLogger()),
                exception=sqlite3.Error,
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path + '7')
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
                object=DBSqlLiteCache(path=self.db_path + '8', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '8', 0, 'channels'),
                    lambda: self.remove_filename(self.db_path + '8')
                ],
            ),
            SubTest(
                name="Test 9",
                description="Base_channel should not be changed",
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
                object=DBSqlLiteCache(path=self.db_path + '9', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '9', ['X', 'P'], 'channels', True)
                ],
                middlewares_after=[
                    lambda: self.check_base_channel(self.db_path + '9', True, 'channels', 'X'),
                    lambda: self.check_base_channel(self.db_path + '9', True, 'channels', 'P'),
                    lambda: self.check_base_channel(self.db_path + '9', False, 'channels', 'Y'),
                    lambda: self.check_db_count_rows(self.db_path + '9', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '9')
                ],
            ),
        ]

    def test_set_channels(self):
        for test in self.set_channels_tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_channels(**kwargs))


class TestDBSqlLiteCacheSetBaseChannels(TestDBSqlLiteCache):

    def setUp(self):
        self.set_base_channels_tests = [
            SubTest(
                name="Test 1",
                description="All fields are not None",
                args={'channels_id': ['X']},
                object=DBSqlLiteCache(path=self.db_path + '1', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '1', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '1')
                ],
            ),
            SubTest(
                name="Test 2",
                description="Some fields are None",
                args={'channels_id': ['X']},
                object=DBSqlLiteCache(path=self.db_path + '2', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '2', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '2')
                ],
            ),
            SubTest(
                name="Test 3",
                description="Two channel per transaction",
                args={'channels_id': ['X', 'Y']},
                object=DBSqlLiteCache(path=self.db_path + '3', hard=True),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '3', 2, 'channels'),
                    lambda: self.remove_filename(self.db_path + '3')
                ],
            ),
            SubTest(
                name="Test 4",
                description="Duplicate channel id into inputs",
                args={'channels_id': ['X', 'X']},
                object=DBSqlLiteCache(path=self.db_path + '4', hard=True, logger=MockLogger()),
                middlewares_before=[],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '4', 1, 'channels'),
                    lambda: self.remove_filename(self.db_path + '4')
                ],
            ),
            SubTest(
                name="Test 5",
                description="Two channel per transaction",
                args={'channels_id': ['X', 'Y']},
                object=DBSqlLiteCache(path=self.db_path + '5', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '5', ['X', 'P'], 'channels')
                ],
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '5', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '5')
                ],
            ),
            SubTest(
                name="Test 6",
                description="Invalid fields exception",
                args={'channels_id': [None]},
                object=DBSqlLiteCache(path=self.db_path + '6', hard=True, logger=MockLogger()),
                exception=Exception,
                middlewares_after=[lambda: self.remove_filename(self.db_path + '6')],
            ),
            SubTest(
                name="Test 7",
                description="Empty",
                args={'channels_id': []},
                object=DBSqlLiteCache(path=self.db_path + '7', hard=True, logger=MockLogger()),
                middlewares_after=[
                    lambda: self.check_db_count_rows(self.db_path + '7', 0, 'channels'),
                    lambda: self.remove_filename(self.db_path + '7')
                ],
            ),
            SubTest(
                name="Test 8",
                description="Existing entries should not be updated",
                args={'channels_id': ["X", "Y"]},
                object=DBSqlLiteCache(path=self.db_path + '8', hard=True, logger=MockLogger()),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '8', ['X', 'P'], 'channels')
                ],
                middlewares_after=[
                    lambda: self.check_base_channel(self.db_path + '8', False, 'channels', 'X'),
                    lambda: self.check_base_channel(self.db_path + '8', True, 'channels', 'Y'),
                    lambda: self.check_db_count_rows(self.db_path + '8', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '8')
                ],
            ),
        ]

    def test_set_base_channels(self):
        for test in self.set_base_channels_tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_base_channels(**kwargs))


class TestDBSqlLiteCacheConstructor(TestDBSqlLiteCache):

    def __create_subtest_constructor(self, i, hard, mws_before, mws_after, exception=None):
        mws_before = [lambda: self.remove_filename(self.db_path + str(i))] + mws_before
        mws_after.append(lambda: self.remove_filename(self.db_path + str(i)))
        return SubTest(
            name="Test %d" % i,
            args={'path': self.db_path + str(i), 'hard': hard},
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
                [lambda: self.check_exist_file(self.db_path + '1')]
            ),
            self.__create_subtest_constructor(
                2,
                False,
                [lambda: self.create_filename(self.db_path + '2')],
                [],
                FileExistsError
            ),
            self.__create_subtest_constructor(
                3,
                True,
                [lambda: self.create_filename(self.db_path + '3')],
                [lambda: self.check_exist_file(self.db_path + '3')]
            ),
        ]

        # self.set_failed_channel_tests = [
        #     SubTest(
        #         name="Test 1",
        #         args={'channels_id': ['X']},
        #         object=DBSqlLiteCache(path=self.__db_path+'1', hard=True),
        #         middlewares_before=[
        #             lambda: self.__set_rows_channels(self.__db_path + '1', ['X', 'P'], 'channels'),
        #         ],
        #         middlewares_after=[
        #             lambda: self.check_db_count_rows(self.__db_path+'1', 1, 'channels'),
        #             lambda: self.__remove_filename(self.__db_path+'1')
        #         ],
        #     ),
        # ]

    def test___init__(self):
        for test in self.constructor_tests:
            self.apply_test(test, lambda obj, kwargs: obj(**kwargs))

    # def test_set_failed_channel(self):
    #     for test in self.set_failed_channel_tests:
    #         self.apply_test(test, lambda obj, kwargs: obj.set_base_channels(**kwargs))
