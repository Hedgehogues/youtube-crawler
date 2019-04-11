from crawler.cache import DBSqlLiteCache
from crawler.crawler import YoutubeCrawler
from crawler.loaders import Loader, Reloader, YoutubeDlLoader
from crawler.scrapper import Scrapper
from crawler import parsers


channel_id = ['UCzAzPC4VWIMHqrnIM1iBPsQ']

x = YoutubeCrawler(cache=DBSqlLiteCache(hard=True))
x.process(channel_id)


loader = Loader()
reloader = Reloader()
ydl_loader = YoutubeDlLoader()
scrapper = Scrapper(
    loader, reloader, ydl_loader,
    [
        parsers.HomePageParser(),
        parsers.VideosParser(max_page=10),
        parsers.ChannelsParser(max_page=3),
        parsers.AboutParser(),
    ]
)
descr = scrapper.parse(channel_id)
# scrapper.download(descr[Tab.Videos][1]['video_id'])
print(descr)

