import sqlite3


class DBCache:
    def __create_db(self):
        c = self.conn.cursor()
        c.execute('''create table video (date text, trans text, symbol text, qty real, price real)''')
        c.execute('''create table video (date text, trans text, symbol text, qty real, price real)''')
        self.conn.commit()
        c.close()

    def __init__(self, path='data/db.sql', hard=False):
        if hard:
            # TODO: flush db
            pass
        self.conn = sqlite3.connect(path)

    def flush(self):
        raise Exception("Not implemented")

    def set_video_descr(self, video_id, video):
        raise Exception("Not implemented")

    def get_video_descr(self, video_id, ordered=False, count=None, downloaded=False):
        raise Exception("Not implemented")

    def set_channels(self, channel_ids, channels):
        raise Exception("Not implemented")

    def get_channels(self, ordered=False, count=None, downloaded=False):
        raise Exception("Not implemented")
