import unittest
from time import sleep

from looptools import Timer

from dirutility.multiprocess import pool_process


def test_func(a):
    sleep(.1)
    return a * a


FUNC = test_func
ITER = list(range(100))
EXPECTED = set([a * a for a in range(100)])


class TestMultiprocessFunc(unittest.TestCase):
    def setUp(self):
        self.result = None

    def tearDown(self):
        if isinstance(self.result, list):
            self.assertEqual(set(self.result), EXPECTED)

    @Timer.decorator
    def test_basic(self):
        self.result = pool_process(FUNC, ITER)

    @Timer.decorator
    def test_return_vals(self):
        self.result = pool_process(FUNC, ITER, return_vals=True)


if __name__ == '__main__':
    unittest.main()
