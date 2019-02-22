from enum import Enum

from crawler.loaders import Tab
import langdetect
from collections import Counter


class ChannelLanguage(Enum):
    STRONG_RU = 0
    WEAK_RU = 1
    FOREIGN = 2
    UNDEFINED = 3


class Filter:
    def __init__(self, len_descr=50, len_descr_parts=50):
        self._len_descr = len_descr
        self._len_descr_parts = len_descr_parts

    @staticmethod
    def __is_title_videos_rus(counter):
        if len(counter) == 0:
            return ''
        return max(counter, key=lambda el: counter[el]) == 'ru'

    def apply(self, descr):
        # TODO: выпиливать ссылки
        # TODO: выпиливать цифры
        # TODO: выпиливать специальные символы
        # TODO: выпиливать хэш-теги и (@)
        # TODO: заменить \n и \t на пробелы
        try:
            description = descr[Tab.About][0]['description']
            lang_description = langdetect.detect(description)
        except:
            description = ''
            lang_description = ''
        if lang_description == 'ru' and len(description) >= self._len_descr:
            return ChannelLanguage.STRONG_RU

        try:
            description_parts = ' '.join(descr[Tab.HomePage][0]['videos']['general']['description_parts'])
            lang_description_parts = langdetect.detect(description_parts)
        except:
            lang_description_parts = ''
            description_parts = ''
        if lang_description_parts == 'ru' and len(description_parts) >= self._len_descr_parts:
            return ChannelLanguage.STRONG_RU

        try:
            lang_videos_titles = [langdetect.detect(video['title']) for video in descr[Tab.Videos]]
        except:
            lang_videos_titles = []

        counter = Counter(lang_videos_titles)
        is_ru = self.__is_title_videos_rus(counter)
        if is_ru:
            return ChannelLanguage.WEAK_RU

        if len(counter) == 0 and len(description_parts) < self._len_descr_parts and len(description) < self._len_descr:
            return ChannelLanguage.UNDEFINED

        return ChannelLanguage.FOREIGN
