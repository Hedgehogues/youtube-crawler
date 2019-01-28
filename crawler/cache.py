class CacheSqlLite:
    def __init__(self, cache_path='~/youtube-crawler', file_name='description.sql'):
        pass

    def set_channel_processed(self, channel_id):
        pass

    def set_channel_error(self, channel_id, err):
        pass

    def set_current_channel(self, channel_id):
        pass

    def get_current_channel(self, channel_id):
        pass

    def set_video_processed(self, channel_id):
        pass

    def set_video_error(self, channel_id, err):
        pass

    def set_channel(self, channel_id, channel_descr):
        pass

    def get_channel(self, channel_id):
        pass

    def get_video_info(self, video_id):
        pass

    def set_video_info(self, video_id, channel_descr):
        pass
