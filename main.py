from crawler.cache import DBSqlLiteCache, DB_MOD
from crawler.crawler import YoutubeCrawler
from crawler.loaders import Loader, Reloader, YoutubeDlLoader
from crawler.scrapper import Scrapper
from crawler import parsers


def sep(x):
    if len(x) < 2:
        return ''
    z = x.replace('\n', '').split('/')
    if len(z[-1]) == 0:
        return z[-2]
    return z[-1]


fd = open('data/base_channels.tsv')
l = fd.readlines()
channel_ids = list(filter(lambda x: len(x) > 0, map(sep, l)))

x = YoutubeCrawler(cache=DBSqlLiteCache(db_mod=DB_MOD.OLD), max_attempts=1)
x.process(channel_ids)

print('Finish')

