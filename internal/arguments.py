import argparse
from os import getenv

from crawler.cache import DB_MOD
from crawler.loaders import YDL_LOADER_FORMAT


def parse():

    args = argparse.ArgumentParser()

    args.add_argument(
        '--base-channels',
        default=getenv('BASE_CHANNELS', 'data/base_channels.tsv'),
        type=str,
        help='path to file with base channels for start crawling (one url to channel per line)',
    )
    args.add_argument(
        '--max-videos-page',
        default=getenv('MAX_VIDEOS_PAGE', None),
        type=int,
        help='max count pages for downloading from video page of channel',
    )
    args.add_argument(
        '--max-channels-page',
        default=getenv('MAX_CHANNELS_PAGE', None),
        type=int,
        help='max count pages for downloading from channel page about another channels',
    )
    args.add_argument(
        '--output-format',
        default=getenv('OUTPUT_FORMAT', YDL_LOADER_FORMAT.MP3),
        choices=[YDL_LOADER_FORMAT.MP3, YDL_LOADER_FORMAT.WAV],
        type=YDL_LOADER_FORMAT,
        help='output video format',
    )
    args.add_argument(
        '--sqlite-path',
        default=getenv('SQLITE_PATH', 'data/db.sqlite'),
        help='path to sqlite database file',
        type=str,
    )
    args.add_argument(
        '--db-mod',
        default=getenv('DB_MOD', DB_MOD.HARD),
        choices=[DB_MOD.NEW, DB_MOD.HARD, DB_MOD.OLD],
        type=DB_MOD,
        help='path to sqlite database file',
    )
    args.add_argument(
        '--max-attempts',
        default=getenv('MAX_ATTEMPTS', 5),
        type=int,
        help='max attempts retry for requests',
    )
    args.add_argument(
        '--log-level',
        default=getenv('LOG_LEVEL', 'INFO'),
        choices=['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL'],
        type=str,
        help='level of logging',
    )
    args.add_argument(
        '--logging-filename',
        default=None,
        type=str,
        help='path to file for logging',
    )

    return vars(args.parse_args())
