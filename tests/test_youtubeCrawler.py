# from unittest import TestCase
#
# from crawler.crawler import YoutubeCrawler
# from tests.utils import SubTest
#
#
# class MockCache:
#
#     def set_channel_scrapped(self, channel_id):
#         raise Exception("Not implemented")
#
#     def set_channel_downloaded(self, channel_id):
#         raise Exception("Not implemented")
#
#     def set_video_descr(self, video):
#         raise Exception("Not implemented")
#
#     def check_video_descr(self, video_id):
#         raise Exception("Not implemented")
#
#     def set_empty_channels(self, channel_ids):
#         raise Exception("Not implemented")
#
#     def set_channel(self, channels):
#         raise Exception("Not implemented")
#
#     def update_channels(self, channel_id, channels):
#         raise Exception("Not implemented")
#
#     def get_best_channel_id(self):
#         raise Exception("Not implemented")
#
#
# class TestYoutubeCrawler(TestCase):
#     __prefix = '_test_'
#     __vtt = '.vtt'
#     __srt = '.srt'
#     __test_file = [
#         'data/videos/_1anwjN9tPA/_1anwjN9tPA.ru',
#         'data/videos/-6RG9SfBkP0/-6RG9SfBkP0.ru',
#     ]
#
#     def __get_checkfile_args(self, i):
#         return {
#             'test_file': self.__test_file[i],
#             'ext': self.__srt,
#             'prefix': self.__prefix,
#         }
#
#     def setUp(self):
#         self.tests = [
#             SubTest(
#                 name="Test 1",
#                 description='',
#                 args={'vtt_path': self.__test_file[0] + self.__vtt},
#                 object=YoutubeCrawler,
#                 middlewares_after=[lambda: self.check_file(**self.__get_checkfile_args(0))],
#             ),
#             SubTest(
#                 name="Test 2",
#                 description='File: %s' % os.path.basename(self.__test_file[1]),
#                 args={'vtt_path': self.__test_file[1] + self.__vtt},
#                 object=VTTtoSRT(prefix=self.__prefix),
#                 middlewares_after=[lambda: self.check_file(**self.__get_checkfile_args(1))],
#             ),
#             SubTest(
#                 name="Test 3",
#                 description='Fail vtt exception',
#                 args={'vtt_path': self.__test_file[0] + self.__vtt + '_'},
#                 object=VTTtoSRT(),
#                 exception=utils.ExtensionError,
#             )
#         ]
#
#     def test_transform(self):
#         for test in self.tests:
#             self.apply_test(test, lambda obj, kwargs: obj.transform(**kwargs))
