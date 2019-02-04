# I took this repo https://github.com/Zephirot93/subs-audio-splicer and modify it. I have got this code
import cmath
import math
import os

import datetime
import re

import srt
from pydub import AudioSegment
from Levenshtein import distance

from crawler.cutter import validate_ext, srt_ext
from crawler.cutter.transcoder import FfmpegWavTranscoder


class Dialogue:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end


class AudioCutter:
    # TODO: в некоторых субтитрах есть более детальная разметка (указано какое слово когда должно появляться)

    # TODO: добавить возможность перезаписывать и нет
    def __init__(self, wav_transcoder=None, postprocessors=None, thrsh_dupl_len=0.1, thrsh_audio_len=0.7):
        self.__out_format = 'wav'
        self.__thrsh_audio_len = thrsh_audio_len
        self.__thrsh_dupl_len = thrsh_dupl_len
        self.__wav_transcoder = wav_transcoder
        if self.__wav_transcoder is None:
            self.__wav_transcoder = FfmpegWavTranscoder()
        self.__postprocessors = postprocessors
        if self.__postprocessors is None:
            self.__postprocessors = []

    def __get_dialogues(self, path_subs):
        with open(path_subs) as fd:
            dialogues = [Dialogue(sub.content, sub.start, sub.end) for sub in srt.parse(fd.read())]
        return dialogues

    def __write_audio(self, dialogue, audio, out_file):
        start = dialogue.start.total_seconds() * 1000
        end = dialogue.end.total_seconds() * 1000
        audio_segment = audio[start:end]
        audio_segment.export('%s.%s' % (out_file, self.__out_format), format=self.__out_format)

    @staticmethod
    def __write_text(dialogue, file_path):
        fd = open(file_path, 'w')
        fd.write(dialogue.text)
        fd.close()

    @staticmethod
    def __get_log_count_files(d):
        return math.ceil(cmath.log(len(d), 10).real)

    def __get_file_format(self, file_path, dialogues):
        return file_path + '-%' + '0%d.d' % self.__get_log_count_files(dialogues)

    def __postprocessing(self, out_file_format, dialogues):
        prev_sub = []
        for i, dialogue in enumerate(dialogues):
            file = out_file_format % i
            total_seconds = (dialogue.end - dialogue.start).total_seconds()
            if total_seconds < self.__thrsh_audio_len:
                os.remove('%s.%s' % (file, self.__out_format))
                os.remove(file)
                continue
            with open(file, 'r') as fd:
                cur_sub = fd.read().split('\n')
            new_sub = []
            for a in cur_sub:
                is_same = False
                a_ = re.sub('[^0-9a-zA-Zа-яА-Я]+', '', a)
                for b in prev_sub:
                    b_ = re.sub('[^0-9a-zA-Zа-яА-Я]+', '', b)
                    sorencen = distance(a_, b_) / (len(a_) + len(b_)) if len(a_) > 0 or len(b_) > 0 else 0
                    is_same |= sorencen < self.__thrsh_dupl_len
                if not is_same and len(a_) > 0:
                    new_sub.append(a)
            prev_sub = cur_sub
            with open(file, 'w') as fd:
                fd.write('\n'.join(new_sub))

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
