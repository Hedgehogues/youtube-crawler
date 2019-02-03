from subs_audio_splicer.parser import Parser


parser = Parser('0XbLz0L6UdI.ru.srt')
for dialogue in parser.get_dialogues():
    print(dialogue.text)
    print(dialogue.start)
    print(dialogue.end)
