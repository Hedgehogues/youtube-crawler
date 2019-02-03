from crawler import parsers, utils
from crawler.cache import DBSqlLiteCache
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper
from crawler.simple_logger import SimpleLogger


class BaseCrawler:
    def __init__(self, logger, max_attempts=5):
        self.__max_attempts = max_attempts

        self.__logger = logger
        if self.__logger is None:
            self.__logger = SimpleLogger()

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
        if err_cond is not None:
            self.__logger.warn(err)

    def _alert(self, err_cond, err):
        if err_cond is not None:
            self.__logger.alert(err)

    def _error(self, err_cond, err):
        if err_cond is not None:
            self.__logger.error(err)


class YoutubeCrawler(BaseCrawler):
    # * TODO: Если загрузка была прервана, то все видео начинают обкачиваться заново. При этом, если скраперу было
    #   TODO: указано скачать не все видео, а только часть, то при повторной загрузке, будет выбран другой набор видео

    # * TODO: Скрапер обкачивает k видео, а Crawler m из них может отбраковать, после чего не скачает новые k - m видео

    def __init__(self, logger=None, cache=None, ydl_loader=None, scraper=None, video_validator=None,
                 channel_validator=None, max_attempts=5):
        super().__init__(logger, max_attempts)

        self.__cache = cache
        if self.__cache is None:
            self.__cache = DBSqlLiteCache()

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
        scrapper = Scrapper(
            loader=loader, reloader=reloader,
            parsers=[
                parsers.HomePageParser(),
                parsers.VideosParser(max_page=10),
                parsers.ChannelsParser(max_page=3),
                parsers.AboutParser(),
            ],
            logger=logger
        )
        self.__scraper = scrapper

    @staticmethod
    def __create_video(video_id, channel_id, full_descr, short_descr):
        subtitles = full_descr['subtitles']
        valid = short_descr['valid']  # TODO: вынести в crawler из scrapper
        priority = short_descr['priority']  # TODO: вынести в crawler из scrapper

        del full_descr['subtitles']
        del short_descr['valid']
        del short_descr['priority']
        return {
            'video_id': video_id,
            'channel_id': channel_id,
            'full_description': full_descr,
            'short_description': short_descr,
            'subtitles': subtitles,
            'valid': valid,
            'priority': priority
        }

    @staticmethod
    def __create_channel(channel_id, download, preload, descr):
        valid = True
        priority = 0

        return [{
            'channel_id': channel_id,
            'download': download,
            'priority': priority,
            'valid': valid,
            'preload': preload,
            'full_description': descr,
        }]

    def __extract_channels(self, descr):
        raise utils.CrawlerExceptions("Not implemented")
        return descr

    def __download_videos(self, descrs):
        channel_id = descrs[Tab.HomePage]['owner_channel']['id']
        for short_video_descr in descrs[Tab.Videos]:
            video_id = short_video_descr['id']

            self._info("Check in Cache videoId: %s" % video_id)
            err = self.__cache.check_video_descr(video_id)
            if err is None:
                self._info("Such video already exist. VideoId: %d" % video_id)
                continue

            self._info("Download video (videoId: %s) from youtube" % video_id)
            full_video_descr, err = self._apply(self.__video_downloader.load(short_video_descr))
            self._warn(err, err)

            data = self.__create_video(video_id, channel_id, full_video_descr, short_video_descr)
            err = self.__cache.set_video_descr(data)
            self._alert(err, err)

    def process(self, channel_ids=None):
        self._info("Setting channel ids from arguments into Cache")
        err = self.__cache.set_empty_channels(channel_ids)
        ch_ids_str = ','.join(channel_ids)
        self._alert(err, err + "%s: [%s]" % ("ChannelIds", ch_ids_str))

        self._info("Getting first channel from Cache")
        channel_id, err = self.__cache.get_best_channel_id()
        self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

        while channel_id is not None:
            self._info("Scrappy channelId: %s" % channel_id)
            descr, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self._warn(err, utils.ScrapperError(channel_id=channel_id, e=err))
            if err is not None:
                continue

            self._info("Setting current channel into Cache. ChannelId: %s" % channel_id)
            data = self.__create_channel(channel_id, False, True, descr)
            err = self.__cache.update_channels(data)
            self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

            data = self.__extract_channels(descr)
            ch_ids_str = ','.join([ch['id'] for ch in data])
            self._info("Setting neighbours channels into Cache. ChannelIds: %s" % ch_ids_str)
            err = self.__cache.update_channels(data)
            self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

            self._info("Downloading youtube for ChannelId: %s" % channel_id)
            self.__download_videos(descr)

            self._info("Getting next channel from Cache")
            channel_id, err = self.__cache.get_best_channel_id()
            self._error(err, err + self.__crash_msg % ("ChannelIds", channel_id))
