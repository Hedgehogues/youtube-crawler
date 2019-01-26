from crawler.loaders import Tab


class VideosParser:
    def __init__(self, max_page=None, jq_path='jq/videos.jq'):
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
