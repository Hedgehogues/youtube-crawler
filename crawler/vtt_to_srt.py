import os
from webvtt import WebVTT
import html
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime

from crawler import utils


class VTTtoSRT:
    __vtt = ".vtt"
    __srt = ".srt"

    @staticmethod
    def __write_srt(fd_srt, path):
        index = 0
        for caption in WebVTT().read(path):
            index += 1
            start = SubRipTime(0, 0, caption.start_in_seconds)
            end = SubRipTime(0, 0, caption.end_in_seconds)
            item = SubRipItem(index, start, end, html.unescape(caption.text))
            fd_srt.write("%s\n" % str(item))

    def transform(self, vvt_path):

        file_path, file_ext = os.path.splitext(vvt_path)
        path, file_name = os.path.split(file_path)

        if not file_ext.lower() == self.__vtt:
            utils.ExtensionError(self.__vtt, "Path to file: %s" % vvt_path)
            return

        with open(path + file_name + self.__srt, "w") as fd_srt:
            self.__write_srt(fd_srt, vvt_path)
