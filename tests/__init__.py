from enum import Enum


class MockLogger:
    def info(self, msg):
        pass

    def warn(self, err):
        pass

    def alert(self, err):
        pass

    def error(self, err):
        raise Exception


class MockTab(Enum):
    TEST0 = "test0"
    TEST1 = "test1"
    TEST2 = "test2"
