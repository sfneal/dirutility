import unittest

from looptools import Timer

from dirutility.hash import Hash


# Disable immediate timer result printing
Timer().disable_printing()


class TestHashFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open('data/Public Site - Services.pdf', 'rb') as fp:
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
