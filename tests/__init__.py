class MockLogger:
    def info(self, msg):
        pass

    def warn(self, err):
        pass

    def alert(self, err):
        pass

    def error(self, err):
        raise Exception
