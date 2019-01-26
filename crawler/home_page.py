from crawler.loader import Loader, Tab


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


class VideosParser:
    def __init__(self, max_page=None, jq_path='jq/videos.jq', download=0):
        self.max_page_ = max_page
        self.tab_ = Tab.Videos
        with open(jq_path) as fd_fq:
            self._jq_pattern = fd_fq.read()

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        print(player_config, data_config)
        return


class AboutParser:
    def __init__(self, jq_path='jq/about.jq'):
        self.tab_ = Tab.HomePage
        with open(jq_path) as fd_fq:
            self._jq_pattern = fd_fq.read()

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        print(player_config, data_config)
        return


class CommunityParser:
    def __init__(self, max_page=None):
        self.tab_ = Tab.Community
        self.max_page_ = max_page

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        print(player_config, data_config)
        return


class ChannelsParser:
    def __init__(self, max_page=None, jq_path='jq/channels.jq'):
        self.tab_ = Tab.Channels
        self.max_page_ = max_page
        with open(jq_path) as fd_fq:
            self._jq_pattern = fd_fq.read()

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        print(player_config, data_config)
        return


class HomePageParser:
    def __init__(self, jq_path='jq/home_page.jq'):
        self.tab_ = Tab.HomePage
        with open(jq_path) as fd_fq:
            self._jq_pattern = fd_fq.read()

    def get_channels(self):
        return []

    def parse(self, player_config, data_config):
        print(player_config, data_config)
        return


channel_id = 'UCSoYSTOt1g_Vdo8xCJeQpHw'
l = Loader()
Scrapper(l, [HomePageParser(), HomePageParser()]).parse(channel_id)
