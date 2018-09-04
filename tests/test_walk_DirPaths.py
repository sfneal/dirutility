import os
import unittest
from dirutility.walk import DirPaths
from tests import *


class TestWalk(unittest.TestCase):
    def test_DirPaths_multiprocess(self):
        paths = DirPaths(directory, console_stream=False, console_output=False, full_paths=True,
                         parallelize=True).walk()
        for i in paths:
            self.assertTrue(os.path.exists(i))

    def test_DirPaths_sequential(self):
        paths = DirPaths(directory, console_stream=False, console_output=False, parallelize=False).walk()
        for i in paths:
            self.assertTrue(os.path.exists(i))


if __name__ == '__main__':
    unittest.main()
