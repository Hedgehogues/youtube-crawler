import youtube_dl

# url = 'https://www.youtube.com/user/b64rus/'
# url = 'https://www.youtube.com/user/Russia24TV/'
# url = 'https://www.youtube.com/user/kreosan/'
# url = 'https://www.youtube.com/channel/UCKNNvv2ZSI7g3N69K8K0XmA'
# url = 'https://www.youtube.com/channel/UCPt9fydnENT7O4Sxbxbrlcg'
# url = 'https://www.youtube.com/channel/UCzO4TsqJwHB0rPSd02RZXJw'


# url = 'https://www.youtube.com/channel/UCDWofc3e1o5DTQEqFscxntA'


url = 'https://www.youtube.com/channel/UCEK3tT7DcfWGWJpNEDBdWog'
params = {
    'playlistend': 3,  # [1;max_n], playlistend <= max_n
    'playliststart': 1,  # [1;max_n], playliststart >= 1
    'writeautomaticsub': True,
    'writesubtitles': True,

    'format': 'bestaudio/best',
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer-avconv': True,
    'simulate': False,
}
ydl = youtube_dl.YoutubeDL(params)
descrs = ydl.extract_info(url, download=False, ie_key='YoutubeChannel')
for descr in descrs['entries']:
    ydl.process_video_result(descr)
    print(descr)


