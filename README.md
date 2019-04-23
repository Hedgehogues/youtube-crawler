# Youtube-crawler

Утилита предназначена для получения данных (например, о каналах и видео) youtube.com в больших объёмах.
Инициализируется несколько начальных каналов, после чего, каждый из каналов скачивается
и из него извлекаются ссылки на каналы-соседи. Каждому из каналов, по некоторому алгоритму
присваивается метка о его релевантности. Все данные кладутся в БД (в дефолтной версии -- sqlite).
После получения всех данных из канала, из сформированной базы извлекается наиболее релевантный
канал и происходит краулинг данных. Данная система сделана с учётом того факта, что могут происходить
сбои в работе паука. В связи с этим, есть возможность производить обкачку данных примерно с того же места,
где произошёл сбой.

### Installation and running

    git clone https://github.com/Hedgehogues/youtube-crawler
    cd youtube-crawler
    pip install -r requirements.txt
    python main --logging-filename=./log

### Description of application:

    usage: main.py [-h] [--base-channels BASE_CHANNELS]
                   [--max-videos-page MAX_VIDEOS_PAGE]
                   [--max-channels-page MAX_CHANNELS_PAGE]
                   [--output-format {mp3,wav}] [--sqlite-path SQLITE_PATH]
                   [--db-mod {new,hard,old}] [--max-attempts MAX_ATTEMPTS]
                   [--log-level {DEBUG,INFO,WARN,ERROR,FATAL}]
                   [--logging-filename LOGGING_FILENAME]

    optional arguments:
      -h, --help            show this help message and exit
      --base-channels BASE_CHANNELS
                            base channels for start crawling
      --max-videos-page MAX_VIDEOS_PAGE
                            max count pages for downloading from video page of
                            channel
      --max-channels-page MAX_CHANNELS_PAGE
                            max count pages for downloading from channel page
                            about another channels
      --output-format {mp3,wav}
                            output video format
      --sqlite-path SQLITE_PATH
                            path to sqlite database file
      --db-mod {new,hard,old}
                            path to sqlite database file
      --max-attempts MAX_ATTEMPTS
                            max attempts retry for requests
      --log-level {DEBUG,INFO,WARN,ERROR,FATAL}
                            level of logging
      --logging-filename LOGGING_FILENAME
                            path to file for logging
