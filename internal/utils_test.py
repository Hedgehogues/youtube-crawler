import json
import unittest
from collections import namedtuple


class BaseTestClass(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(BaseTestClass, self).__init__(*args, **kwargs)
        self.tests = []

    def _apply_test(self, i):
        kwargs = self.tests[i].args
        want = self.tests[i].want
        obj = self.tests[i].object
        exception = self.tests[i].exception
        msg = self._create_msg(i)
        with self.subTest(i=i, msg=msg):
            if exception is None:
                res = obj.parse(**kwargs)
                self.assertEqual(want, res, msg=msg)
                return
            is_exception = False
            try:
                obj.parse(**kwargs)
            except Exception as e:
                is_exception = True
                self.assertEqual(type(e), exception)
            self.assertTrue(is_exception)

    def _create_msg(self, i):
        descr = self.tests[i].description
        conf = json.dumps(self.tests[i].configuration)
        msg = ''
        if descr is not None:
            msg += 'Description: %s. ' % descr
        if descr is not None:
            msg += 'Configuration: %s. ' % conf
        return msg


SubTest = namedtuple(
    'SubTest',
    [
        'name',  # Name of test
        'description',  # Description of test
        'configuration',  # Configuration input parameters
        'args',  # Arguments tested function
        'object',  # Test function (need lambda wrapper) or test method of object
        'want',  # Wanted answer
        'exception'  # Wanted exception or None
    ]
)
