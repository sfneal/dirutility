import os
import shutil
import unittest
from time import sleep

from dirutility.open.open import tardir


destination = os.path.join(os.path.dirname(__file__), 'data')
if os.path.exists(destination):
    shutil.rmtree(destination)
if not os.path.exists(destination):
    os.mkdir(destination)


class TestArchive(unittest.TestCase):

    def test_tardir(self):
        tempfile = os.path.join(destination, 'kasdkfasdf.txt')
        with open(tempfile, 'w') as wfd:
            wfd.write(tempfile)
        with open(tempfile, 'r') as rfd1, open(tempfile, 'r') as rfd2:
            paths = {
                'abc': 'abc abc abc',
                'kbs': {
                    'haha': {},
                    'yoyo': {
                        'haha': rfd1
                    }
                },
                'abcd': {
                    'kbs': rfd2
                },
            }
            with tardir(os.path.join(destination, 'haha.tar.gz'), **paths) as tarfile:
                self.assertTrue(os.path.exists(tarfile.filepath))
            self.assertFalse(os.path.exists(tarfile.filepath))
        with open(tempfile, 'r') as rfd1, open(tempfile, 'r') as rfd2:
            paths = {
                'abc': 'abc abc abc',
                'kbs': {
                    'haha': {},
                    'yoyo': {
                        'haha': rfd1
                    }
                },
                'abcd': {
                    'kbs': rfd2
                },
            }
            with tardir(os.path.join(destination, 'haha.zip'), **paths, mode='w:zip', withdir=True) as tarfile:
                self.assertTrue(os.path.exists(tarfile.filepath))
                sleep(10)
            self.assertFalse(os.path.exists(tarfile.filepath))
        os.remove(tempfile)


if __name__ == '__main__':
    unittest.main()
