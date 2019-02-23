import json
import os
import unittest


# TODO: нельзя протестировать конструктор


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.tests_parse = []

    def __middleware(self, mws):
        for mw in mws:
            res = mw()
            if res is not None:
                self.assertTrue(res)

    def __valid(self, obj, kwargs, func, want, ignore, msg):
        res = func(obj, kwargs)
        if not ignore:
            self.assertEqual(want, res, msg=msg)

    def __exception(self, obj, kwargs, exception, func):
        is_exception = False
        try:
            func(obj, kwargs)
        except Exception as e:
            is_exception = True
            self.assertEqual(type(e), exception)
        self.assertTrue(is_exception)

    def check_file(self, test_file, ext, prefix):
        path, filename = os.path.split(test_file)
        fd = open('%s/%s' % (path, prefix + filename + ext))
        lines_got_srt = fd.readlines()
        fd.close()
        fd = open('%s/%s' % (path, filename + ext))
        lines_want_srt = fd.readlines()
        fd.close()
        for item in zip(lines_want_srt, lines_got_srt):
            self.assertEqual(item[0], item[1])
        self.assertEqual(len(lines_want_srt), len(lines_got_srt))
        os.remove('%s/%s' % (path, prefix + filename + ext))

    def apply_test(self, test, func):
        kwargs = test.args
        want = test.want
        obj = test.object
        exception = test.exception
        ignore = test.ignore_want
        msg = test.create_msg()
        with self.subTest(msg=msg):
            self.__middleware(test.middlewares_before)
            if exception is None:
                self.__valid(obj, kwargs, func, want, ignore, msg)
            else:
                self.__exception(obj, kwargs, exception, func)
            self.__middleware(test.middlewares_after)


class SubTest:

    """
    Table data for object. If you want data single function, you can use closure (lambda wrapper)

    :param name (str): name of data
    :param args (dict): arguments tested function
    :param description (str): description of data
    :param object (object): description of data
    :param want (object): wanted answer from function
    :param ignore_want (bool): ignore returned value of function if exception is not state.
        If exception is, then want ignore anyway. This param can use for test of constructor
    :param exception (Exception): exception of data case or None (if exception is not raises).
        If exception is state, then field lwant is ignore
    :param middlewares_before (list): list of middlewares functions which execute before start data.
        Each function must return True if all right or False another case. If function return None,
        than it means all right.
    :param middlewares_before (list): list of middlewares functions which execute after finished data.
        Each function must return True if all right or False another case. If function return None,
        than it means all right.
    self.configuration = self.fill('configure_', {}, kwargs)
    """

    def __init__(self, **kwargs):
        # Name of data
        self.name = self.fill('name', 'Default name test', kwargs)
        # Description of data
        self.description = self.fill('description', None, kwargs)
        # Arguments tested function
        self.args = self.fill('args', {}, kwargs)
        # Test function (need lambda wrapper) or data method of object
        self.object = kwargs['object']
        # Wanted answer
        self.want = self.fill('want', None, kwargs)
        # Ignore want
        self.ignore_want = self.fill('ignore_want', False, kwargs)
        # Wanted exception or None
        self.exception = self.fill('exception', None, kwargs)
        self.middlewares_before = self.fill('middlewares_before', [], kwargs)
        self.middlewares_after = self.fill('middlewares_after', [], kwargs)
        self.configuration = self.fill('configuration', None, kwargs)

    @staticmethod
    def fill(k, r, kwargs):
        return kwargs[k] if k in kwargs else r

    def create_msg(self):
        descr = self.description
        msg = self.name
        if descr is not None:
            msg += 'Description: %s. ' % descr
        if self.configuration is not None:
            msg += 'Configuration: %s. ' % json.dumps(self.configuration)
        return msg
