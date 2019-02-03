import sqlite3


class DBSqlLiteCache:
    def __create_db(self):
        c = self.conn.cursor()
        c.execute('''
            create table videos (
                date text,
                trans text,
                symbol text,
                qty real, 
                price real
            )
        ''')
        c.execute('''create table channels (date text, trans text, symbol text, qty real, price real)''')
        self.conn.commit()
        c.close()

    def __init__(self, path='data/db.sql', hard=False):
        self.conn = sqlite3.connect(path)

        if hard:
            # TODO: DROP ALL TABLES
            pass

    def set_video_descr(self, video):
        raise Exception("Not implemented")

    def check_video_descr(self, video_id):
        raise Exception("Not implemented")

    def set_empty_channels(self, channel_ids):
        raise Exception("Not implemented")

    def update_channels(self, channels):
        raise Exception("Not implemented")

    def get_best_channel_id(self):
        raise Exception("Not implemented")
