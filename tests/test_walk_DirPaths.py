import os
import unittest
from dirutility.walk import DirPaths
from dirutility.walk.walk import hash_file
from tests import *


class TestWalk(unittest.TestCase):
    def test_DirPaths_multiprocess(self):
        paths = DirPaths(directory, full_paths=True, parallelize=True).walk()
        for i in paths:
            self.assertTrue(os.path.exists(i))

    def test_DirPaths_sequential(self):
        paths = DirPaths(directory, full_paths=True, parallelize=False).walk()
        for i in paths:
            self.assertTrue(os.path.exists(i))

    def test_DirPaths_sequential_nofilters(self):
        paths = DirPaths(directory, full_paths=True, parallelize=False, to_exclude=False).walk()
        for i in paths:
            self.assertTrue(os.path.exists(i))

    def test_DirPaths_hash(self):
        paths = DirPaths(directory, full_paths=True, parallelize=False, hash_files=True).walk()
        for path, _hash in paths:
            self.assertTrue(os.path.exists(path))
            self.assertEqual(_hash, hash_file(path))


if __name__ == '__main__':
    unittest.main()
