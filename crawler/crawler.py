from crawler import parsers
from crawler.cache import DBCache
from crawler.filter import Filter
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper


class YoutubeCrawler:
    def __init__(self, logger, cache=None, scraper=None, max_attempts=5):
        self.__logger = logger

        self.__cache = cache
        if self.__cache is None:
            self.__cache = DBCache()

        self.__scraper = scraper
        if self.__scraper is None:
            self.__init_none_scraper(self.__logger)

        self.used_channels_ = {}

    def __init_none_scraper(self, logger):
        loader = Loader()
        reloader = Reloader()
        ydl_loader = YoutubeDlLoader()
        filter = Filter()
        scrapper = Scrapper(
            loader=loader, reloader=reloader, ydl_loader=ydl_loader,
            parsers=[
                parsers.HomePageParser(),
                parsers.VideosParser(max_page=10),
                parsers.ChannelsParser(max_page=3),
                parsers.AboutParser(),
            ],
            logger=logger,
            channel_filter=filter
        )
        self.__scraper = scrapper

    def process(self, channel_ids=None):
        if channel_ids is None:
            self.__cache.read_channel(False, None, False)
        return
