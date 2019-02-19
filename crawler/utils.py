class CrawlerExceptions(Exception):
    """This is base exception of crawler. This exception is generated of Scrapper

    If you can catch this exception then all others exception is caught.
    This is base class of crawler exceptions
    """

    def __init__(self, msg="", e=None):
        self.msg = msg
        self.e = e
        if e is CrawlerExceptions:
            self.e = e

    def __add__(self, other):
        self.msg += other

    def __recursion(self, e):
        e_ = []
        if e is CrawlerExceptions:
            e_ = [self] + self.__recursion(self.e)
        return e_

    def get_stack_errors(self):
        e = []
        if self.e is CrawlerExceptions:
            e = [self] + self.__recursion(self.e)
        return e


class ReloadTokenError(CrawlerExceptions):
    """ Token was not found or invalid

    This exception may be thrown when token for reload page not found or invalid
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class JsonExtractionError(CrawlerExceptions):
    """Json with data not found in a page. This exception is generated of Scrapper

    This exception may be thrown when one page of channel not contains
    json with data or this json move to other place of page.
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class JsonSerializableError(CrawlerExceptions):
    """Json with data not found in a page. This exception is generated of Scrapper

    This exception may be thrown when one page of channel consist not valid json
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class RequestError(CrawlerExceptions):
    """Json with data not valid. This exception is generated of Scrapper

    This exception may be thrown when http-request is failed or
    body of response is not parsed
    """
    def __init__(self, msg, e=None):
        super().__init__(msg, e)


class ScrapperError(CrawlerExceptions):
    """Scrapper is crashed. This exception is generated of Crawler

    This exception denote crash of Scrapper. This exception is generated of Crawler
    after raised exception of Scrapper. Returned answer from Scrapper is invalid.
    """
    def __init__(self, channel_id, e=None):
        super().__init__("Scrapper was failed. ChannelId: %s" % channel_id, e)


class CacheGetChannelsError(CrawlerExceptions):
    """There is problem with getting channels from Cache. This exception is generated of Cache
    """
    def __init__(self, msg="", e=None):
        super().__init__("Problem with getting channels from Cache. %s" % msg, e)


class ExtensionError(CrawlerExceptions):
    """There is problem with extension of file. For instance, file has invalid extension
    """
    def __init__(self, ext, msg="", e=None):
        msg = 'Message: "%s".' % msg if len(msg) > 0 else ""
        super().__init__("Extension problem. %s Extension: %s" % (msg, ext), e)


def check_resp(resp):
    if resp.status_code != 200:
        raise RequestError("Status code exception: %d. Url: %s" % (resp.status_code, resp.url))
