from crawler import parsers, utils
from crawler.cache import DBSqlLiteCache
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper
from crawler.simple_logger import SimpleLogger


class YoutubeCrawler:
    # TODO: указано скачать не все видео, а только часть, то при повторной загрузке, будет выбран другой набор видео
    # TODO: Скрапер обкачивает k видео, а Crawler m из них может отбраковать, после чего не скачает новые k - m видео

    def __init__(self, logger=None, cache=None, ydl_loader=None, scraper=None, max_attempts=5):
        # TODO: переписать на StateMachine
        self.__max_attempts = max_attempts

        self.logger = logger
        if self.logger is None:
            self.logger = SimpleLogger()

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
            logger=self.logger
        )
        self.__scraper = scrapper

    def _apply(self, fn):
        count = 0
        e = None
        while count < self.__max_attempts:
            try:
                return fn(), None
            except e:
                count += 1
        return None, e

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
    def __create_cur_channel(channel_id, full_descr, short_descr):
        # TODO: заменить на алгоритмы valid и priority
        priority = 0

        return [{
            'channel_id': channel_id,
            'priority': priority,
            'full_description': full_descr,
            'short_description': short_descr,
        }]

    def __get_neighb_channels(self, descr):
        channels = []
        for page in descr[Tab.Channels]:
            for channel in page['channels']:
                channels += self.__create_cur_channel(channel['id'], None, channel)
        return channels

    def __set_failed_channel(self, channel_id):
        try:
            self.__cache.set_failed_channel(channel_id)
        except Exception as e:
            self.logger.alert(e)

    def __download_videos(self, descrs):
        channel_id = descrs[Tab.HomePage]['owner_channel']['id']
        for short_video_descr in descrs[Tab.Videos]:
            video_id = short_video_descr['id']

            # Check in Cache videoId
            err = self.__cache.check_video_descr(video_id)
            if err is None:
                self.logger.info("Such video already exist. VideoId: %d" % video_id)
                continue

            # Download video
            full_video_descr, err = self._apply(self.__video_downloader.load(short_video_descr))
            self.logger.warn(err)

            data = self.__create_video(video_id, channel_id, full_video_descr, short_video_descr)
            err = self.__cache.set_video_descr(data)
            self.logger.alert(err)

    def process(self, channel_ids=None):
        self.logger.info("Setting channel ids from arguments into Cache")
        err = self.__cache.set_base_channels(channel_ids)
        ch_ids_str = ','.join(channel_ids)
        self.logger.alert(err + "%s: [%s]" % ("ChannelIds", ch_ids_str))

        # Getting first channel from Cache
        channel_id, err = self.__cache.get_best_channel_id()
        self.logger.error(err + self.__crash_msg % ("ChannelIds", ch_ids_str))

        while channel_id is not None:
            self.logger.info("Scrappy channelId: %s" % channel_id)
            # Extract full_descr
            full_descr, err = self._apply(lambda: self.__scraper.parse(channel_id))
            try:
                channel = self.__create_cur_channel(channel_id, full_descr, None)
            except Exception as e:
                self.__set_failed_channel(channel_id)
                self.logger.error(e)
                continue

            # Setting current channel into Cache. ChannelId
            try:
                self.__cache.set_channels(channel, scrapped=True, valid=True)
            except Exception as e:
                self.__set_failed_channel(channel_id)
                self.logger.error(e)
                continue

            # Setting neighbours channels into Cache. ChannelId
            neighb_channels = self.__get_neighb_channels(full_descr)
            err = self.__cache.set_channels(neighb_channels, scrapped=False, valid=True)
            ch_ids_str = ','.join([ch['id'] for ch in neighb_channels])
            self.logger.error(err + self.__crash_msg % ("ChannelIds", ch_ids_str))

            # Downloading youtube for ChannelId
            self.__download_videos(full_descr)

            # Channel was downloaded
            channel_id, err = self.__cache.set_channel_downloaded(channel_id)
            self.logger.error(err + self.__crash_msg % ("ChannelId", channel_id))

            # Getting next channel from Cache
            channel_id, err = self.__cache.get_best_channel_id()
            self.logger.error(err + self.__crash_msg % ("ChannelIds", channel_id))
