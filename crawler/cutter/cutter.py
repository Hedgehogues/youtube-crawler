# I took this repo https://github.com/Zephirot93/subs-audio-splicer and modify it. I have got this code
import cmath
import math
import os

import pysrt
from pydub import AudioSegment

from crawler.cutter import validate_ext, srt_ext
from crawler.cutter.transcoder import FfmpegWavTranscoder


class Dialogue:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end


class AudioCutter:
    # TODO: в некоторых субтитрах есть более детальная разметка (указано какое слово когда должно появляться).
    # TODO: _1anwjN9tPA
    # TODO: добавить возможность перезаписывать и нет
    def __init__(self, wav_transcoder=None, threshold_len=1500):
        self.__out_format = 'wav'
        self.__threshold_len = threshold_len
        self.__wav_transcoder = wav_transcoder
        if self.__wav_transcoder is None:
            self.__wav_transcoder = FfmpegWavTranscoder()

    def __to_ms_srt(self, time):
        # Pysrt is stupid and doesn't return a deltatime object so we have to convert everything manually
        hours, minutes, seconds, milliseconds = time.hours, time.minutes, time.seconds, time.milliseconds
        return 36000000 * hours + 60000 * minutes + 1000 * seconds + milliseconds

    def __get_dialogues(self, path_subs):
        subs = pysrt.open(path_subs)
        return [Dialogue(sub.text, self.__to_ms_srt(sub.start), self.__to_ms_srt(sub.end)) for sub in subs]

    def __write_audio(self, dialogue, audio, out_file):
        start = dialogue.start
        end = dialogue.end
        audio_segment = audio[start:end]
        audio_segment.export('%s.%s' % (out_file, self.__out_format), format=self.__out_format)

    @staticmethod
    def __write_subs(dialogue, file_path):
        fd = open(file_path, 'w')
        fd.write(dialogue.text)
        fd.close()

    @staticmethod
    def __get_log_count_files(d):
        return math.ceil(cmath.log(len(d), 10).real)

    def __get_file_format(self, file_path, dialogues):
        return file_path + '-%' + '0%d.d' % self.__get_log_count_files(dialogues)

    def __postprocessing(self, out_file_format, dialogues):
        count_files = len(dialogues)
        log_count_files = self.__get_log_count_files(dialogues)
        for i, dialogue in enumerate(dialogues):
            out_file = out_file_format % i

    def apply(self, path_audio, path_subs):
        path_audio = os.path.abspath(path_audio)
        path_subs = os.path.abspath(path_subs)

        subs_file_path = validate_ext(path_subs, srt_ext)

        dialogues = self.__get_dialogues(path_subs)

        self.__wav_transcoder.apply(path_audio)
        audio = AudioSegment.from_wav(path_audio)

        out_file_format = self.__get_file_format(subs_file_path, dialogues)
        for i, dialogue in enumerate(dialogues):
            if dialogue.end - dialogue.start < self.__threshold_len:
                continue

            out_file = out_file_format % i
            self.__write_subs(dialogue, out_file)
            self.__write_audio(dialogue, audio, out_file)

        self.__postprocessing(out_file_format, dialogues)
