from enum import Enum

from crawler.loaders import Tab
import langdetect
from collections import Counter


class ChannelStatus(Enum):
    STRONG_RU = 0
    WEAK_RU = 1
    FOREIGN = 2
    UNDEFINED = 3


class Filter:
    def __init__(self, len_descr=50, len_descr_parts=50):
        self._len_descr = len_descr
        self._len_descr_parts = len_descr_parts

    def apply(self, descr):
        try:
            description = langdetect.detect(descr[Tab.About][0]['description'])
        except:
            description = ''
        try:
            description_parts = langdetect.detect(' '.join(descr[Tab.HomePage][0]['videos']['general']['description_parts']))
        except:
            description_parts = ''
        try:
            videos_title = [langdetect.detect(video['title']) for video in descr[Tab.Videos]]
        except:
            videos_title = []
        if description == 'ru' and len(description) > self._len_descr or \
                description_parts == 'ru' and len(description_parts) > self._len_descr_parts:
            return ChannelStatus.STRONG_RU
        counter = Counter(videos_title)
        if len(counter) == 0:
            return ChannelStatus.UNDEFINED
        is_ru = max(counter, key=lambda el: counter[el]) == 'ru'
        if is_ru:
            return ChannelStatus.WEAK_RU
        return ChannelStatus.FOREIGN


