from crawler import parsers
from crawler.loaders import Loader, Reloader, Tab


class Scrapper:
    """
    Scrapper download concrete channel with (or without video) from Youtube.

    loader : crawler.loaders.Loader
        This object must satisfy the interface `crawler.loaders.Loader`.
        Loader download and extract json with data from next pages:
            * featured
            * videos
            * channels
            * about
            * TODO: community
        If you want to add new pages, you should be add new constants int crawler.loaders.Tab
    """
    def __init__(self, loader, reloader, parsers=None, logger=None, channel_descr_dumper=None, hard=True, channel_filter=None):
        self._hard = hard

        self._parsers = parsers if parsers is not None else []
        self._reloader = reloader
        self._loader = loader
        self._channel_descr_dumper = channel_descr_dumper
        self._channel_filter = channel_filter

        self._logger = logger

        self._query_params = {
            Tab.HomePage: None,
            Tab.Videos: {'flow': 'grid', 'view': '0'},
            Tab.Channels: {'flow': 'grid', 'view': '56'},
            Tab.About: None,
        }

    def _reload_pages(self, p, next_page_token):
        count_pages = 1
        descr_slice = []
        while (p.max_page is None or count_pages < p.max_page) and next_page_token is not None:
            # TODO: добавить логгирование
            count_pages += 1
            data_config = self._reloader.load(next_page_token)
            descr, next_page_token = p.reload_parse(data_config)
            descr_slice += descr
        return descr_slice

    def _dump(self, descr):
        with open(descr, 'w') as fd:
            self._channel_descr_dumper.dump(fd, descr)

    def parse(self, channel_id):
        # TODO: добавить логгирование
        channel_descr = {}
        for p in self._parsers:
            player_config, data_config = self._loader.load(channel_id, p.tab, self._query_params[p.tab])
            descr, next_page_token = p.parse(player_config, data_config)
            channel_descr[p.tab] = descr + self._reload_pages(p, next_page_token)
        return channel_descr

    def download(self, channel_id, descr_videos):
        # TODO: реализовать обкачку видео, инорфмацию по которым скачали
        # TODO: логгировать все статусы обкачки для того, чтобы можно было возобновить обкачку с прежнего места
        pass


channel_id = 'UCO08VxZ3ZsYi5-TIsO3dvFw'
loader = Loader()
reloader = Reloader()
Scrapper(
    loader, reloader,
    [
        parsers.HomePageParser(),
        parsers.VideosParser(max_page=3),
        parsers.ChannelsParser(max_page=None),
        parsers.AboutParser(),
    ]
).parse(channel_id)
