from crawler.cache import DBSqlLiteCache
from crawler.crawler import YoutubeCrawler
from crawler.loaders import Loader, Reloader, YoutubeDlLoader
from crawler.scrapper import Scrapper
from crawler import parsers


channel_ids = ['UCzAzPC4VWIMHqrnIM1iBPsQ']

x = YoutubeCrawler(cache=DBSqlLiteCache(hard=True), max_attempts=1)
x.process(channel_ids)

print('Finish')

