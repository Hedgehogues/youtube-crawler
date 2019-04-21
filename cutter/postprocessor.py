import os
import re

from Levenshtein import distance


class Deduplicator:
    def __init__(self, subs_ext, sorencen=0.08):
        self.__sorencen = sorencen
        self.__out_ext = subs_ext
        self.__re = re.compile('[^0-9a-zA-Zа-яА-Я]+')

    def __get_intersection(self, cur_sub, prev_sub):
        new_sub = []
        for a in cur_sub:
            is_same = False
            a_ = self.__re.sub('', a)
            for b in prev_sub:
                b_ = self.__re.sub('', b)
                sorencen = distance(a_, b_) / (len(a_) + len(b_)) if len(a_) > 0 or len(b_) > 0 else 0
                is_same |= sorencen < self.__sorencen
            if not is_same and len(a_) > 0:
                new_sub.append(a)
        return new_sub

    def apply(self, out_file_format, dialogues):
        prev_sub = []
        for i, dialogue in enumerate(dialogues):
            file = out_file_format % i
            if not os.path.exists(file):
                continue

            with open(file, 'r') as fd:
                cur_sub = fd.read().split('\n')
            new_sub = self.__get_intersection(cur_sub, prev_sub)
            prev_sub = cur_sub
            with open(file, 'w') as fd:
                fd.write('\n'.join(new_sub))


class AudioShorter:
    def __init__(self, audio_ext, subs_ext, audio_msec_len=700):
        self.__audio_msec_len = audio_msec_len
        self.__audio_ext = audio_ext
        self.__subs_ext = subs_ext

    def apply(self, out_file_format, dialogues):
        for i, dialogue in enumerate(dialogues):
            file = out_file_format % i
            if not os.path.exists(file + self.__audio_ext):
                raise FileNotFoundError("Not found file: %s" % file + self.__audio_ext)
            if not os.path.exists(file + self.__subs_ext):
                raise FileNotFoundError("Not found file: %s" % file + self.__subs_ext)

            total_mseconds = (dialogue.end - dialogue.start).total_seconds() * 1000
            if total_mseconds < self.__audio_msec_len:
                os.remove(file + self.__audio_ext)
                os.remove(file + self.__subs_ext)
