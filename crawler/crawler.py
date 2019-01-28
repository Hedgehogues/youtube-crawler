from crawler import parsers
from crawler.filter import Filter
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper


class YoutubeCrawler:
    def __init__(self, scraper=None, cache_path='~', max_attempts=5):
        self._cache_path = cache_path
        self._scraper = scraper
        if self._scraper is None:
            self._init_none_scraper()

        self.used_channels_ = {}

    def _init_none_scraper(self):
        loader = Loader()
        reloader = Reloader()
        ydl_loader = YoutubeDlLoader()
        filter = Filter()
        scrapper = Scrapper(
            loader, reloader, ydl_loader,
            [
                parsers.HomePageParser(),
                parsers.VideosParser(max_page=10),
                parsers.ChannelsParser(max_page=3),
                parsers.AboutParser(),
            ],
            channel_filter=filter
        )
        self._scraper = scrapper

    def _dfs(self, channel_id):
        self.count_ += 1
        channel = self._scraper.parse(channel_id)
        if not channel[Tab.Meta]['is_valid']:
            return
        self.used_channels_[channel_id] = channel
        for item in channel.channels:
            if item['channel_id'] not in self.used_channels_:
                self._dfs(item['channel_id'])
        return

    def process(self, channel_ids):
        self.used_channels_ = {}
        self.count_ = 0
        for v in channel_ids:
            if v not in self.used_channels_:
                self._dfs(v)
        return
