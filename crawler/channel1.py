import re
from collections import namedtuple
from enum import Enum

from crawler.base import BaseYoutubeDL


class ChannelStatus(Enum):
    RU = 0
    FOREIGN = 1
    UNDEFINED = 2
    NONE = 3


def priorities_channels(channels):
    answ = sorted(channels, key=lambda el: (el['count_subscribers'], el['count_videos']))[::-1]
    return answ


class Channel:
    def __init__(self, view_count_homepage_video, short_descr, full_descr, count_subscribers, joined_date,
                 view_counts_channel, channels, status):
        self.view_count_homepage_video = view_count_homepage_video
        self.short_descr = short_descr
        self.full_descr = full_descr
        self.count_subscribers = count_subscribers
        self.joined_date = joined_date
        self.view_counts_channel = view_counts_channel
        self.channels = channels
        self.status = status


class ChannelYoutubeDLParser(BaseYoutubeDL):
    def __init__(self, priorities_fn=None, params=None):
        super().__init__(params)
        self.__priorities_channels_fn = lambda x: x
        if priorities_fn is not None:
            self.__priorities_channels_fn = priorities_fn
        self._prefixes = {
            'view_count': '"viewCount":"',
            'short_descr': '"shortDescription":"',
            'count_subscribers': '"subscriberCountText":{"simpleText":"',

            'full_descr': '{"channelAboutFullMetadataRenderer":{"description":{"simpleText":"',
            'joined_date': '"joinedDateText":{"simpleText":"',
            'view_counts_channel': '"viewCountText":{"runs":\\[{"text":"',

            'ctoken': '"nextContinuationData":{"continuation":"',

            'channel_id': 'channelId":"',
            'channel_count_videos': '"videoCountText":{"simpleText":"',
            'channel_count_subscribers': '"subscriberCountText":{"simpleText":"',
        }
        self._suffixes = {
            'view_count': '"',
            'short_descr': '","isCrawlable"',
            'count_subscribers': ' subs',

            'full_descr': '"},"primaryLinks":',
            'joined_date': '"},"canonicalChannelUrl"',
            'view_counts_channel': '","bold":true},{"text":" view',

            'ctoken': '","clickTrackingParams":',

            'channel_id': '","title":',
            'channel_count_videos': ' video',
            'channel_count_subscribers': ' subscriber',
        }
        self._target = {
            'view_count': self._numerics,
            'short_descr': self._any_symbols,
            'count_subscribers': self._numerics,

            'full_descr': self._any_symbols,
            'joined_date': self._any_symbols,
            'view_counts_channel': self._any_symbols,

            'ctoken': self._any_symbols,

            'channel_id': self._any_symbols,
            "channel_count_videos": self._any_symbols,
            "channel_count_subscribers": self._any_symbols,
        }

    def __get_home_page_info(self, text):
        view_count = self._extract_regexp_substr(text, 'view_count')
        if view_count is not None:
            view_count = int(view_count)
        short_descr = self._extract_regexp_substr(text, 'short_descr')
        self._none_exception(short_descr)
        count_subscribers = self._extract_regexp_substr(text, 'count_subscribers')
        if count_subscribers is not None:
            count_subscribers = int(count_subscribers)

        return view_count, short_descr, count_subscribers

    def __get_about_page_info(self, text):
        full_descr = self._extract_regexp_substr(text, 'full_descr')
        self._none_exception(full_descr)
        joined_date = self._extract_regexp_substr(text, 'joined_date')
        self._none_exception(joined_date)
        view_counts_channel = int(self._extract_regexp_substr(text, 'view_counts_channel').replace(',', ''))
        if view_counts_channel is not None:
            view_counts_channel = int(view_counts_channel)

        return full_descr, joined_date, view_counts_channel

    @staticmethod
    def __extract_shelfs(text):
        return re.findall('view=\d+', text)

    def __extract_additional_descr(self, text, s, name):
        prefix = self._prefixes[name]
        suffix = self._suffixes[name]
        target = self._target[name]
        substr_channel = text[text.find(s):]
        descr = re.findall(prefix + target + suffix, substr_channel)
        if len(descr) == 0:
            return 0
        return int(descr[0][len(prefix):-len(suffix)].replace(' ', '').replace(',', ''))

    def __extract_channels(self, text):
        prefix = self._prefixes['channel_id']
        suffix = self._suffixes['channel_id']
        target = self._target['channel_id']
        candidate_strs = re.findall(prefix + target + suffix, text)
        channels = []
        for s in candidate_strs:
            channels.append(
                {
                    'channel_id': s[len(prefix):-len(suffix)],
                    'count_videos': self.__extract_additional_descr(text, s[len(prefix):-len(suffix)], 'channel_count_videos'),
                    'count_subscribers': self.__extract_additional_descr(text, s[len(prefix):-len(suffix)], 'channel_count_subscribers'),
                })
        return channels

    def __extract_all_channel_id(self, text):
        channels = self.__extract_channels(text)
        ctoken = self._extract_regexp_substr(text, 'ctoken')
        headers = {
            'x-youtube-client-name': '1',
            'x-youtube-client-version': '2.20190117',
            'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'VISITOR_INFO1_LIVE=t3zCqZs-6NA; _ga=GA1.2.1862333059.1547989835; _gid=GA1.2.366404146.1547989835; PREF=f5=30&al=en&cvdm=list&f1=50000000; YSC=KCsXvfHQG-I; GPS=1',
        }
        url = 'https://www.youtube.com/browse_ajax'
        while ctoken is not None:
            params = {'ctoken': ctoken}
            text_for_channel_id = self._get_resp_text(url, params=params, headers=headers)
            channels += self.__extract_channels(text_for_channel_id)
            ctoken = self._extract_regexp_substr(text_for_channel_id, 'ctoken')

        return channels

    def __get_channels(self, url):
        text = self._get_resp_text(url+'/channels')
        shelfs = list(set(self.__extract_shelfs(text)))
        channels = []
        for shelf in shelfs:
            channels += self.__extract_all_channel_id(text)
            text = self._get_resp_text(url + '/channels?flow=list&' + shelf)
        channels += self.__extract_all_channel_id(text)

        base_channel_id = url[url.rfind('/')+1:]
        channels = {channel['channel_id']: channel for channel in channels if channel['channel_id'] != base_channel_id}
        return list(channel[1] for channel in channels.items())

    def get_channel_info(self, channel_id):
        url = 'https://www.youtube.com/channel/' + channel_id

        text = self._get_resp_text(url)
        view_count_homepage_video, short_descr, count_subscribers = self.__get_home_page_info(text)

        text = self._get_resp_text(url + '/about')
        full_descr, joined_date, view_counts_channel = self.__get_about_page_info(text)

        channels = self.__get_channels(url)

        return Channel(
            view_count_homepage_video=view_count_homepage_video,
            short_descr=short_descr,
            full_descr=full_descr,
            count_subscribers=count_subscribers,
            joined_date=joined_date,
            view_counts_channel=view_counts_channel,
            channels=self.__priorities_channels_fn(channels),
            status=ChannelStatus.NONE,
        )
