import unittest

from looptools import Timer

from dirutility.hash import Hash


class TestHashString(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hash = Hash(b'Nobody inspects the spammish repetition')

    @Timer.decorator
    def test_md5(self):
        self.hash.md5()

    @Timer.decorator
    def test_sha1(self):
        self.hash.sha1()

    @Timer.decorator
    def test_sha256(self):
        self.hash.sha256()

    @Timer.decorator
    def test_sha512(self):
        self.hash.sha512()

    @Timer.decorator
    def test_blake2b(self):
        self.hash.blake2b()

    @Timer.decorator
    def test_blake2s(self):
        self.hash.blake2s()

    @Timer.decorator
    def test_shake_128(self):
        self.hash.shake_128()

    @Timer.decorator
    def test_xxh32(self):
        self.hash.xxh32()

    @Timer.decorator
    def test_xxh64(self):
        self.hash.xxh64()


if __name__ == '__main__':
    unittest.main()
