from jq import jq
from crawler import utils
from crawler.loaders import Tab
from crawler.utils import ReloadTokenError


class BaseParser:
    def __init__(self, jq_path, max_page=1):
        """
        This parser loads the only page

        :param max_page (int): max page of
        :param jq_path (str): path to jq-script of load data
        """
        if max_page is not None and max_page < 1:
            raise AttributeError("Attribute max_page must be more 0")
        self.max_page = max_page
        with open(jq_path) as fd_fq:
            self._jq_load = jq(fd_fq.read())

    def is_final_page(self):
        return True

    def parse(self, data_config, is_reload):
        if is_reload:
            raise ReloadTokenError("This parser not implement reload options. Token cannot be received")
        data = self._jq_load.transform(data_config)
        return data, None


class ReloaderParser(BaseParser):
    def __init__(self, max_page, tab, jq_load_path, jq_reload_path):
        """
        This parser loads first page and reload next pages

        :param max_page (int): max page of
        :param tab (Tab(Enum)): tab was defined type of parser
        :param jq_load_path (str): path to jq-script of load data
        :param jq_reload_path (str): path to jq-script of reload data
        """
        super().__init__(max_page=max_page, jq_path=jq_load_path)

        self.__count_pages = 0
        with open(jq_reload_path) as fd_fq:
            self._jq_reload = jq(fd_fq.read())
        self.next_page_token = None
        self.tab = tab

    def is_final_page(self):
        return not (self.max_page is None or self.__count_pages < self.max_page)

    def parse(self, data_config, is_reload):
        self.__count_pages += 1
        data = self._jq_load.transform(data_config)
        try:
            itct = data['next_page_token']['itct']
            next_page_token = data['next_page_token']['ctoken']
        except Exception as e:
            raise utils.ParserError("Next page token is not available", e)
        if next_page_token is not None and itct is not None:
            return data[self.tab], {
                'ctoken': next_page_token,
                'itct':  itct,
            }
        return data[self.tab], None


class VideosParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='crawler/jq/videos.jq', jq_reload_path='crawler/jq/videos_reload.jq'):
        """
        This parser loads the pages with videos

        :param max_page (int): max page of
        :param tab (Tab.Enum): tab was defined type of parser
        :param jq_load_path (str): path to jq-script of load data
        :param jq_reload_path (str): path to jq-script of reload data
        """
        super().__init__(max_page, Tab.Videos, jq_load_path, jq_reload_path)
        self.max_page = max_page


class ChannelsParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='crawler/jq/channels.jq', jq_reload_path='crawler/jq/channels_reload.jq'):
        """
        This parser loads the pages with channels

        :param max_page (int): max page of
        :param tab (Tab.Enum): tab was defined type of parser
        :param jq_load_path (str): path to jq-script of load data
        :param jq_reload_path (str): path to jq-script of reload data
        """
        super().__init__(max_page, Tab.Channels, jq_load_path, jq_reload_path)


class AboutParser(BaseParser):
    def __init__(self, jq_path='crawler/jq/about.jq'):
        """
        This parser loads the page with description channel

        :param jq_path (str): path to jq-script of load data
        """
        super().__init__(jq_path=jq_path, max_page=1)


class HomePageParser(BaseParser):
    def __init__(self, jq_path='crawler/jq/home_page.jq'):
        """
        This parser loads the home page channel

        :param jq_path (str): path to jq-script of load data
        """
        super().__init__(jq_path=jq_path, max_page=1)
