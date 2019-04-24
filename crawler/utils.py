class CrawlerError(Exception):
    """This is base exception of crawler. This exception is generated of Scrapper

    If you can catch this exception then all others exception is caught.
    This is base class of crawler exceptions
    """

    def __init__(self, msg="", e=None):
        self.msg = msg
        self.e = e

    def __add__(self, other):
        self.msg += other

    def __str__(self):
        return self.__recursion(self)

    def __recursion(self, e):
        if isinstance(e, CrawlerError):
            msg = self.__recursion(e.e)
            return "%s" % self.msg if len(msg) == 0 else "%s:%s -> %s" % (type(e), e.msg, msg)
        if e is None:
            return ""
        return "%s:%s" % (type(e), e.__str__())


class ReloadTokenError(CrawlerError):
    """ Token was not found or invalid

    This exception may be thrown when token for reload page not found or invalid
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class ParserError(CrawlerError):
    """
    Problem while parsing response
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class RequestError(CrawlerError):
    """Json with data not valid. This exception is generated of Scrapper

    This exception may be thrown when http-request is failed or
    body of response is not parsed
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class CacheError(CrawlerError):
    """There is problem with getting channels from Cache. This exception is generated of Cache
    """
    def __init__(self, video_id=None, channel_id=None, msg="", e=None):
        if video_id is not None and len(video_id) != 0:
            msg += ". video_id: %s" % video_id
        if channel_id is not None and len(channel_id) != 0:
            msg += ". channel_id: %s" % channel_id
        super().__init__("problem with cache. %s" % msg, e)


class ExtensionError(CrawlerError):
    """There is problem with extension of file. For instance, file has invalid extension
    """
    def __init__(self, ext, msg="", e=None):
        msg = 'Message: "%s".' % msg if len(msg) > 0 else ""
        super().__init__("extension problem. %s extension: %s" % (msg, ext), e)


def check_resp(resp):
    if resp.status_code != 200:
        raise RequestError("status code exception: %d. url: %s" % (resp.status_code, resp.url))
