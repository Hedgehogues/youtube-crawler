from enum import Enum

from crawler.loaders import Tab


class MockTab(Enum):
    TEST0 = "test0"
    TEST1 = "test1"
    TEST2 = "test2"


full_descr_mock = {
    Tab.HomePage: [
        {
            'owner_channel': {
                'id': 'UCzAzPC4VWIMHqrnIM1iBPsQ',
                'title': 'Tero',
                'verified': False,
                'count_subscribers': '79\xa0900 подписчиков',
                'tags': []
            },
            'videos': {
                'others': [
                    {
                        'title': 'Все видео',
                        'videos': [
                            {
                                'id': '77zRrFOuW0k',
                                'title': '😹 Иностранец реагирует на Miyagi & Andy Panda - Get Up',
                                'published_time': '1 день назад',
                                'count_views': '12\xa0356 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '5:17'
                            }, {
                                'id': 'CQbaAZ1px9Y',
                                'title': 'Reaktion | KIANUSH - SO JUNG  | Mordsstimme?',
                                'published_time': '1 день назад',
                                'count_views': '402 просмотра',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '10:28'
                            }, {
                                'id': 'W1vDil6MXV4',
                                'title': 'Reaktion | MASSIV FEAT. RAMO - PSHT  | Ist das der alte Massiv?',
                                'published_time': '1 день назад',
                                'count_views': '851 просмотр',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '8:41'
                            }, {
                                'id': 'WHKMNgfAhFc',
                                'title': '😹 Иностранец реагирует на масло черного тмина - аппарат президента 2',
                                'published_time': '1 день назад',
                                'count_views': '5\xa0014 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '4:44'
                            }, {
                                'id': 'nro8jiv81Xo',
                                'title': 'Reaktion | Kontra K feat. Veysel - Blei | Was ein Kontrast',
                                'published_time': '3 дня назад',
                                'count_views': '746 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '7:54'
                            }, {
                                'id': 'gFGSB6XgS0Y',
                                'title': '😹 Иностранец реагирует на alyona alyona & Alina Pash - Падло',
                                'published_time': '3 дня назад',
                                'count_views': '28\xa0294 просмотра',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '8:16'
                            }, {
                                'id': 'dj07UStI9Bg',
                                'title': 'Reaktion | SAMRA - SHOOTE MA SHOOTE | Was eine Bombe',
                                'published_time': '3 дня назад',
                                'count_views': '438 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '7:26'
                            }, {
                                'id': 'paqZ995ahug',
                                'title': '😹 Иностранец реагирует на OttO - UNREAL',
                                'published_time': '3 дня назад',
                                'count_views': '2\xa0826 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '4:26'
                            }, {
                                'id': 'g10xnXNcydU',
                                'title': 'Reaktion | CAPITAL BRA, KC REBELL & SUMMER CEM - ROLEX | Trio des lebenes?',
                                'published_time': '5 дней назад',
                                'count_views': '793 просмотра',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '9:39'
                            }, {
                                'id': 'mBJQRkRiAEM',
                                'title': '😹 Иностранец реагирует на Johnyboy - HOODIE',
                                'published_time': '6 дней назад',
                                'count_views': '4\xa0820 просмотров',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '5:34'
                            }, {
                                'id': 'hum1caC1aRo',
                                'title': '😹 Иностранец реагирует на МАЙК СТИКС - Tripsitter',
                                'published_time': '6 дней назад',
                                'count_views': '6\xa0001 просмотр',
                                'has_custom_subtitles': False,
                                'verified': False,
                                'duration': '14:59'
                            }
                        ]
                    }
                ],
                'general': [
                    {
                        'id': 'eKf8fAqAQBc',
                        'title': '(Ледяной сахар) Tero - Zucker Eis',
                        'description_parts': None,
                        'published_time': '1 месяц назад',
                        'count_views': '10\xa0605 просмотров'
                    }
                ]
            },
            'channels': [
                {
                    'channel_id': 'UCmKXJ_GDAyitVCIu8z_wKhg',
                    'channel_name': 'ВИД ВИДНЫЙ',
                    'count_videos': '1\xa0159 видео',
                    'count_subscribers': '167\xa0тыс.',
                    'verified': False
                }, {
                    'channel_id': 'UCvfSetaLGemgGTteTrgqOag',
                    'channel_name': 'GlebaTV',
                    'count_videos': '88 видео',
                    'count_subscribers': '510\xa0тыс.',
                    'verified': True
                },
                {
                    'channel_id': 'UCJ__5k6NqgJySelFO53WAIA',
                    'channel_name': 'Versus Rap Channel',
                    'count_videos': '1\xa0177 видео',
                    'count_subscribers': '38\xa0тыс.',
                    'verified': False
                }, {
                    'channel_id': 'UCbNEph0nbcJtpQco_5W7jRQ',
                    'channel_name': 'Мама Туся',
                    'count_videos': '469 видео',
                    'count_subscribers': '319\xa0тыс.',
                    'verified': True},
                {
                    'channel_id': 'UCbrI9IBM9N1SNc-XZZolFkg',
                    'channel_name': 'Батя Тестит',
                    'count_videos': '230 видео',
                    'count_subscribers': '25\xa0тыс.',
                    'verified': False
                },
                {
                    'channel_id': 'UCtXqCOwm-OeSHGXUjwc_HHA',
                    'channel_name': 'KING DEMI',
                    'count_videos': '732 видео',
                    'count_subscribers': '34\xa0тыс.',
                    'verified': False
                }
            ]
        }
    ],
    Tab.Videos: [
        [
            {
                'id': '77zRrFOuW0k',
                'title': '😹 Иностранец реагирует на Miyagi & Andy Panda - Get Up',
                'published_time': '1 день назад',
                'view_counts': '12\xa0356 просмотров',
                'has_custom_subtitles': False,
                'verified': False,
                'duration': '5:17'
            }, {
            'id': 'CQbaAZ1px9Y',
            'title': 'Reaktion | KIANUSH - SO JUNG  | Mordsstimme?',
            'published_time': '1 день назад',
            'view_counts': '402 просмотра',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '10:28'
        }, {
            'id': 'W1vDil6MXV4',
            'title': 'Reaktion | MASSIV FEAT. RAMO - PSHT  | Ist das der alte Massiv?',
            'published_time': '1 день назад',
            'view_counts': '851 просмотр',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '8:41'
        }, {
            'id': 'WHKMNgfAhFc',
            'title': '😹 Иностранец реагирует на масло черного тмина - аппарат президента 2',
            'published_time': '1 день назад',
            'view_counts': '5\xa0014 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '4:44'
        }, {
            'id': 'nro8jiv81Xo',
            'title': 'Reaktion | Kontra K feat. Veysel - Blei | Was ein Kontrast',
            'published_time': '3 дня назад',
            'view_counts': '746 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '7:54'
        }, {
            'id': 'gFGSB6XgS0Y',
            'title': '😹 Иностранец реагирует на alyona alyona & Alina Pash - Падло',
            'published_time': '3 дня назад',
            'view_counts': '28\xa0294 просмотра',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '8:16'
        }, {
            'id': 'dj07UStI9Bg',
            'title': 'Reaktion | SAMRA - SHOOTE MA SHOOTE | Was eine Bombe',
            'published_time': '3 дня назад',
            'view_counts': '438 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '7:26'
        }, {
            'id': 'paqZ995ahug',
            'title': '😹 Иностранец реагирует на OttO - UNREAL',
            'published_time': '3 дня назад',
            'view_counts': '2\xa0826 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '4:26'
        }, {
            'id': 'g10xnXNcydU',
            'title': 'Reaktion | CAPITAL BRA, KC REBELL & SUMMER CEM - ROLEX | Trio des lebenes?',
            'published_time': '5 дней назад',
            'view_counts': '793 просмотра',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '9:39'
        }, {
            'id': 'mBJQRkRiAEM',
            'title': '😹 Иностранец реагирует на Johnyboy - HOODIE',
            'published_time': '6 дней назад',
            'view_counts': '4\xa0820 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '5:34'
        }, {
            'id': 'hum1caC1aRo',
            'title': '😹 Иностранец реагирует на МАЙК СТИКС - Tripsitter',
            'published_time': '6 дней назад',
            'view_counts': '6\xa0001 просмотр',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '14:59'
        }, {
            'id': 'XQZF0I1gZDE',
            'title': '😹 Иностранец реагирует на JEEMBO feat. Boulevard Depo & ЛАУД — M.O.D.',
            'published_time': 'Неделю назад',
            'view_counts': '18\xa0724 просмотра',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '6:00'
        }, {
            'id': 'KgLIo1N7CbU',
            'title': 'Neuer Style? | Apache 207 - KEIN PROBLEM',
            'published_time': 'Неделю назад',
            'view_counts': '1\xa0522 просмотра',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '6:55'
        }, {
            'id': 'u24digR5IP8',
            'title': '😹 Иностранец реагирует на PIEM, OXXXYMIRON, J. MAKONNEN, DINAST, LETAI, PALMDROPOV - REALITY',
            'published_time': 'Неделю назад',
            'view_counts': '77\xa0248 просмотров',
            'has_custom_subtitles': False,
            'verified': False,
            'duration': '16:50'
        }, {
            'id': 'rjUdlSGSuH8', 'title': '😹 Иностранец реагирует на Andy Panda feat. Скриптонит, 104, TumaniYO & Miyagi - Billboard', 'published_time': 'Неделю назад', 'view_counts': '57\xa0574 просмотра', 'has_custom_subtitles': False, 'verified': False, 'duration': '7:44'
        }, {
            'id': 'G369KBtRk9k', 'title': '😹 Иностранец реагирует на JOKEASSES - УЯТ', 'published_time': 'Неделю назад', 'view_counts': '5\xa0878 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '6:43'
        }, {
            'id': 'm7oALSDQADo', 'title': 'Reaktion auf Fler ✖️Vermächtnis✖️  | Bestes Album', 'published_time': 'Неделю назад', 'view_counts': '748 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '10:16'
        }, {
            'id': 'p0r0BOMguVU', 'title': '😹 Иностранец реагирует на alyona alyona - Пушка', 'published_time': 'Неделю назад', 'view_counts': '64\xa0785 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '5:57'
        }, {
            'id': 'JuX5bMyt2Ns', 'title': '😹 Иностранец реагирует на RAM - TRAUMATIX', 'published_time': '2 недели назад', 'view_counts': '16\xa0135 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '36:52'
        }, {
            'id': 'vfHeKcJhTdM', 'title': '😹 Иностранец реагирует на Miyagi - Angel', 'published_time': '2 недели назад', 'view_counts': '47\xa0395 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '6:15'
        }, {
            'id': 'Rb5lQ-Wowuk', 'title': 'Reaktion auf CAPITAL BRA - CHERRY LADY | Dieter Bohlen auf dem Olymp der Musikgeschichte?', 'published_time': '3 недели назад', 'view_counts': '2\xa0039 просмотров', 'has_custom_subtitles': False, 'verified': False, 'duration': '5:36'
        }
        ]
    ],
    Tab.Channels: [],
    Tab.About: [
        {
            'title': 'Tero',
            'description': 'Spaß und meine Füße\n\nAdresse:\n\nPostfach 11 01\n49493 Mettingen\nGermany',
            'joined_date': 'Дата регистрации: 8 мая 2012 г.',
            'count_views': '17\xa0135\xa0853',
            'count_subscribers': '79\xa0899',
            'links': []
        }
    ]
}

