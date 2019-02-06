import os

from webvtt import WebVTT
import html
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime
from crawler.cutter import validate_ext


def __write_srt(fd_srt, path):
    index = 0
    for caption in WebVTT().read(path):
        index += 1
        start = SubRipTime(0, 0, caption.start_in_seconds)
        end = SubRipTime(0, 0, caption.end_in_seconds)
        item = SubRipItem(index, start, end, html.unescape(caption.text))
        fd_srt.write("%s\n" % str(item))


def vtt_to_srt(vtt_path, replace=True):
    vtt_path = os.path.abspath(vtt_path)
    file_path = validate_ext(vtt_path, vtt_ext)

    with open("%s.%s" % (file_path, srt_ext[1:]), "w") as fd_srt:
        __write_srt(fd_srt, vtt_path)

    if replace:
        os.remove(vtt_path)

    return file_path + srt_ext