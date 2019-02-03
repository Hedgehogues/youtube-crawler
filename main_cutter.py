from crawler.cutter.cutter import AudioCutter
from crawler.cutter.vtt_to_srt import vtt_to_srt


video_id = '_1anwjN9tPA'
audio_name = video_id
out_subtitles = video_id+'.ru'
srt = '.srt'
vtt = '.vtt'
path = 'data/test/videos/%s/' % video_id


vtt_to_srt(path+out_subtitles+vtt, replace=False)

cutter = AudioCutter()
cutter.apply(path+audio_name, path+out_subtitles+srt)
