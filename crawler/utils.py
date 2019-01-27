class JsonExtractionError(Exception):
    """Json with data not found in a page

    This exception may be thrown when one page of channel not contains
    json with data or this json move to other place of page.
    """
    def __init__(self, msg, e=None):
        self.e = e
        self.msg = msg


class JsonSerializableError(Exception):
    """Json with data not found in a page

    This exception may be thrown when one page of channel consist not valid json
    """
    def __init__(self, msg, e=None):
        self.e = e
        self.msg = msg


class RequestError(Exception):
    """Json with data not valid

    This exception may be thrown when http-request is failed or
    body of response is not parsed
    """
    def __init__(self, msg, e=None):
        self.e = e
        self.msg = msg


def check_resp(resp):
    if resp.status_code != 200:
        raise RequestError("Status code exception: %d. Url: %s" % (resp.status_code, resp.url))
