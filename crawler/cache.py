import os
import sqlite3

from crawler import utils
from crawler.simple_logger import SimpleLogger


def create_args_set_base_channels(channel_id):
    return [
        channel_id,
        True,
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
    """
    Rows in tables with channels can be:
        * valid==True, scrapped==True, downloaded==False. It means, that channel was scrapped and some videos were not
            downloaded
        * valid==True, scrapped==False, downloaded==False. It means, that channel was got from another channel or as
            base channels. Some videos were not downloaded
        * valid==False, downloaded==False. It means, that channel is not valid
        * valid==False, scrapped==False, downloaded==True. It means, that channel has been completely download
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
      channel_id=?,
      valid=?,
      scrapped=?,
      downloaded=?,
      priority=?,
      full_description=?,
      short_description=?
    where channel_id=?;
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

    __sql_insert_set_base_channel = '''
    insert into channels(
      channel_id,
      valid, 
      base_channel
    ) 
    values(?, ?, ?)
    '''

    __sql_update_failed_channel = '''
    update channels
    set
      valid=?
    where channel_id=?;
    '''

    __sql_select_exist_channel = '''
    select channel_id from channels where channel_id=? 
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

    def set_channel_downloaded(self, channel_id):
        """
        This function process next cases:
            * valid==False, scrapped==False, downloaded==True
        If you want got more information, see c  lass description
        """
        raise Exception("Not implemented")

    def set_video_descr(self, video):
        raise Exception("Not implemented")

    def check_video_descr(self, video_id):
        raise Exception("Not implemented")

    def __check_exist_channel_id(self, conn, channel_id):
        c = conn.cursor()
        c.execute(self.__sql_select_exist_channel, channel_id)
        res = c.fetchone()
        c.close()
        return res is not None and len(res) != 0

    def __log_exist_channel(self, channel_id):
        warn = utils.CacheError(channel_id=channel_id, msg="This channel already exists")
        self.logger.warn(warn)

    def set_base_channels(self, channels_id):
        """
        This method sets id of channels, which user sat.

        :param channels_id: list of channel ids for insert
        """
        channels = []
        for channel_id in channels_id:
            channels.append({'channel_id': channel_id})
        channels = self.__deduplicate_channels(channels)
        conn = sqlite3.connect(self.db_path)
        for channel in channels:
            channel_id = channel['channel_id']
            if self.__check_exist_channel_id(conn, channel_id):
                self.__log_exist_channel(channel_id)
                continue
            args = create_args_set_base_channels(channel_id)
            conn.execute(self.__sql_insert_set_base_channel, args)
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

        :param channels: describe of channel (dict)
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
                self.__log_exist_channel(channel_id)
                query = self.__sql_update_channel
                args.append(channel_id)
            conn.execute(query, args)
        conn.commit()
        conn.close()

    def set_failed_channel(self, channel_id):
        """
        This method set field valid as False. If there is not channel_id, then exceptions will be generated

        :param channel_id: failed channel id (str)
        :return:
        """
        conn = sqlite3.connect(self.db_path)
        conn.execute(self.__sql_update_failed_channel, (False, channel_id))
        conn.commit()
        conn.close()

    def get_best_channel_id(self):
        """
        This method return best channel_id. This method select all channels except downloaded==True
        or valid==False. If method was scrapped, but not downloaded, then this channel will be scrapped
        again and some videos which not downloaded will be download
        :return:
            channel_id (str): the best channel_id by priority
        """
        raise Exception("Not implemented")
