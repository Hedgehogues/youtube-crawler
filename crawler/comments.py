from crawler.base import BaseYoutubeDL


class CommentsYoutubeDl(BaseYoutubeDL):
    '''
    Не используются сложные регулярные выражения, поскольку требуется обеспечить быстроту работы. Приоритет отдан
    простым конструкциям, в которых часто захардкожены те или иные части данных.

    Данный код не является кодом общего назначения и рассматривает узкие случаи. В связи с этим, при изменении формата
    ответа сервисов youtube.com, данный софт перестанет работать.
    '''
    def __init__(self, params=None):
        super().__init__(params)
        self._prefixes = {
            'ctoken': '"nextContinuationData":{"continuation":"',
        }
        self._suffixes = {
            'ctoken': '","clickTrackingParams":',
        }
        self._target = {
            'ctoken': self._any_symbols,
        }

    def get_comments(self, url, max_page=None):
        text = self._get_resp_text(url)
        ctoken = self._extract_regexp_substr(text, 'ctoken')
        self._none_exception(ctoken)
