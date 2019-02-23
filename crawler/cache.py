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

    __channels_table_name = 'channels'
    __videos_table_name = 'videos'

    __sql_query_create_channel = '''
    create table %s (
      channel_id text PRIMARY KEY,
      valid boolean,
      download boolean,
      priority float,
      description text
    );''' % __channels_table_name

    __sql_query_create_videos = '''
    create table %s (
      channel_id text,
      video_id text PRIMARY KEY,
      valid boolean,
      scrapped boolean,
      download boolean,
      priority float,
      description text
    );''' % __videos_table_name

    def __create_db(self):
        c = self.conn.cursor()
        c.execute(self.__sql_query_create_channel)
        c.execute(self.__sql_query_create_videos)
        self.conn.commit()
        c.close()

    def __init__(self, path='data/db.sqlite', hard=False):
        if hard and os.path.exists(path):
            os.remove(path)

        if os.path.exists(path):
            raise FileExistsError("Data base already exist. Path: %s" % os.path.abspath(path))
        self.conn = sqlite3.connect(path)
        self.__create_db()

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

    def update_channels(self, channels, scrapped, valid):
        """
        This function process next cases:
            * valid==True, scrapped==True, downloaded==False
            * valid==True, scrapped==False, downloaded==False
            * valid==False, scrapped==False, downloaded==False
        If you want got more information, see class description
        """
        raise Exception("Not implemented")

    def get_best_channel_id(self):
        raise Exception("Not implemented")
