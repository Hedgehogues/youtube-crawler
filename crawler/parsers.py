from crawler.loaders import Tab

from jq import jq


class PageDescription:
    def __init__(self):
        self.channel_descrs = {}

    def __getitem__(self, key):
        return self.channel_descrs['channels'][key]


class BaseParser:
    def __init__(self, tab, max_page=1, jq_path='jq/videos.jq'):
        if max_page is not None and max_page < 1:
            raise AttributeError("Attribute max_page must be more 0")
        self.max_page = max_page
        self.tab = tab
        with open(jq_path) as fd_fq:
            self._jq_load = jq(fd_fq.read())

    def _parse(self, player_config, data_config):
        data = self._jq_load.transform(data_config)
        return [data], None

    def parse(self, player_config, data_config):
        return self._parse(player_config, data_config)


class ReloaderParser(BaseParser):
    def __init__(self, tab, max_page, data_key, jq_load_path, jq_reload_path):
        super().__init__(tab, max_page, jq_load_path)

        with open(jq_reload_path) as fd_fq:
            self._jq_reload = jq(fd_fq.read())
        self._next_page_token = None
        self._data_key = data_key

    def _parse(self, player_config, data_config):
        data = self._jq_load.transform(data_config)
        itct = data['next_page_token']['itct']
        next_page_descr = data['next_page_token']['ctoken']
        if next_page_descr is not None and itct is not None:
            return data[self._data_key], {
                'ctoken': next_page_descr,
                'itct':  itct,
            }
        return [data[self._data_key]], None

    def parse(self, player_config, data_config):
        return self._parse(player_config, data_config)

    def _reload_parse(self, data_config):
        data = self._jq_reload.transform(data_config)
        itct = data['next_page_token']['itct']
        next_page_descr = data['next_page_token']['ctoken']
        if next_page_descr is not None and itct is not None:
            return data[self._data_key], {
                'ctoken': next_page_descr,
                'itct':  itct,
            }
        return data[self._data_key], None

    def reload_parse(self, data_config):
        return self._reload_parse(data_config)


class VideosParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='jq/videos.jq', jq_reload_path='jq/videos_reload.jq'):
        super().__init__(Tab.Videos, max_page, 'videos', jq_load_path, jq_reload_path)
        self.max_page = max_page


class ChannelsParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='jq/channels.jq', jq_reload_path='jq/channels_reload.jq'):
        super().__init__(Tab.Channels, max_page, 'channels', jq_load_path, jq_reload_path)


class AboutParser(BaseParser):
    def __init__(self, jq_path='jq/about.jq'):
        super().__init__(Tab.About, 1, jq_path)


class HomePageParser(BaseParser):
    def __init__(self, jq_path='jq/home_page.jq'):
        super().__init__(Tab.HomePage, 1, jq_path)
