from tests.utils import BaseTestClass, SubTest


class TestScrapper(BaseTestClass):
    """
    Token save information about next page
    """

    def setUp(self):
        self.tests = [
            SubTest(
                name="Test 1",
                description="",
                configuration={},
                args={'vtt_path': ''},
                object=None,
                want={},
                exception=None,
            )
        ]

    def test_parse(self):
        for i in range(len(self.tests)):
            self.apply_test(i, lambda obj, kwargs: obj.transform(**kwargs))
