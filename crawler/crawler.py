from crawler import parsers
from crawler.cache import DBCache
from crawler.filter import Filter
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper


class BaseCrawler:
    def __init__(self, max_attempts=5):
        self.__max_attempts = max_attempts

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


class YoutubeCrawler(BaseCrawler):
    def __init__(self, logger, cache=None, ydl_loader=None, scraper=None, videos_per_ch=None, max_attempts=5):
        super().__init__(max_attempts)
        self.__logger = logger
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

        self.used_channels_ = {}

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

            err = self.__cache.read_video_descr(video_id)
            if err is None:
                msg = "Download is failed! Video already in DB. VideoId: %s. Program is finishing..."
                msg = msg % video_id
                self.__logger.error(err, msg)
                raise err

            descr, err = self._apply(self.__video_downloader.load(descr_short))
            self.__logger.error(err, "Problem with downloading video from youtube")

            err = self.__cache.set_video_descr(video_id, {'full_descr': descr, 'short_descr': descr})
            self.__logger.error(err, "Problem with set video info into DB. VideoId: %s" % video_id)

    def __base_channels_process(self, channel_ids):
        if channel_ids is None:
            return

        err = self.__cache.set_channels(channel_ids, None)
        msg = "Some channels were downloaded already or problem with set video info into DB. Base channels"
        self.__logger.error(err, msg)

        channel_ids_, err = self.__cache.read_channels(ordered=False, count=None, downloaded=False)
        self.__logger.error(err, "Problem with reading channel info from DB. Base channels")

        for channel_id in channel_ids_:
            descrs, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self.__logger.error(err, "Scrapper was failed. ChannelId: %s" % channel_id)
            self.__download_videos(descrs)

    def process(self, channel_ids=None):
        self.__base_channels_process(channel_ids)

        channel_id, err = self.__cache.read_channels(ordered=True, count=1, downloaded=False)
        self.__logger.error(err, "Problem with reading channel info from DB")

        while channel_id is not None:
            descrs, err = self._apply(lambda: self.__scraper.parse(channel_id))
            self.__logger.error(err, "Scrapper was failed. ChannelId: %s" % channel_id)
            self.__download_videos(descrs)

            channel_id = self.__cache.read_channels(ordered=True, count=1, downloaded=False)
            self.__logger.error(err, "Problem with reading channel info from DB")
