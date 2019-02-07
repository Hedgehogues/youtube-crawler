# I took this repo https://github.com/Zephirot93/subs-audio-splicer and modify it. I have got this code
import cmath
import math
import os

import srt
from pydub import AudioSegment

from crawler.cutter import validate_ext
from crawler.cutter import postprocessor as prc
from crawler.cutter.transcoder import FfmpegWavTranscoder, VttToSrtTranscoder


class Dialogue:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end


# Требования:
# * Преобразовывать аудио и субтитры в набор дорожек согласно субтитрам.  Результат требуется положить в
#   директорию, в этой же папке (по дефолту) или указанную в конструкторе, при инициализации.
# * Требуется поддерживать произвольный формат субтитров
# * Требуется поддерживать произвольный формат аудио
# * Добавить возможность удаления исходных субтитров и видео

class AudioCutter:
    # TODO: в некоторых субтитрах есть более детальная разметка (указано какое слово когда должно появляться)

    # TODO: добавить возможность перезаписывать и нет
    def __init__(self, subs_transcoder=None, audio_transcoder=None, postprocessors=None, audio_fragment_gap=200):
        self.__audio_transcoder = audio_transcoder
        if self.__audio_transcoder is None:
            self.__audio_transcoder = FfmpegWavTranscoder(clear=False)

        self.__subs_transcoder = subs_transcoder
        if self.__subs_transcoder is None:
            self.__subs_transcoder = VttToSrtTranscoder(clear=False)

        self.__sub_in_ext = self.__subs_transcoder.get_in_ext()
        self.__sub_out_ext = self.__subs_transcoder.get_out_ext()
        self.__audio_ext = self.__audio_transcoder.get_ext()
        self.__audio_fragment_gap = audio_fragment_gap

        self.__postprocessors = postprocessors
        if self.__postprocessors is None:
            self.__postprocessors = [
                prc.AudioShorter(
                    audio_msec_len=700 + 2*self.__audio_fragment_gap,
                    audio_ext=self.__audio_ext,
                    subs_ext=self.__sub_out_ext
                ),
                prc.Deduplicator(subs_ext=self.__sub_out_ext)
            ]

    def __write_text(self, dialogue, file_path):
        fd = open(file_path + self.__sub_out_ext, 'w')
        fd.write(dialogue.text)
        fd.close()

    @staticmethod
    def __get_log_count_files(d):
        return math.ceil(cmath.log(len(d), 10).real)

    @staticmethod
    def __get_dialogues(path_subs):
        with open(path_subs) as fd:
            dialogues = [Dialogue(sub.content, sub.start, sub.end) for sub in srt.parse(fd.read())]
        return dialogues

    def __write_audio(self, dialogue, audio, out_file):
        start = dialogue.start.total_seconds() * 1000 - self.__audio_fragment_gap
        end = dialogue.end.total_seconds() * 1000 + self.__audio_fragment_gap
        audio_segment = audio[start:end]
        audio_segment.export(out_file + self.__audio_ext, format=self.__audio_ext[1:])

    def __get_file_format(self, dialogues):
        return '%' + '0%d.d' % self.__get_log_count_files(dialogues)

    @staticmethod
    def __create_dirs(path_cutter):
        if not os.path.exists(path_cutter):
            os.makedirs(path_cutter)

    @staticmethod
    def __get_abs_out_dir(path_cutter):
        abs_path_cutter = '%s/' % os.path.abspath(path_cutter)
        if len(abs_path_cutter) == 0:
            raise FileNotFoundError("Path not found: %s", abs_path_cutter)
        return abs_path_cutter

    def __create_dialogues(self, path_subs):
        path_subs = os.path.abspath(path_subs)
        validate_ext(path_subs, self.__sub_in_ext)
        new_subs_path = self.__subs_transcoder.apply(path_subs)
        return self.__get_dialogues(new_subs_path)

    def __create_audio(self, path_audio):
        path_audio = os.path.abspath(path_audio)
        validate_ext(path_audio, self.__audio_ext)
        new_audio_path = self.__audio_transcoder.apply(path_audio)
        return AudioSegment.from_wav(new_audio_path)

    def apply(self, path_audio, path_subs, path_cutter):
        dialogues = self.__create_dialogues(path_subs)
        audio = self.__create_audio(path_audio)

        self.__create_dirs(path_cutter)

        out_file_format = self.__get_abs_out_dir(path_cutter) + self.__get_file_format(dialogues)
        for i, dialogue in enumerate(dialogues):
            out_file = out_file_format % i
            self.__write_text(dialogue, out_file)
            self.__write_audio(dialogue, audio, out_file)

        for p in self.__postprocessors:
            p.apply(out_file_format, dialogues)
