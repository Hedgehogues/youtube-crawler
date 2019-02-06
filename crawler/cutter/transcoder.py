import subprocess
import os

from webvtt import WebVTT
import html
from pysrt.srtitem import SubRipItem, SubRipTime
from crawler.cutter import validate_ext


class FfmpegWavTranscoder:
    # TODO: добавить возможность перезаписывать и нет
    def __init__(self):
        self.__ext = '.wav'

    def apply(self, audio_name):
        cmd = ['ffmpeg', '-loglevel', 'panic', '-i', audio_name, audio_name +'X' + self.__ext]
        subprocess.call(cmd)
        cmd = ['mv', audio_name +'X' + self.__ext, audio_name]
        subprocess.call(cmd)


# Требования:
# * Преобразование vtt в srt
# * Возможность очистки vtt
# * Задавать суффикс для всех srt-файлов
class VttToSrtTranscoder:
    def __init__(self, suffix='', vtt_reader=None):
        self.__suffix = suffix
        self.__out_ext = '.srt'
        self.__in_ext = '.vtt'

        self.__vtt_reader = vtt_reader
        if self.__vtt_reader is None:
            self.__vtt_reader = WebVTT()

    def __write_subs(self, out_fd, in_path):
        for index, caption in enumerate(self.__vtt_reader.read(in_path)):
            start = SubRipTime(0, 0, caption.start_in_seconds)
            end = SubRipTime(0, 0, caption.end_in_seconds)
            item = SubRipItem(index+1, start, end, html.unescape(caption.text))
            out_fd.write("%s\n" % str(item))

    def __create_out_filename(self, in_file_path):
        out_file_path = "%s.%s" % (in_file_path, self.__out_ext)
        if len(self.__suffix) > 0:
            out_file_path = "%s-%s.%s" % (in_file_path, self.__suffix, self.__out_ext)

        return out_file_path

    def apply(self, in_vtt_path, clear=True):
        # *_file_path -- path to file without extension (e.t. *, for example 'subs')
        # *_vtt_path -- path to file with vtt-extension (e.t. *.vtt, for example 'subs.vtt')

        in_vtt_path = os.path.abspath(in_vtt_path)
        in_file_path = validate_ext(in_vtt_path,  self.__in_ext)

        out_file_path = self.__create_out_filename(in_file_path)

        with open(out_file_path, "w") as out_fd:
            self.__write_subs(out_fd, in_vtt_path)

        if clear:
            os.remove(in_vtt_path)

        return out_file_path
