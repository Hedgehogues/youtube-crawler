from crawler import utils


class SimpleLogger:
    def __get_stack_err(self, err):
        stack_err = None
        if err is utils.CrawlerExceptions:
            stack_err = err.get_stack_errors()
        return stack_err

    def info(self, msg):
        print("[INFO]: %s", msg)

    def warn(self, err):
        print("[WARN]: %s. StackError: %x" % (err.msg, self.__get_stack_err(err)))

    def alert(self, err):
        print("[ALERT]: %s. StackError: %x" % (err.msg, self.__get_stack_err(err)))

    def error(self, err):
        print("[ERROR]: %s. StackError: %x" % (err.msg, self.__get_stack_err(err)))
        raise err
