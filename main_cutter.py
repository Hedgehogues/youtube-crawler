from crawler.cutter.cutter import AudioCutter


video_id = '_1anwjN9tPA'
audio_name = video_id
out_subtitles = video_id+'.ru'
srt = '.srt'
vtt = '.vtt'
path = 'data/test/videos/%s/' % video_id


cutter = AudioCutter()
cutter.apply(path+audio_name, path+out_subtitles+srt)
