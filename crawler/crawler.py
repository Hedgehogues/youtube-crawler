class YoutubeCrawler:
    def __init__(self, parser=None, channel_validator=default_channel_validator):
        self.__parser = ChannelYoutubeDLParser(priorities_channels)
        self.__set_validator = channel_validator
        if parser is not None:
            self.__parser = parser

        self.used_channels_ = {}
        self.count_ = 0

    def __dfs(self, channel_id):
        self.count_ += 1
        print(channel_id, self.count_)
        channel = self.__parser.get_channel_info(channel_id)
        channel.status = self.__set_validator(channel)
        if channel.status != ChannelStatus.RU:
            return
        self.used_channels_[channel_id] = channel
        for item in channel.channels:
            if item['channel_id'] not in self.used_channels_:
                self.__dfs(item['channel_id'])
        return

    def process(self, channel_ids):
        self.used_channels_ = {}
        self.count_ = 0
        for v in channel_ids:
            if v not in self.used_channels_:
                self.__dfs(v)
        return
