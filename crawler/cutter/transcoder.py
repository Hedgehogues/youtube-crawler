import subprocess
import os
import uuid

from webvtt import WebVTT
import html
from pysrt.srtitem import SubRipItem, SubRipTime
from crawler.cutter import validate_ext


class FfmpegWavTranscoder:
    # TODO: добавить возможность перезаписывать и нет
    def __init__(self, clear=True):
        self.__ext = '.wav'
        self.__clear = clear

    def get_ext(self):
        return self.__ext

    def apply(self, audio_name):
        out_audio_name = '%s-%s-%s' % (audio_name, str(uuid.uuid4()), self.__ext)
        cmd = ['ffmpeg', '-loglevel', 'panic', '-i', audio_name, out_audio_name]
        subprocess.call(cmd)
        cmd = ['mv', out_audio_name, audio_name]
        subprocess.call(cmd)
        return audio_name


# Требования:
# * Преобразование vtt в srt
# * Возможность очистки vtt
# * Задавать суффикс для всех srt-файлов
class VttToSrtTranscoder:
    def __init__(self, suffix='', clear=True, vtt_reader=None):
        self.__suffix = suffix
        self.__clear = clear

        self.__out_ext = '.srt'
        self.__in_ext = '.vtt'

        self.__vtt_reader = vtt_reader
        if self.__vtt_reader is None:
            self.__vtt_reader = WebVTT()

    def get_in_ext(self):
        return self.__in_ext

    def get_out_ext(self):
        return self.__out_ext

    def __write_subs(self, out_fd, in_path):
        for index, caption in enumerate(self.__vtt_reader.read(in_path)):
            start = SubRipTime(0, 0, caption.start_in_seconds)
            end = SubRipTime(0, 0, caption.end_in_seconds)
            item = SubRipItem(index+1, start, end, html.unescape(caption.text))
            out_fd.write("%s\n" % str(item))

    def __create_out_filename(self, in_file_path):
        out_file_path = os.path.splitext(in_file_path)[0]
        if len(self.__suffix) > 0:
            out_file_path = "%s-%s" % (out_file_path, self.__suffix)

        return out_file_path + self.__out_ext

    def apply(self, in_vtt_path):

        in_vtt_path = os.path.abspath(in_vtt_path)
        validate_ext(in_vtt_path,  self.__in_ext)

        out_file_path = self.__create_out_filename(in_vtt_path)

        with open(out_file_path, "w") as out_fd:
            self.__write_subs(out_fd, in_vtt_path)

        if self.__clear:
            os.remove(in_vtt_path)

        return out_file_path
