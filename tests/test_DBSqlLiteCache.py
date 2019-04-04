import sqlite3

from crawler import utils
from crawler.cache import DBSqlLiteCache
from tests import MockLogger
from tests.utils import BaseTestClass, SubTest


class TestDBSqlLiteCache(BaseTestClass):
    db_path = 'data/test.sqlite'

    @staticmethod
    def set_rows_channels(db_path, channel_ids, table_name,
                          base_channel=False, valid=True, downloaded=False, scrapped=False, priority=0.):
        conn = sqlite3.connect(db_path)
        query = 'insert into %s' \
                '(channel_id, base_channel, valid, downloaded, scrapped, priority) ' \
                'values(?, ?, ?, ?, ?, ?)' % table_name
        for channel_id in channel_ids:
            conn.execute(query, (channel_id, base_channel, valid, downloaded, scrapped, priority))
        conn.commit()
        conn.close()

    def check_field(self, db_path, value, table_name, channel_id, field):
        fields_indexes = {
            'base_channel': 1,
            'valid': 2,
        }
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        query = 'select * from %s where channel_id=?' % table_name
        c.execute(query, (channel_id,))
        res = c.fetchone()
        self.assertIsNotNone(res)
        field_index = fields_indexes[field]
        self.assertEqual(value, res[field_index])
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
        self.tests = [
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
                    lambda: self.check_field(self.db_path + '9', 1, 'channels', 'X', field='base_channel'),
                    lambda: self.check_field(self.db_path + '9', 1, 'channels', 'P', field='base_channel'),
                    lambda: self.check_field(self.db_path + '9', 0, 'channels', 'Y', field='base_channel'),
                    lambda: self.check_db_count_rows(self.db_path + '9', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '9')
                ],
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_channels(**kwargs))


class TestDBSqlLiteCacheSetBaseChannels(TestDBSqlLiteCache):

    def setUp(self):
        self.tests = [
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
                    lambda: self.check_field(self.db_path + '8', 0, 'channels', 'X', field='base_channel'),
                    lambda: self.check_field(self.db_path + '8', 1, 'channels', 'Y', field='base_channel'),
                    lambda: self.check_db_count_rows(self.db_path + '8', 3, 'channels'),
                    lambda: self.remove_filename(self.db_path + '8')
                ],
            ),
        ]

    def test(self):
        for test in self.tests:
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
        self.tests = [
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

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj(**kwargs))


class TestDBSqlLiteCacheSetFailedChannel(TestDBSqlLiteCache):

    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description="Modify old value",
                args={'channel_id': 'X'},
                object=DBSqlLiteCache(path=self.db_path+'1', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '1', ['X', 'P'], 'channels', valid=True),
                ],
                middlewares_after=[
                    lambda: self.check_field(self.db_path + '1', 0, 'channels', 'X', field='valid'),
                    lambda: self.check_field(self.db_path + '1', 1, 'channels', 'P', field='valid'),
                    lambda: self.remove_filename(self.db_path+'1')
                ],
            ),
            SubTest(
                name="Test 2",
                description="Exception undefined value",
                args={'channel_id': 'Y'},
                object=DBSqlLiteCache(path=self.db_path+'2', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path + '2', ['X', 'P'], 'channels', valid=True),
                ],
                exception=utils.CacheError,
                middlewares_after=[lambda: self.remove_filename(self.db_path+'2')],
            ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.set_failed_channel(**kwargs))


class TestDBSqlLiteCacheGetBestChannelId(TestDBSqlLiteCache):

    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description="Empty cache",
                object=DBSqlLiteCache(path=self.db_path+'1', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'1', [], 'channels'),
                ],
                exception=utils.CacheError,
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'1')
                ],
            ),
            SubTest(
                name="Test 2",
                description="There are not valid channels",
                object=DBSqlLiteCache(path=self.db_path+'2', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'2', ['X'], 'channels', valid=False),
                ],
                exception=utils.CacheError,
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'2')
                ],
            ),
            SubTest(
                name="Test 3",
                description="There are valid channel the only",
                object=DBSqlLiteCache(path=self.db_path+'3', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'3', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                ],
                want='X',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'3')
                ],
            ),
            SubTest(
                name="Test 4",
                description="There are base channel",
                object=DBSqlLiteCache(path=self.db_path+'4', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'4', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'4', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                ],
                want='Y',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'4')
                ],
            ),
            SubTest(
                name="Test 5",
                description="There are base channel and downloaded",
                object=DBSqlLiteCache(path=self.db_path+'5', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'5', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'5', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'5', ['Z'], 'channels', base_channel=False, valid=True,
                                                   downloaded=True, scrapped=False, priority=0),
                ],
                want='Y',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'5')
                ],
            ),
            SubTest(
                name="Test 6",
                description="There are base channel priority",
                object=DBSqlLiteCache(path=self.db_path+'6', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'6', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'6', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'6', ['Z'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=1),
                ],
                want='Z',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'6')
                ],
            ),
            SubTest(
                name="Test 7",
                description="There are the only downloaded channel",
                object=DBSqlLiteCache(path=self.db_path+'7', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'7', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=True, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'7', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=True, scrapped=False, priority=1),
                ],
                exception=utils.CacheError,
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'7')
                ],
            ),
            SubTest(
                name="Test 8",
                description="Scrapped and base channel",
                object=DBSqlLiteCache(path=self.db_path+'8', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'8', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=True, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'8', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                ],
                want='X',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'8')
                ],
            ),
            SubTest(
                name="Test 9",
                description="Scrapped, base channel, priority",
                object=DBSqlLiteCache(path=self.db_path+'9', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'9', ['X'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=True, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'9', ['Y'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=1),
                ],
                want='X',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'9')
                ],
            ),
            SubTest(
                name="Test 10",
                description="Scrapped, base channel, priority",
                object=DBSqlLiteCache(path=self.db_path+'10', hard=True),
                middlewares_before=[
                    lambda: self.set_rows_channels(self.db_path+'10', ['X'], 'channels', base_channel=True, valid=True,
                                                   downloaded=False, scrapped=False, priority=0),
                    lambda: self.set_rows_channels(self.db_path+'10', ['Y'], 'channels', base_channel=False, valid=True,
                                                   downloaded=False, scrapped=False, priority=1.1),
                ],
                want='X',
                middlewares_after=[
                    lambda: self.remove_filename(self.db_path+'10')
                ],
            ),
            # SubTest(
            #     name="Test 3",
            #     description="Empty cache",
            #     object=DBSqlLiteCache(path=self.db_path+'3', hard=True),
            #     middlewares_before=[
            #         lambda: self.set_rows_channels(self.db_path + '3', ['X'], 'channels'),
            #     ],
            #     want='X',
            #     middlewares_after=[
            #         lambda: self.remove_filename(self.db_path+'3')
            #     ],
            # ),
        ]

    def test(self):
        for test in self.tests:
            self.apply_test(test, lambda obj, kwargs: obj.get_best_channel_id(**kwargs))
