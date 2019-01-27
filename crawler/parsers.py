from crawler.loaders import Tab

from jq import jq


class BaseParser:
    def __init__(self, tab, jq_path='jq/videos.jq'):
        self.tab = tab
        with open(jq_path) as fd_fq:
            fd = fd_fq.read()
            self._jq = jq(fd)

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        x = self._jq.transform(data_config)
        return


class VideosParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/videos.jq'):
        self.max_page = max_page
        super().__init__(Tab.Videos, jq_path)


class AboutParser(BaseParser):
    def __init__(self, jq_path='jq/about.jq'):
        super().__init__(Tab.About, jq_path)


class CommunityParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/videos'):
        self.max_page = max_page
        super().__init__(Tab.Community, jq_path)


class ChannelsParser(BaseParser):
    def __init__(self, max_page=None, jq_path='jq/channels.jq'):
        self.max_page = max_page
        super().__init__(Tab.Channels, jq_path)


class HomePageParser(BaseParser):
    def __init__(self, jq_path='jq/home_page.jq'):
        super().__init__(Tab.HomePage, jq_path)
