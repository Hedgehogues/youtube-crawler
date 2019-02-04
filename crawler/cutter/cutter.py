# I took this repo https://github.com/Zephirot93/subs-audio-splicer and modify it. I have got this code
import cmath
import math
import os

import srt
from pydub import AudioSegment

from crawler.cutter import validate_ext, srt_ext
from crawler.cutter import postprocessor as prc
from crawler.cutter.transcoder import FfmpegWavTranscoder


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
    def __init__(self, wav_transcoder=None, postprocessors=None, audio_fragment_gap=200):
        self.__out_format = 'wav'
        self.__audio_fragment_gap = audio_fragment_gap
        self.__wav_transcoder = wav_transcoder
        if self.__wav_transcoder is None:
            self.__wav_transcoder = FfmpegWavTranscoder()
        self.__postprocessors = postprocessors
        if self.__postprocessors is None:
            self.__postprocessors = [prc.AudioShorter(), prc.Deduplicator()]

    @staticmethod
    def __write_text(dialogue, file_path):
        fd = open(file_path, 'w')
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
        audio_segment.export('%s.%s' % (out_file, self.__out_format), format=self.__out_format)

    def __get_file_format(self, file_path, dialogues):
        return file_path + '-%' + '0%d.d' % self.__get_log_count_files(dialogues)

    def apply(self, path_audio, path_subs):
        path_audio = os.path.abspath(path_audio)
        path_subs = os.path.abspath(path_subs)

        subs_file_path = validate_ext(path_subs, srt_ext)

        dialogues = self.__get_dialogues(path_subs)

        self.__wav_transcoder.apply(path_audio)
        audio = AudioSegment.from_wav(path_audio)

        out_file_format = self.__get_file_format(subs_file_path, dialogues)
        for i, dialogue in enumerate(dialogues):
            out_file = out_file_format % i
            self.__write_text(dialogue, out_file)
            self.__write_audio(dialogue, audio, out_file)

        for p in self.__postprocessors:
            p.apply(out_file_format, dialogues)
