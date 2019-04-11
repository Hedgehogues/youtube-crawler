import os
import sqlite3

from crawler import utils
from crawler.simple_logger import SimpleLogger


def create_args_set_update_base_channels(channel_id):
    return [
        channel_id,
        True,
        channel_id
    ]


def create_args_set_insert_base_channels(channel_id):
    return [
        channel_id,
        True
    ]


def create_args_update_channels(channel, scrapped, valid):
    return [
        channel['channel_id'],
        valid,
        scrapped,
        False,
        channel['priority'],
        channel['full_description'],
        channel['short_description']
    ]


class DBSqlLiteCache:
    # TODO: change integration test to unit tests and make integration tests
    """
    Rows in tables with channels can be:
        * valid==True, scrapped==True, downloaded==False. It means, that channel was scrapped and some videos were not
            downloaded
        * valid==True, scrapped==False, downloaded==False. It means, that channel was got from another channel or as
            base channels. Some videos were not downloaded
        * valid==False, downloaded==False. It means, that channel is not valid
        * valid==False, scrapped==False, downloaded==True. It means, that channel has been completely download (included
          video)
        * base_channel is parameter means users_channel
    Any other configuration is not possible and wrong. Field description:
        * field valid: if field sets True, then channel have not errors
        * field scrapped: if field sets True, then channel was scrapped
        * field downloaded: if field sets True, then channel was download with all available videos (or limited videos)
    """

    __sql_query_create_channel = '''
    create table channels (
      channel_id text PRIMARY KEY,
      base_channel boolean DEFAULT FALSE,
      valid boolean DEFAULT TRUE,
      scrapped boolean DEFAULT FALSE,
      downloaded boolean DEFAULT FALSE,
      priority float DEFAULT 0,
      full_description text,
      short_description text
    );'''

    __sql_query_create_videos = '''
    create table videos (
      channel_id text,
      video_id text PRIMARY KEY,
      valid boolean,
      downloaded boolean,
      priority float,
      description text
    );'''

    __sql_update_channel = '''
    update channels
    set
      channel_id text,
      video_id text PRIMARY KEY,
      valid boolean,
      downloaded boolean,
      priority float,
      description text
    where video_id=?;
    '''

    __sql_insert_channel = '''
    insert into channels(
      channel_id,
      valid, 
      scrapped, 
      downloaded, 
      priority, 
      full_description, 
      short_description
    ) 
    values(?, ?, ?, ?, ?, ?, ?)
    '''

    __sql_insert_video = '''
    insert into videos(
      channel_id,
      video_id,
      valid,
      downloaded,
      priority,
      description
    ) 
    values(?, ?, ?, ?, ?, ?, ?)
    '''

    __sql_insert_base_channel = '''
    insert into channels(
      channel_id,
      base_channel
    ) 
    values(?, ?)
    '''

    __sql_update_base_channel = '''
    update channels
    set
      channel_id=?,
      base_channel=?
    where channel_id=?;
    '''

    __sql_update_failed_channel = '''
    update channels
    set
      valid=?
    where channel_id=?;
    '''

    __sql_update_failed_video = '''
    update videos
    set
      valid=?
    where video_id=?;
    '''

    __sql_update_downloaded_channel = '''
    update channels
    set
      downloaded=?
    where channel_id=?;
    '''

    __sql_update_video = '''
    update videos
    set
      downloaded=?
    where channel_id=?;
    '''

    __sql_select_exist_channel = '''
    select channel_id from channels where channel_id=? 
    '''

    __sql_select_exist_video = '''
    select video_id from videos where video_id=? 
    '''

    __sql_get_best_channel = '''
    select channel_id from channels
    where channels.valid = TRUE and channels.downloaded = FALSE 
    order by NOT channels.scrapped, NOT channels.base_channel, -channels.priority 
    '''

    def __create_db(self, conn):
        conn.execute(self.__sql_query_create_channel)
        conn.execute(self.__sql_query_create_videos)
        conn.commit()

    def __init__(self, path='data/db.sqlite', hard=False, logger=None):
        if hard and os.path.exists(path):
            os.remove(path)

        self.logger = logger
        if self.logger is None:
            self.logger = SimpleLogger()

        if os.path.exists(path):
            raise FileExistsError("Data base already exist. Path: %s" % os.path.abspath(path))
        self.db_path = path
        conn = sqlite3.connect(self.db_path)
        self.__create_db(conn)
        conn.close()

    def __deduplicate_channels(self, channels):
        s = set()
        output_channels = []
        for channel in channels:
            if channel['channel_id'] not in s:
                output_channels.append(channel)
                s.add(channel['channel_id'])
                continue
            msg = "This channel already exists into input channels"
            warn = utils.CacheError(channel_id=channel['channel_id'], msg=msg)
            self.logger.warn(warn)
        return output_channels

    def update_failed_video(self, video_id):
        """
        This method set field valid as False. If there is not video_id, then exceptions will be generated

        :param video_id: failed video id (str)
        :exception utils.CacheError: it is not found video id
        """
        conn = sqlite3.connect(self.db_path)
        if not self.__check_exist_video_id(conn, video_id):
            raise utils.CacheError(channel_id=video_id, msg="Not found video in DB")
        conn.execute(self.__sql_update_failed_video, (False, video_id))
        conn.commit()
        conn.close()

    def insert_video_descr(self, video):
        """
        This method inserts video description into data base

        :param video: description of video: (
            {
                'video_id': video_id,
                'channel_id': channel_id,
                'full_description': full_descr,
                'short_description': short_descr,
                'valid': valid,
                'priority': priority,
            }
        )
        """
        # TODO: this method doesn't tested
        conn = sqlite3.connect(self.db_path)
        conn.execute(self.__sql_insert_video, video)
        conn.commit()
        conn.close()

    def check_exist_video(self, video_id):
        """
        This method check exist video and returns True if there is one or else another

        :param video_id: video id
        :return exist video (bool)
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(self.__sql_select_exist_video, video_id)
        res = c.fetchone()
        c.close()
        return res is not None and len(res) != 0

    def __check_exist_video_id(self, conn, video_id):
        c = conn.cursor()
        c.execute(self.__sql_select_exist_video, video_id)
        res = c.fetchone()
        c.close()
        return res is not None and len(res) != 0

    def __check_exist_channel_id(self, conn, channel_id):
        c = conn.cursor()
        c.execute(self.__sql_select_exist_channel, channel_id)
        res = c.fetchone()
        c.close()
        return res is not None and len(res) != 0

    def set_base_channels(self, channels_id, replace=False):
        """
        This method sets id of channels, which user sat.

        :param channels_id: list of channel ids for insert
        :param replace: field is True, then duplicate channel is replace else is not replace. Base_channel was updated.
            Another fields don't update
        """

        channels = []
        for channel_id in channels_id:
            channels.append({'channel_id': channel_id})
        channels = self.__deduplicate_channels(channels)
        conn = sqlite3.connect(self.db_path)
        for channel in channels:
            channel_id = channel['channel_id']
            query = self.__sql_insert_base_channel
            args = create_args_set_insert_base_channels(channel_id)
            is_exist_channel_id = self.__check_exist_channel_id(conn, channel_id)
            if is_exist_channel_id and not replace:
                continue
            if is_exist_channel_id and replace:
                query = self.__sql_update_base_channel
                args = create_args_set_update_base_channels(channel_id)
            conn.execute(query, args)
        conn.commit()
        conn.close()

    def set_channels(self, channels, scrapped, valid):
        """
        This function process next cases:
            * valid==True, scrapped==True, downloaded==False
            * valid==True, scrapped==False, downloaded==False
            * valid==False, scrapped==False, downloaded==False
        If you want got more information, see class description.

        This function insert new channel and update old channels fully (without field base_channel)

        :param channels: describe of channel: (
            [{
                    'channel_id': channel_id,
                    'priority': priority,
                    'full_description': full_descr,
                    'short_description': short_descr,
            }]
        )
        :param scrapped: scrapped or not channel (bool)
        :param valid: valid or invalid channel (bool)
        """
        conn = sqlite3.connect(self.db_path)
        channels = self.__deduplicate_channels(channels)
        for channel in channels:
            channel_id = channel['channel_id']
            query = self.__sql_insert_channel
            args = create_args_update_channels(channel, scrapped, valid)
            if self.__check_exist_channel_id(conn, channel_id):
                query = self.__sql_update_channel
                args.append(channel_id)
            conn.execute(query, args)
        conn.commit()
        conn.close()

    def update_failed_channel(self, channel_id):
        """
        This method set field valid as False. If there is not channel_id, then exceptions will be generated

        :param channel_id: failed channel id (str)
        :exception utils.CacheError: it is not found channel id
        """
        conn = sqlite3.connect(self.db_path)
        if not self.__check_exist_channel_id(conn, channel_id):
            raise utils.CacheError(channel_id=channel_id, msg="Not found channel in DB")
        conn.execute(self.__sql_update_failed_channel, (False, channel_id))
        conn.commit()
        conn.close()

    def update_channel_downloaded(self, channel_id):
        """
        This function process next cases:
            * valid==False, scrapped==False, downloaded==True
        If you want got more information, see c  lass description

        :param channel_id: field downloaded sets as True
        :exception utils.CacheError: it is not found channel id
        """
        conn = sqlite3.connect(self.db_path)
        if not self.__check_exist_channel_id(conn, channel_id):
            raise utils.CacheError(channel_id=channel_id, msg="Not found channel in DB")
        conn.execute(self.__sql_update_downloaded_channel, (True, channel_id))
        conn.commit()
        conn.close()

    def get_best_channel_id(self):
        """
        This method returns the best channel_id. This method selects all channels except downloaded==True
        or valid==False. All channels ranges by priority. But there are two flags, which ones set additional ranges.
        (see sql-query)

        :return the best channel_id (str) by priority or '' if there are not any actual channels
        :exception utils.CacheError: it is not found any channel id for return
        """
        conn = sqlite3.connect(self.db_path)

        # It uses fetch one instead of top 1 as not all data bases have top directive
        res = conn.execute(self.__sql_get_best_channel).fetchone()
        conn.close()
        if res is None or len(res) == 0:
            raise utils.CacheError(msg="There are not any channels")
        return res[0]
