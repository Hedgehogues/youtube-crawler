import json
import unittest


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.tests = []

    def __middleware(self, mws):
        for mw in mws:
            mw()

    def __valid(self, obj, kwargs, func, want, msg):
        res = func(obj, kwargs)
        self.assertEqual(want, res, msg=msg)

    def __exception(self, obj, kwargs, exception, func):
        is_exception = False
        try:
            func(obj, kwargs)
        except Exception as e:
            is_exception = True
            self.assertEqual(type(e), exception)
        self.assertTrue(is_exception)

    def apply_test(self, i, func):
        kwargs = self.tests[i].args
        want = self.tests[i].want
        obj = self.tests[i].object
        exception = self.tests[i].exception
        msg = self.tests[i].create_msg()
        with self.subTest(i=i, msg=msg):
            self.__middleware(self.tests[i].middlewares_before)
            if exception is None:
                self.__valid(obj, kwargs, func, want, msg)
            else:
                self.__exception(obj, kwargs, exception, func)
            self.__middleware(self.tests[i].middlewares_after)


class SubTest:
    def __init__(self, **kwargs):
        # Name of test
        self.name = self.fill('name', 'Test', kwargs)
        # Description of test
        self.description = self.fill('description', '', kwargs)
        # Arguments tested function
        self.args = self.fill('args', {}, kwargs)
        # Test function (need lambda wrapper) or test method of object
        self.object = kwargs['object']
        # Wanted answer
        self.want = self.fill('want', None, kwargs)
        # Wanted exception or None
        self.exception = self.fill('exception', None, kwargs)
        self.middlewares_before = self.fill('middlewares_before', [], kwargs)
        self.middlewares_after = self.fill('middlewares_after', [], kwargs)
        self.configuration = self.fill('configure_', {}, kwargs)

    @staticmethod
    def fill(k, r, kwargs):
        return kwargs[k] if k in kwargs else r

    def create_msg(self):
        descr = self.description
        conf = json.dumps(self.configuration)
        msg = ''
        if descr is not None:
            msg += 'Description: %s. ' % descr
        if descr is not None:
            msg += 'Configuration: %s. ' % conf
        return msg
