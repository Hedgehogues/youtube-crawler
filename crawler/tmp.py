import youtube_dl
import os


path_to_channels = 'channels.tsv'
videos_dir = 'channels/'

if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

params = {
    # 'listsubtitles': True,
}

url = 'https://www.youtube.com/watch?v=Ye8mB6VsUHw'
with youtube_dl.YoutubeDL(params) as ydl:
    video_descr_extractor = ydl.get_info_extractor(youtube_dl.gen_extractors()[1125].ie_key())
    ie_result = video_descr_extractor.extract(url)
    ydl.download([url])

print(ie_result)
