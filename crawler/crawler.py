import logging
import json
from time import sleep

from crawler import parsers, utils
from crawler.cache import DBSqlLiteCache
from crawler.loaders import Loader, Reloader, YoutubeDlLoader, Tab
from crawler.scrapper import Scrapper


class YoutubeCrawler:
    # TODO: указано скачать не все видео, а только часть, то при повторной загрузке, будет выбран другой набор видео
    # TODO: Скрапер обкачивает k видео, а Crawler m из них может отбраковать, после чего не скачает новые k - m видео
    # TODO: добавить описание к краулеру

    def __init__(self, cache=None, ydl_loader=None, scraper=None, **kwargs):
        # TODO: переписать на StateMachine
        # TODO: выводить инфу о способе запуска
        self.__max_attempts = kwargs.pop("max_attempts", 5)
        self.__retry_sleep = kwargs.pop("retry_sleep", 3.)

        self.__cache = cache
        if self.__cache is None:
            self.__cache = DBSqlLiteCache()

        self.__video_downloader = ydl_loader
        if self.__video_downloader is None:
            logger = logging.getLogger()
            self.__video_downloader = YoutubeDlLoader(logger)

        self.__scraper = scraper
        if self.__scraper is None:
            self.__init_none_scraper()
        self.__logger = logging.getLogger()

        self.__crash_msg = "channel from cache isn't got (%s=%s). crawler interrupts execute..."

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
            ]
        )
        self.__scraper = scrapper

    @staticmethod
    def __create_video(video_id, channel_id, full_descr, short_descr):
        # TODO: заменить на алгоритмы valid и priority
        valid = True
        priority = 0

        if 'subtitles' in full_descr:
            del full_descr['subtitles']
        return {
            'video_id': video_id,
            'channel_id': channel_id,
            'full_description': json.dumps(full_descr),
            'short_description': json.dumps(short_descr),
            'valid': valid,
            'priority': priority
        }

    @staticmethod
    def __create_cur_channel(channel_id, full_descr, short_descr):
        # TODO: заменить на алгоритмы valid и priority
        priority = 0

        new_full_descr = {}
        if full_descr is not None:
            for k in full_descr:
                new_full_descr[k.value] = full_descr[k]

        return [{
            'channel_id': channel_id,
            'priority': priority,
            'full_description': json.dumps(new_full_descr) if new_full_descr is not None else None,
            'short_description': json.dumps(short_descr) if short_descr is not None else None,
        }]

    def __get_neighb_channels(self, descr):
        channels = []
        for channel in descr[Tab.Channels]:
            channels += self.__create_cur_channel(channel['channel_id'], None, channel)
        return channels

    def __sleep_and_logging(self, s, c, e):
        msg = "problem into scrapper: timeout error. sleeping...: %d sec. count retry: %d" % (s, c)
        logging.warning(msg)
        sleep(self.__retry_sleep)
        if c >= self.__max_attempts:
            raise e

    def __retry(self, fn, *args, **kwargs):
        count = 0
        while True:
            try:
                return fn(*args, **kwargs)
                # Different politics
            except ConnectionError as e:
                self.__sleep_and_logging(str(type(e)), count, e)
            except TimeoutError as e:
                self.__sleep_and_logging(str(type(e)), count, e)
            except Exception as e:
                self.__sleep_and_logging(str(type(e)), count, e)
            count += 1

    def __scrappy(self, channel_id):
        try:
            full_descr = self.__retry(self.__scraper.parse, channel_id)
            # Extract full_descr
            channel = self.__create_cur_channel(channel_id, full_descr, None)
            # Setting current channel into Cache. ChannelId
            self.__cache.set_channels(channel, scrapped=True, valid=True)
            return full_descr, True
        except Exception as e:
            self.__logger.warning(e, msg="problem with channel_id=%s" % channel_id)
            self.__cache.update_failed_channel(channel_id)
            return None, False

    def __download_video(self, video_id):
        try:
            full_video_descr = self.__retry(self.__video_downloader.load, video_id)
            return full_video_descr, True
        except Exception as e:
            self.__logger.warning(e, msg="problem with video_id=%s" % video_id)
            self.__cache.insert_failed_video(video_id)
        return None, False

    def __insert_video(self, video_id, channel_id, full_video_descr, descr):
        data = self.__create_video(video_id, channel_id, full_video_descr, descr)
        try:
            self.__cache.insert_video_descr(data)
        except Exception as e:
            logging.warning(e, msg="problem with video inserting into db video_id=%s" % video_id)
            return False
        return True

    def __download_videos(self, descrs):
        channel_id = descrs[Tab.HomePage][0]['owner_channel']['id']
        for descr in descrs[Tab.Videos]:
            video_id = descr['id']
            logging.info("starting downloading video_id=%s" % video_id)

            # Check in Cache video_id
            if self.__cache.check_exist_video(video_id):
                logging.info("such video already exist (video_id=%s)" % video_id)
                continue

            # Download video
            full_video_descr, is_downloaded = self.__download_video(video_id)
            if not is_downloaded:
                continue

            self.__insert_video(video_id, channel_id, full_video_descr, descr)

    def __set_neighb_channels(self, full_descr):
        neighb_channels = None
        try:
            # Setting neighbours channels into Cache. ChannelId
            neighb_channels = self.__get_neighb_channels(full_descr)
            self.__cache.set_channels(neighb_channels, scrapped=False, valid=True)
        except Exception as e:
            ch_ids_str = ','.join([ch['id'] for ch in neighb_channels])
            logging.error(e, msg=self.__crash_msg % ("channel_ids", ch_ids_str))

    def __update_channel_downloaded(self, channel_id):
        try:
            self.__cache.update_channel_downloaded(channel_id)
        except Exception as e:
            msg = "problem with update channel_id. " + self.__crash_msg % ("channel_id", channel_id)
            e = utils.CrawlerError(e=e, msg=msg)
            logging.warning(e)
            return False
        return True

    def process(self, channel_ids=None):
        if channel_ids is None:
            channel_ids = []
        if not isinstance(channel_ids, list):
            raise utils.CrawlerError("channel_ids is not list")
        self.__logger.debug("setting channel ids from arguments into Cache")

        self.__logger.debug("setting base channels into Cache (channel_ids=%s)" % ','.join(channel_ids))
        self.__cache.set_base_channels(channel_ids)
        self.__logger.debug("get best channel id")
        channel_id = self.__cache.get_best_channel_id()
        self.__logger.debug("best channel_id=%s" % channel_id)

        while channel_id is not None:
            self.__logger.info("channel_id=%s" % channel_id)
            full_descr, is_scrappy = self.__scrappy(channel_id)
            if not is_scrappy:
                self.__logger.debug("skipping... get best channel id")
                channel_id = self.__cache.get_best_channel_id()
                self.__logger.debug("best channel_id=%s" % channel_id)
                continue

            self.__set_neighb_channels(full_descr)

            # Downloading youtube for ChannelId
            # TODO: move to scrapper
            self.__download_videos(full_descr)

            # Channel was downloaded
            if not self.__update_channel_downloaded(channel_id):
                channel_id = self.__cache.get_best_channel_id()
                continue

            # Getting next channel from Cache
            channel_id = self.__cache.get_best_channel_id()
