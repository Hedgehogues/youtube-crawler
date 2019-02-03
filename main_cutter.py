from crawler.cutter.cutter import AudioCutter
from crawler.cutter.vtt_to_srt import vtt_to_srt


audio_name = '-6RG9SfBkP0'
out_subtitles = '-6RG9SfBkP0.ru'
srt = '.srt'
vtt = '.vtt'
path = 'data/test/videos/'


vtt_to_srt(path+out_subtitles+vtt, replace=False)

cutter = AudioCutter()
cutter.apply(path+audio_name, path+out_subtitles+srt)
