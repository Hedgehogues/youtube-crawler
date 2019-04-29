from crawler import utils
from internal import arguments
from internal import compose

# TODO: выпилить стрёмные ошибки из краулера
# TODO: Внутри crawler сделать нормальные декораторы
# TODO: из первого канала скачалось только 50 видео. А где остальные? Скорее всего они не скачались, т.к. у них нет субтитров
# TODO: учитывать, что если произошёл отваливание по таймауту, то скорее всего ютуб залочил. Нужно устанавливать какие-то политики поведения
# TODO: использовать несколько уровней логгирования (youtube-dl, crawler)


def main():
    args = arguments.parse()
    crawler = compose.build_crawler(**args)

    with open(args['base_channels']) as fd:
        channel_ids = list(filter(lambda x: len(x) > 0, map(compose.sep_url, fd.readlines())))

    crawler.process(channel_ids)


if __name__ == '__main__':
    main()
