import subprocess
import os

from webvtt import WebVTT
import html
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime
from crawler.cutter import validate_ext, srt_ext, vtt_ext


class FfmpegWavTranscoder:
    # TODO: добавить возможность перезаписывать и нет
    def __init__(self):
        self.format = 'wav'

    def apply(self, audio_name):
        cmd = ['ffmpeg', '-loglevel', 'panic', '-i', audio_name, audio_name+'X.'+self.format]
        subprocess.call(cmd)
        cmd = ['mv', audio_name+'X.'+self.format, audio_name]
        subprocess.call(cmd)


# Требования:
# * Преобразование vtt в srt
# * Возможность очистки vtt
# * Задавать кастомное имя и путь до srt-файла
# * Задавать суффикс для всех srt-файлов
class VttToSrtTranscoder:
    def __init__(self, suffix=''):
        self.__suffix = suffix
        self.__ext = 'srt'
        self.__vtt_reader = WebVTT()

    def __write_subs(self, out_fd, in_path):
        for index, caption in enumerate(self.__vtt_reader.read(in_path)):
            start = SubRipTime(0, 0, caption.start_in_seconds)
            end = SubRipTime(0, 0, caption.end_in_seconds)
            item = SubRipItem(index+1, start, end, html.unescape(caption.text))
            out_fd.write("%s\n" % str(item))

    def __create_out_filename(self, in_file_path, out_vtt_path):
        out_vtt_path = os.path.abspath(out_vtt_path)

        out_file_path = "%s.%s" % (in_file_path, self.__ext)
        if len(self.__suffix) > 0:
            out_file_path = "%s-%s.%s" % (in_file_path, self.__suffix, self.__ext)

        if len(out_vtt_path) > 0:
            out_path = validate_ext(out_vtt_path, vtt_ext)
            out_file_path = "%s.%s" % (self.__ext, out_path)

        return out_file_path

    def apply(self, in_vtt_path, out_vtt_path='', clear=True):
        # *_file_path -- path to file without extension (e.t. *, for example 'subs')
        # *_vtt_path -- path to file with vtt-extension (e.t. *.vtt, for example 'subs.vtt')

        in_vtt_path = os.path.abspath(in_vtt_path)
        in_file_path = validate_ext(in_vtt_path, vtt_ext)

        out_file_path = self.__create_out_filename(in_file_path, out_vtt_path)

        with open(out_file_path, "w") as out_fd:
            self.__write_subs(out_fd, in_vtt_path)

        if clear:
            os.remove(in_vtt_path)

        return out_file_path
