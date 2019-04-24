import logging
import os

from crawler import parsers
from crawler.cache import DBSqlLiteCache, DB_MOD
from crawler.crawler import YoutubeCrawler
from crawler.loaders import YoutubeDlLoader, YDL_LOADER_FORMAT, Loader, Reloader
from crawler.scrapper import Scrapper


def sep_url(x):
    return x.replace('\n', '').split('/')[-1]


def build_crawler(**kwargs):
    """

    :param kwargs:
    :return:
    """

    logging_filename = kwargs.pop('logging_filename', None)
    if logging_filename is not None and os.path.exists(logging_filename):
        os.remove(logging_filename)
    f = '{"Time": "%(asctime)-15s", "Level": "%(levelname)s", "AppName": "[%(name)s]", "Message": "%(message)s"}'
    logging.basicConfig(format=f, filename=logging_filename)

    logger = logging.getLogger()
    logger.name = kwargs.pop('app_name', 'youtube-crawler')
    logger.setLevel(kwargs.pop('log_level', logging.INFO))
    scrapper = Scrapper(
        loader=Loader(base_url=kwargs.pop('loader_base_url', 'https://www.youtube.com/channel/')),
        reloader=Reloader(base_url=kwargs.pop('reloader_base_url', 'https://www.youtube.com/browse_ajax/')),
        parsers=[
            parsers.HomePageParser(jq_path=kwargs.pop('homepage_parser_jq_path', 'crawler/jq/home_page.jq')),
            parsers.VideosParser(
                max_page=kwargs.pop('max_videos_page', None),
                jq_load_path=kwargs.pop('video_jq_load_path', 'crawler/jq/videos.jq'),
                jq_reload_path=kwargs.pop('video_jq_reload_path', 'crawler/jq/videos_reload.jq'),
            ),
            parsers.ChannelsParser(
                max_page=kwargs.pop('max_channels_page', None),
                jq_load_path=kwargs.pop('channels_jq_load_path', 'crawler/jq/channels.jq'),
                jq_reload_path=kwargs.pop('channels_jq_reload_path', 'crawler/jq/channels_reload.jq'),
            ),
            parsers.AboutParser(jq_path=kwargs.pop('homepage_jq_path', 'crawler/jq/about.jq')),
        ],
    )

    crwl = YoutubeCrawler(
        ydl_loader=YoutubeDlLoader(
            ydl_params=kwargs.pop("ydl_params", None),
            f=kwargs.pop("ydl_format", YDL_LOADER_FORMAT.MP3),
            base_url=kwargs.pop("ydl_url", 'https://www.youtube.com/watch'),
            logger=logger,
        ),
        cache=DBSqlLiteCache(
            path=kwargs.pop("sqlite_path", 'data/db.sqlite'),
            db_mod=kwargs.pop("db_mod", DB_MOD.NEW),
        ),
        scraper=scrapper,
        max_attempts=kwargs.pop("max_attempts", 5),
        retry_sleep=kwargs.pop("retry_sleep", 10.)
    )
    return crwl
