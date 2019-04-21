import json
import os

import deepdiff
import unittest


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.tests_parse = []

    def __middleware(self, mws):
        for mw in mws:
            mw()

    def __valid(self, obj, kwargs, func, want, ignore, msg):
        res = func(obj, kwargs)
        if not ignore:
            diff = deepdiff.DeepDiff(want, res)
            self.assertEqual(0, len(diff), msg="want=%s, got=%s" % (want, res))

    def __exception(self, obj, kwargs, exception, func):
        self.assertRaises(exception, func, obj, kwargs)

    def check_exist_file(self, filename):
        self.assertTrue(os.path.exists(filename))

    @staticmethod
    def remove_filename(filename):
        if os.path.exists(filename):
            os.remove(filename)

    @staticmethod
    def create_filename(filename):
        if not os.path.exists(filename):
            open(filename, 'w').close()

    def apply_test(self, test, func):
        if test.fail:
            self.fail()
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
    Table data for object. If you want to test single function, you can use closure (lambda wrapper)

    :param name (str): name of test
    :param args (dict): arguments tested function
    :param description (str): description of test
    :param object (object): description of test
    :param want (object): wanted answer from function
    :param ignore_want (bool): ignore returned value of function if exception is not state.
        If exception generates into function, want ignore don't need. This param can use for
        test of constructor for instance.
    :param exception (Exception): exception expected from function or None (if exception is not raises).
        If exception is state, then field lwant is ignore
    :param middlewares_before (list): list of middlewares functions which execute before start function.
        Into middleware available all unittests methods. Response from middleware not processed
    :param middlewares_before (list): list of middlewares functions which execute after finished function.
        Into middleware available all unittests methods. Response from middleware not processed
    :param fail (bool): is true, then test will be fail
    self.configuration = self.fill('configuration', None, kwargs)
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
        self.fail = self.fill('fail', False, kwargs)

    @staticmethod
    def fill(k, r, kwargs):
        return kwargs[k] if k in kwargs else r

    def create_msg(self):
        descr = self.description
        msg = self.name + '. '
        if descr is not None:
            msg += 'Description: %s. ' % descr
        if self.configuration is not None:
            msg += 'Configuration: %s. ' % json.dumps(self.configuration)
        return msg
