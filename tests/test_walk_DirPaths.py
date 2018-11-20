import os
import unittest
from datetime import datetime
from dirutility.walk import DirPaths
from dirutility.walk.walk import md5_hash
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
            self.assertEqual(_hash, md5_hash(path))

    def test_DirPaths_created_at(self):
        dp = DirPaths(directory, full_paths=True, parallelize=True)
        dp.walk()
        file_created = dp.creation_dates(sort=True)

        for path, created_at in file_created:
            self.assertTrue(os.path.exists(path))
            self.assertTrue(isinstance(created_at, datetime))


if __name__ == '__main__':
    unittest.main()
