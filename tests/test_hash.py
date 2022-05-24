import unittest
import os
from looptools import Timer
from tests import directory
from dirutility import Hash, DirPaths, PoolProcess

FILE = os.path.join(os.path.dirname(__file__), 'document.pdf')
DIRECTORY = directory


def get_paths():
    return DirPaths(DIRECTORY, full_paths=True, parallelize=False).walk()


def hash_file(path):
    with open(path, 'rb') as fp:
        return Hash(fp.read())


def hash_file_xxh64(path):
    return hash_file(path).xxh64()


def hash_file_xxh32(path):
    return hash_file(path).xxh32()


def hash_file_md5(path):
    return hash_file(path).md5()


def hash_file_sha256(path):
    return hash_file(path).sha256()


class TestHashFilesRecursive(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.paths = get_paths()
        print(len(cls.paths))

    @classmethod
    def tearDownClass(cls):
        print('\n\nRecursive File Hashing results\n' + '-' * 68)
        Timer().print_times('TestHashFile')

    @Timer.decorator_noprint
    def test_xxh64(self):
        return PoolProcess(hash_file_xxh64, self.paths).map_return()

    @Timer.decorator_noprint
    def test_xxh32(self):
        return PoolProcess(hash_file_xxh32, self.paths).map_return()

    @Timer.decorator_noprint
    def test_md5(self):
        return PoolProcess(hash_file_md5, self.paths).map_return()

    @Timer.decorator_noprint
    def test_sha256(self):
        return PoolProcess(hash_file_sha256, self.paths).map_return()


class TestHashFile(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(FILE, 'rb') as fp:
            cls.hash = Hash(fp.read())

    @classmethod
    def tearDownClass(cls):
        print('\n\nFile Hashing results\n' + '-' * 68)
        Timer().print_times('TestHashFile')

    @Timer.decorator_noprint
    def test_md5(self):
        self.hash.md5()

    @Timer.decorator_noprint
    def test_sha1(self):
        self.hash.sha1()

    @Timer.decorator_noprint
    def test_sha256(self):
        self.hash.sha256()

    @Timer.decorator_noprint
    def test_sha512(self):
        self.hash.sha512()

    @Timer.decorator_noprint
    def test_blake2b(self):
        self.hash.blake2b()

    @Timer.decorator_noprint
    def test_blake2s(self):
        self.hash.blake2s()

    @Timer.decorator_noprint
    def test_shake_128(self):
        self.hash.shake_128()

    @Timer.decorator_noprint
    def test_xxh32(self):
        self.hash.xxh32()

    @Timer.decorator_noprint
    def test_xxh64(self):
        self.hash.xxh64()


class TestHashString(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hash = Hash(b'Nobody inspects the spammish repetition')

    @classmethod
    def tearDownClass(cls):
        print('\n\nString Hashing results\n' + '-' * 68)
        Timer().print_times('TestHashString')

    @Timer.decorator_noprint
    def test_md5(self):
        self.hash.md5()

    @Timer.decorator_noprint
    def test_sha1(self):
        self.hash.sha1()

    @Timer.decorator_noprint
    def test_sha256(self):
        self.hash.sha256()

    @Timer.decorator_noprint
    def test_sha512(self):
        self.hash.sha512()

    @Timer.decorator_noprint
    def test_blake2b(self):
        self.hash.blake2b()

    @Timer.decorator_noprint
    def test_blake2s(self):
        self.hash.blake2s()

    @Timer.decorator_noprint
    def test_shake_128(self):
        self.hash.shake_128()

    @Timer.decorator_noprint
    def test_xxh32(self):
        self.hash.xxh32()

    @Timer.decorator_noprint
    def test_xxh64(self):
        self.hash.xxh64()


if __name__ == '__main__':
    unittest.main()
