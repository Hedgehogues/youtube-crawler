from crawler import parsers, utils
from crawler.cache import DBCache
from crawler.filter import Filter
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper


class BaseCrawler:
    def __init__(self, logger, max_attempts=5):
        self.__max_attempts = max_attempts
        self.__logger = logger

    def _apply(self, fn):
        count = 0
        e = None
        while count < self.__max_attempts:
            try:
                return fn(), None
            except e:
                count += 1
        # TODO: допихивать к ошибке информацию про count_attemps
        return None, e

    def _info(self, msg):
        self.__logger.info(msg)

    def _warn(self, err_cond, err):
        self.__logger.warn(err_cond is not None, err)

    def _allert(self, err_cond, err):
        self.__logger.allert(err_cond is not None, err)

    def _error(self, err_cond, err):
        self.__logger.error(err_cond is not None, err)


class YoutubeCrawler(BaseCrawler):
    def __init__(self, logger=None, cache=None, ydl_loader=None, scraper=None, videos_per_ch=None, max_attempts=5):
        super().__init__(logger, max_attempts)
        self.__videos_per_ch = videos_per_ch

        self.__cache = cache
        if self.__cache is None:
            self.__cache = DBCache()

        self.__video_downloader = ydl_loader
        if self.__video_downloader is None:
            self.__video_downloader = YoutubeDlLoader()

        self.__scraper = scraper
        if self.__scraper is None:
            self.__init_none_scraper(self.__logger)

        self.__crash_msg = "Channel from Cache isn't got. %s: [%s]. Crawler interrupts execute..."

    def __init_none_scraper(self, logger):
        loader = Loader()
        reloader = Reloader()
        filter = Filter()
        scrapper = Scrapper(
            loader=loader, reloader=reloader,
            parsers=[
                parsers.HomePageParser(),
                parsers.VideosParser(max_page=10),
                parsers.ChannelsParser(max_page=3),
                parsers.AboutParser(),
            ],
            logger=logger,
            channel_filter=filter
        )
        self.__scraper = scrapper

    def __download_videos(self, descrs):
        for descr_short in descrs[Tab.Videos]:
            video_id = descr_short['id']

            err = self.__cache.get_video_descr(video_id)
            if err is None:
                err = utils.CrawlerExceptions(msg=self.__crash_msg % ("VideoIds", video_id))
                self._error(err, err)

            descr, err = self._apply(self.__video_downloader.load(descr_short))
            self._warn(err, err)

            err = self.__cache.set_video_descr(video_id, {'full_descr': descr, 'short_descr': descr})
            self._allert(err, err)

    def __base_channels_process(self, channel_ids):
        if channel_ids is None:
            self._info("There is not base channels")
            return

        ids = ','.join(channel_ids)
        err = self.__cache.set_channels(channel_ids, None)
        self._allert(err, utils.CacheSetChannelsError(msg="Base channelIds: [%s]" % ids, e=err))

        channel_ids_, err = self.__cache.get_channels(ordered=False, count=None, downloaded=False)
        self._allert(err, utils.CacheGetChannelsError(msg="Base channelIds: [%s]" % ids, e=err))

        for channel_id in channel_ids_:
            descrs, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self._warn(err, utils.ScrapperError(channel_id=channel_id, e=err))
            if err is not None:
                continue

            self.__download_videos(descrs)

    def process(self, channel_ids=None):
        self.__base_channels_process(channel_ids)

        channel_id, err = self.__cache.get_channels(ordered=True, count=1, downloaded=False)
        ch_ids_str = ','.join(channel_ids)
        self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

        while channel_id is not None:
            descrs, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self._warn(err, utils.ScrapperError(channel_id=channel_id, e=err))
            if err is not None:
                continue

            self.__download_videos(descrs)

            channel_id, err = self.__cache.get_channels(ordered=True, count=1, downloaded=False)
            self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))
