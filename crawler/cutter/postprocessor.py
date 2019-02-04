import os
import re

from Levenshtein import distance


class Deduplicator:
    def __init__(self, sorencen=0.08, out_format='wav'):
        self.__sorencen = sorencen
        self.__out_format = out_format
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
    def __init__(self, audio_len=0.7, out_format='wav'):
        self.__audio_len = audio_len
        self.__out_format = out_format

    def apply(self, out_file_format, dialogues):
        for i, dialogue in enumerate(dialogues):
            file = out_file_format % i
            if not os.path.exists(file):
                continue

            total_seconds = (dialogue.end - dialogue.start).total_seconds()
            if total_seconds < self.__audio_len:
                os.remove('%s.%s' % (file, self.__out_format))
                os.remove(file)
