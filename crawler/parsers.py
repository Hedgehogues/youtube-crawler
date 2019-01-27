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
            self._jq = jq(fd_fq.read())

        self._next_page_token = {
            'ctoken': '',
            'itct': '',
        }

    def parse(self, player_config, data_config):
        data = self._jq.transform(data_config)
        return data, self._next_page_token


class VideosParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/videos.jq'):
        self.max_page = max_page
        super().__init__(Tab.Videos, max_page, jq_path)

    def parse(self, player_config, data_config):
        data = self._jq.transform(data_config)
        itct = data['page_loader']['itct']
        next_page_descr = data['page_loader']['ctoken']
        next_page_descr = {
            'ctoken': '' if next_page_descr is None else next_page_descr,
            'itct': '' if itct is None else itct,
        }
        return data['owner_videos'], next_page_descr


class AboutParser(BaseParser):
    def __init__(self, jq_path='jq/about.jq'):
        super().__init__(Tab.About, 1, jq_path)


class CommunityParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/videos'):
        super().__init__(Tab.Community, max_page, jq_path)

    def parse(self, player_config, data_config):
        data = self._jq.transform(data_config)
        c_token = data
        return data, c_token


class ChannelsParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/channels.jq'):
        super().__init__(Tab.Channels, max_page, jq_path)

    def parse(self, player_config, data_config):
        data = self._jq.transform(data_config)
        c_token = data
        return data, c_token


class HomePageParser(BaseParser):
    def __init__(self, jq_path='jq/home_page.jq'):
        super().__init__(Tab.HomePage, 1, jq_path)
