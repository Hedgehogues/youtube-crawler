import os
import sqlite3


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
      description text
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

    # __sql_update_channel = '''
    # update %s
    # set
    #   channel_id=?,
    #   valid=?,
    #   scrapped=?,
    #   downloaded=?,
    #   priority=?,
    #   full_description=?,
    #   short_description=?
    # where channel_id=?;
    # ''' % __sql_query_create_channel

    __sql_update_channel = '''
    update videos 
    set
      channel_id=?;
    '''

    __sql_insert_channel = '''
    insert into channels(channel_id) 
    values(?)
    '''

    __sql_select_channel = '''
    select channel_id from channels 
    '''

    def __create_db(self, conn):
        c = conn.cursor()
        c.execute(self.__sql_query_create_channel)
        c.execute(self.__sql_query_create_videos)
        conn.commit()
        c.close()

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
        return (
            channel['channel_id'],
            # valid,
            # scrapped,
            # False,
            # channel['priority'],
            # channel['full_description'],
            # channel['short_description'],
            # channel['channel_id']
        )

    def update_channels(self, channels, scrapped, valid):
        """
        This function process next cases:
            * valid==True, scrapped==True, downloaded==False
            * valid==True, scrapped==False, downloaded==False
            * valid==False, scrapped==False, downloaded==False
        If you want got more information, see class description
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        errors = []
        for channel in channels:
            c.execute(self.__sql_select_channel)
            args = self.__create_args_update_channels(channel, scrapped, valid)
            query = self.__sql_insert_channel
            res = c.fetchone()
            if res is not None and len(res) != 0:
                errors.append("")
                query = self.__sql_update_channel
            conn.execute(query, args)
        conn.commit()
        c.close()

    def get_best_channel_id(self):
        raise Exception("Not implemented")
