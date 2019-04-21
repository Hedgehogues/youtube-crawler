import os
from webvtt import WebVTT
import html
from pysrt import srtitem
from pysrt import srttime

from crawler import utils


class VTTtoSRT:
    __vtt = ".vtt"
    __srt = ".srt"

    def __init__(self, prefix=''):
        self.prefix = prefix

    @staticmethod
    def __write_srt(fd_srt, path):
        index = 0
        for caption in WebVTT().read(path):
            index += 1
            start = srttime.SubRipTime(0, 0, caption.start_in_seconds)
            end = srttime.SubRipTime(0, 0, caption.end_in_seconds)
            item = srtitem.SubRipItem(index, start, end, html.unescape(caption.text))
            fd_srt.write("%s\n" % str(item))

    def transform(self, vtt_path):
        file_path, file_ext = os.path.splitext(vtt_path)
        path, file_name = os.path.split(file_path)

        if not file_ext.lower() == self.__vtt:
            raise utils.ExtensionError(self.__vtt, "Path to file: %s" % vtt_path)

        with open('%s/%s%s%s' % (path, self.prefix, file_name, self.__srt), "w") as fd_srt:
            self.__write_srt(fd_srt, vtt_path)
