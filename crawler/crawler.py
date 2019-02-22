from crawler import parsers, utils
from crawler.cache import DBSqlLiteCache
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper
from crawler.simple_logger import SimpleLogger


class BaseCrawler:
    # TODO: переписать на StateMachine
    def __init__(self, logger, max_attempts=5):
        self.__max_attempts = max_attempts

        self._logger = logger
        if self._logger is None:
            self._logger = SimpleLogger()

    def _apply(self, fn):
        count = 0
        e = None
        while count < self.__max_attempts:
            try:
                return fn(), None
            except e:
                count += 1
        return None, e

    def _info(self, msg):
        self._logger.info(msg)

    def _warn(self, err_cond, err):
        if err_cond is not None:
            self._logger.warn(err)

    def _alert(self, err_cond, err):
        if err_cond is not None:
            self._logger.alert(err)

    def _error(self, err_cond, err):
        if err_cond is not None:
            self._logger.error(err)


class YoutubeCrawler(BaseCrawler):
    # * TODO: Если загрузка была прервана, то все видео начинают обкачиваться заново. При этом, если скраперу было
    #   TODO: указано скачать не все видео, а только часть, то при повторной загрузке, будет выбран другой набор видео

    # * TODO: Скрапер обкачивает k видео, а Crawler m из них может отбраковать, после чего не скачает новые k - m видео

    def __init__(self, logger=None, cache=None, ydl_loader=None, scraper=None, max_attempts=5):
        super().__init__(logger, max_attempts)

        self.__cache = cache
        if self.__cache is None:
            self.__cache = DBSqlLiteCache()

        self.__video_downloader = ydl_loader
        if self.__video_downloader is None:
            self.__video_downloader = YoutubeDlLoader()

        self.__scraper = scraper
        if self.__scraper is None:
            self.__init_none_scraper()

        self.__crash_msg = "Channel from Cache isn't got. %s: [%s]. Crawler interrupts execute..."

    def __init_none_scraper(self):
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
            logger=self._logger
        )
        self.__scraper = scrapper

    @staticmethod
    def __create_video(video_id, channel_id, full_descr, short_descr):
        subtitles = full_descr['subtitles']
        # TODO: заменить на алгоритмы valid и priority
        valid = True
        priority = 0

        del full_descr['subtitles']
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
    def __create_cur_channel(channel_id, download, preload, descr):
        # TODO: заменить на алгоритмы valid и priority
        valid = True
        priority = 0

        return {
            'channel_id': channel_id,
            'download': download,
            'priority': priority,
            'valid': valid,
            'preload': preload,
            'full_description': descr,
        }

    @staticmethod
    def __get_neighb_channels(descr):
        channels = []
        for page in descr[Tab.Channels]:
            channels.append(page['channels'])
        return channels

    def __download_videos(self, descrs):
        channel_id = descrs[Tab.HomePage]['owner_channel']['id']
        for short_video_descr in descrs[Tab.Videos]:
            video_id = short_video_descr['id']

            # Check in Cache videoId
            err = self.__cache.check_video_descr(video_id)
            if err is None:
                self._info("Such video already exist. VideoId: %d" % video_id)
                continue

            # self._info("Download video (videoId: %s) from youtube" % video_id)
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

        # Getting first channel from Cache
        channel_id, err = self.__cache.get_best_channel_id()
        self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

        while channel_id is not None:
            self._info("Scrappy channelId: %s" % channel_id)
            descr, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self._warn(err, utils.ScrapperError(channel_id=channel_id, e=err))
            if err is not None:
                continue

            # Channel was scrapped
            channel_id, err = self.__cache.set_channel_scrapped(channel_id)
            self._error(err, err + self.__crash_msg % ("ChannelId", channel_id))

            # Setting current channel into Cache. ChannelId
            channel = self.__create_cur_channel(channel_id, False, True, descr)
            err = self.__cache.set_channel(channel)
            self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

            # Setting neighbours channels into Cache. ChannelId
            neighb_channels = self.__get_neighb_channels(descr)
            ch_ids_str = ','.join([ch['id'] for ch in neighb_channels])
            err = self.__cache.update_channels(channel['id'], neighb_channels)
            self._error(err, err + self.__crash_msg % ("ChannelIds", ch_ids_str))

            # Downloading youtube for ChannelId
            self.__download_videos(descr)

            # Channel was downloaded
            channel_id, err = self.__cache.set_channel_downloaded(channel_id)
            self._error(err, err + self.__crash_msg % ("ChannelId", channel_id))

            # Getting next channel from Cache
            channel_id, err = self.__cache.get_best_channel_id()
            self._error(err, err + self.__crash_msg % ("ChannelIds", channel_id))
