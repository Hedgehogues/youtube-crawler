import sqlite3


class DBCache:
    def __create_db(self):
        c = self.conn.cursor()
        c.execute('''create table video (date text, trans text, symbol text, qty real, price real)''')
        c.execute('''create table video (date text, trans text, symbol text, qty real, price real)''')
        self.conn.commit()
        c.close()

    def __init__(self, path='data/db.sql'):
        self.conn = sqlite3.connect(path)

    def write_channels(self, channels):
        raise Exception("Not implemented")

    def read_channels(self, ordered=False, count=None, downloaded=False):
        raise Exception("Not implemented")
