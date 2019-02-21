from crawler import parsers
from tests.utils import BaseTestClass, SubTest


class TestReloaderParser(BaseTestClass):
    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description=None,
                args={},
                object=parsers.ReloaderParser(),
            ),
        ]

    # def test_parse(self):
    #     for i in range(len(self.tests)):
    #         self.apply_test(i, lambda obj, kwargs: obj.transform(**kwargs))
