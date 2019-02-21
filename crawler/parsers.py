from crawler import jq
from crawler.loaders import Tab


class BaseParser:
    def __init__(self, jq_path, max_page=1):
        if max_page is not None and max_page < 1:
            raise AttributeError("Attribute max_page must be more 0")
        self.max_page = max_page
        self.__count_pages = 0
        with open(jq_path) as fd_fq:
            self._jq_load = jq.jq(fd_fq.read())

    def is_final_page(self):
        return self.max_page is None or self.__count_pages < self.max_page

    def parse(self, data_config):
        self.__count_pages += 1
        data = self._jq_load.transform(data_config)
        return data, None


class ReloaderParser(BaseParser):
    def __init__(self, max_page, tab, jq_load_path, jq_reload_path):
        """
        :param max_page (int): max page of
        :param tab (Tab.Enum): tab was defined type of parser
        :param jq_load_path (str):
        :param jq_reload_path (str):
        """
        super().__init__(max_page, jq_load_path)

        with open(jq_reload_path) as fd_fq:
            self._jq_reload = jq.jq(fd_fq.read())
        self.next_page_token = None
        self.tab = tab

    def parse(self, data_config):
        self.__count_pages += 1
        data = self._jq_load.transform(data_config)
        itct = data['next_page_token']['itct']
        next_page_descr = data['next_page_token']['ctoken']
        if next_page_descr is not None and itct is not None:
            return data[self.tab], {
                'ctoken': next_page_descr,
                'itct':  itct,
            }
        return data[self.tab], None


class VideosParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='crawler/jq/videos.jq', jq_reload_path='crawler/jq/videos_reload.jq'):
        super().__init__(max_page, Tab.Videos, jq_load_path, jq_reload_path)
        self.max_page = max_page


class ChannelsParser(ReloaderParser):
    def __init__(self, max_page=None, jq_load_path='crawler/jq/channels.jq', jq_reload_path='crawler/jq/channels_reload.jq'):
        super().__init__(max_page, Tab.Channels, jq_load_path, jq_reload_path)


class AboutParser(BaseParser):
    def __init__(self, jq_path='crawler/jq/about.jq'):
        super().__init__(jq_path=jq_path, max_page=1)


class HomePageParser(BaseParser):
    def __init__(self, jq_path='crawler/jq/home_page.jq'):
        super().__init__(jq_path=jq_path, max_page=1)
