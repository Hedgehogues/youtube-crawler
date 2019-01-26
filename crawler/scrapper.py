from crawler.loaders import Loader, Tab
from crawler.parsers import HomePageParser


class Scrapper:
    def __init__(self, loader, parsers=None, logger=None):
        self._parsers = parsers if parsers is not None else []
        self._loader = loader
        self._is_parsed = False

        self.channel_descr_ = {}
        self.logger = logger

    def parse(self, channel_id, force=False):
        if self._is_parsed and not force:
            return
        self._is_parsed = True
        self.channel_descr_ = {}
        for p in self._parsers:
            player_config, data_config = self._loader.load(channel_id, p.tab)
            self.channel_descr_[p.name] = p.parse(player_config, data_config)

    def dump(self, fd):
        pass

    def download(self):
        if self._is_parsed:
            raise Exception("Videos not parsed")
        # TODO: реализовать обкачку видео, инорфмацию по которым скачали
        # TODO: логгировать все статусы обкачки для того, чтобы можно было возобновить обкачку с прежнего места

    def get_all_videos(self, only_id=True):
        if only_id:
            return self.channel_descr_[Tab.Videos]
        return self.channel_descr_[Tab.Videos]

    def get_all_channels(self, only_id=True):
        channels = []
        for channel in self.channel_descr_:
            if only_id:
                channels += channel
                continue
            channels += channel
        return channels


channel_id = 'UCSoYSTOt1g_Vdo8xCJeQpHw'
l = Loader()
Scrapper(l, [HomePageParser(), HomePageParser()]).parse(channel_id)
