class SimpleLogger:

    def info(self, msg):
        print("[INFO]: %s" % msg)

    def warn(self, err):
        print("[WARN]: %s" % err)

    def alert(self, err):
        print("[ALERT]: %s" % err)
        raise err

    def error(self, err):
        print("[ERROR]: %s" % err)
