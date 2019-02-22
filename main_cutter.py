from cutter.cutter import AudioCutter

video_id = '-6RG9SfBkP0'
audio_name = video_id + '.wav'
subtitles_name = video_id + '.ru.vtt'
vtt = '.vtt'
path = 'data/test/videos/%s/' % video_id
cutter_path = 'cutter/x/'


cutter = AudioCutter()
cutter.apply(path + audio_name, path + subtitles_name, path + cutter_path)
