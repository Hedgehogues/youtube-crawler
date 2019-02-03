import subprocess


class FfmpegWavTranscoder:
    def __init__(self):
        self.format = 'wav'

    def apply(self, audio_name):
        cmd = ['ffmpeg', '-loglevel', 'panic', '-i', audio_name, audio_name+'X.'+self.format]
        subprocess.call(cmd)
        cmd = ['mv', audio_name+'X.'+self.format, audio_name]
        subprocess.call(cmd)
