import os
import sqlite3

from crawler import utils


class DBSqlLiteCache:
    """
    Rows in tables with channels can be:
        * valid==True, scrapped==True, downloaded==False. It means, that channel was scrapped and some videos were not
            downloaded
        * valid==True, scrapped==False, downloaded==False. It means, that channel was got from another channel or as
            base channels. Some videos were not downloaded
        * valid==False, scrapped==False, downloaded==False. It means, that channel is not valid
        * valid==False, scrapped==False, downloaded==True. It means, that channel has been completely download
    Any other configuration is not possible and wrong. Field description:
        * field valid: if field sets True, then channel have not errors
        * field scrapped: if field sets True, then channel was scrapped
        * field downloaded: if field sets True, then channel was download with all available videos (or limited videos)
    """

    __sql_query_create_channel = '''
    create table channels (
      channel_id text PRIMARY KEY,
      valid boolean,
      scrapped boolean,
      downloaded boolean,
      priority float,
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

    __sql_select_exist_channel = '''
    select channel_id from channels where channel_id=? 
    '''

    def __create_db(self, conn):
        conn.execute(self.__sql_query_create_channel)
        conn.execute(self.__sql_query_create_videos)
        conn.commit()

    def __init__(self, path='data/db.sqlite', hard=False):
        if hard and os.path.exists(path):
            os.remove(path)

        if os.path.exists(path):
            raise FileExistsError("Data base already exist. Path: %s" % os.path.abspath(path))
        self.db_path = path
        conn = sqlite3.connect(self.db_path)
        self.__create_db(conn)
        conn.close()

    def set_channel_downloaded(self, channel_id):
        """
        This function process next cases:
            * valid==False, scrapped==False, downloaded==True
        If you want got more information, see class description
        """
        raise Exception("Not implemented")

    def set_video_descr(self, video):
        raise Exception("Not implemented")

    def check_video_descr(self, video_id):
        raise Exception("Not implemented")

    def set_empty_channels(self, channel_ids):
        raise Exception("Not implemented")

    @staticmethod
    def __create_args_update_channels(channel, scrapped, valid):
        return [
            channel['channel_id'],
            valid,
            scrapped,
            False,
            channel['priority'],
            channel['full_description'],
            channel['short_description']
        ]

    @staticmethod
    def __deduplicate_channels(channels):
        s = set()
        error = None
        output_channels = []
        for channel in channels:
            if channel['channel_id'] not in s:
                output_channels.append(channel)
                s.add(channel['channel_id'])
                continue
            error = utils.CacheError(
                channel_id=channel['channel_id'],
                msg="This channel already exists into input channels",
                e=error
            )
        return output_channels, error

    def update_channels(self, channels, scrapped, valid):
        """
        This function process next cases:
            * valid==True, scrapped==True, downloaded==False
            * valid==True, scrapped==False, downloaded==False
            * valid==False, scrapped==False, downloaded==False
        If you want got more information, see class description
        """

        conn = sqlite3.connect(self.db_path)
        channels, error = self.__deduplicate_channels(channels)
        for channel in channels:
            c = conn.cursor()
            c.execute(self.__sql_select_exist_channel, (channel['channel_id']))
            res = c.fetchone()
            c.close()
            query = self.__sql_insert_channel
            args = self.__create_args_update_channels(channel, scrapped, valid)
            if res is not None and len(res) != 0:
                error = utils.CacheError(channel_id=channel['channel_id'], msg="This channel already exists", e=error)
                query = self.__sql_update_channel
                args.append(channel['channel_id'])
            conn.execute(query, args)
        conn.commit()
        conn.close()
        return error

    def get_best_channel_id(self):
        raise Exception("Not implemented")
