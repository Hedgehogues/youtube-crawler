import sqlite3


class DBSqlLiteCache:
    __channels_table_name = 'channels'
    __videos_table_name = 'videos'

    __sql_query_create_channel = '''
    create table %s (
      channel_id text PRIMARY KEY,
      download boolean,
      priority float,
      valid boolean, -- Scrapper set flag VALID==TRUE
      preload boolean, -- If FALSE then there is only channel_id else there is other fields
      full_description text,
      short_description text
    );''' % __channels_table_name

    __sql_query_create_videos = '''
    create table %s (
      video_id text,
      channel_id text,
      full_descr text,
      short_descr text,
      subtitles text,
      valid boolean,
      priority float
    );''' % __videos_table_name

    def __is_exist_db(self):
        return True

    def __create_db(self):
        c = self.conn.cursor()
        c.execute(self.__sql_query_create_channel)
        c.execute(self.__sql_query_create_videos)
        self.conn.commit()
        c.close()

    def __drop_db(self):
        c = self.conn.cursor()
        c.execute('drop table %s;' % self.__videos_table_name)
        c.execute('drop table %s;' % self.__channels_table_name)
        self.conn.commit()
        c.close()

    def __init__(self, path='data/db.sqlite', hard=False):
        self.conn = sqlite3.connect(path)

        if hard:
            self.__drop_db()
        if not self.__is_exist_db():
            self.__create_db()

    def set_channel_scrapped(self, channel_id):
        raise Exception("Not implemented")

    def set_channel_downloaded(self, channel_id):
        raise Exception("Not implemented")

    def set_video_descr(self, video):
        raise Exception("Not implemented")

    def check_video_descr(self, video_id):
        raise Exception("Not implemented")

    def set_empty_channels(self, channel_ids):
        raise Exception("Not implemented")

    def set_channel(self, channels):
        raise Exception("Not implemented")

    def update_channels(self, channel_id, channels):
        raise Exception("Not implemented")

    def get_best_channel_id(self):
        raise Exception("Not implemented")
