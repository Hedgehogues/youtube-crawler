class SimpleLogger:

    def info(self, msg):
        print("[INFO]: %s", msg)

    def warn(self, err):
        print("[WARN]: %s. StackError: %s" % (err.msg, err.get_stack_errors()))

    def alert(self, err):
        print("[ALERT]: %s. StackError: %s" % (err.msg, err.get_stack_errors()))

    def error(self, err):
        print("[ERROR]: %s. StackError: %s" % (err.msg, err.get_stack_errors()))
        raise err
