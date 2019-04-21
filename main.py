from crawler.cache import DBSqlLiteCache, DB_MOD
from crawler.crawler import YoutubeCrawler
from crawler.loaders import YoutubeDlLoader, YoutubeDlLoaderFormat


def sep(x):
    if len(x) < 2:
        return ''
    z = x.replace('\n', '').split('/')
    if len(z[-1]) == 0:
        return z[-2]
    return z[-1]


fd = open('data/base_channels.tsv')
channel_ids = list(filter(lambda x: len(x) > 0, map(sep, fd.readlines())))
fd.close()

crawler = YoutubeCrawler(
    ydl_loader=YoutubeDlLoader(f=YoutubeDlLoaderFormat.MP3),
    cache=DBSqlLiteCache(db_mod=DB_MOD.OLD),
    max_attempts=5
)
crawler.process(channel_ids)

print('###################### Finish ######################')

