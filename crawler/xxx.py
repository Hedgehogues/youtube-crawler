from youtube_dl.extractor import gen_extractor_classes
from youtube_dl.extractor.common import InfoExtractor

infoExtractor = InfoExtractor()
downloader = gen_extractor_classes()[1126]
infoExtractor.set_downloader(downloader)
x = infoExtractor.extract('LJ1s8Esuyfw')

print(x)
