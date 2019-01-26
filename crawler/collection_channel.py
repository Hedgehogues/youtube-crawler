import youtube_dl
import os


path_to_channels = 'channels.tsv'
videos_dir = 'channels/'

if not os.path.exists(videos_dir):
    os.makedirs(videos_dir)

params = {
    'writeautomaticsub': True,
    'outtmpl': videos_dir+'%(channel_id)s/%(id)s',
    'format': 'bestaudio/best',
    'prefer-avconv': True,
    'subtitleslangs': ['ru'],
    'simulate': False,
    'max_sleep_interval': 2,
    'sleep_interval': 1,
    'ignoreerrors': True,
}

# TODO: Как обрабатывать ошибки и писать об этом в слак?
with open('../data/'+path_to_channels) as fd:
    for i, url in enumerate(fd):
        with youtube_dl.YoutubeDL(params) as ydl:
            ydl.download([url])




