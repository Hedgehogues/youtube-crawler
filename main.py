import logging
import os

from internal import arguments
from internal import compose

# TODO: Внутри crawler сделать нормальные декораторы
# TODO: из первого канала скачалось только 50 видео. А где остальные? Скорее всего они не скачались, т.к. у них нет субтитров
# TODO: учитывать, что если произошёл отваливание по таймауту, то скорее всего ютуб залочил. Нужно устанавливать какие-то политики поведения


def main():
    args = arguments.parse()
    crawler = compose.build_crawler(**args)
    if args['logging_filename'] is not None and os.path.exists(args['logging_filename']):
        os.remove(args['logging_filename'])
    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s [%(name)s]: %(message)s',
        filename=args['logging_filename']
    )

    with open(args['base_channels']) as fd:
        channel_ids = list(filter(lambda x: len(x) > 0, map(compose.sep_url, fd.readlines())))

    crawler.process(channel_ids)


if __name__ == '__main__':
    main()
