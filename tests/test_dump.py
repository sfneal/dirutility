import os
import unittest
from looptools import Timer
from dirutility import TextDump


class TestTextDumpWrite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data = 'dev.hpadesign.com beta.hpadesign.com dev.projects.hpadesign.com projects.hpadesign.com'
        cls.data += 'beta.projects.hpadesign.com staging.projects.hpadesign.com staging.hpadesign.com'
        cls.data = cls.data.split(' ')

        for f in os.listdir(os.path.dirname(__file__)):
            if f.startswith('test_dump') and f.endswith('.txt'):
                print('Removing: `{0}`'.format(f))
                os.remove(f)

    @Timer.decorator_noprint
    def test_dump_write(self):
        TextDump('test_dump_write.txt').write(self.data)

    @Timer.decorator_noprint
    def test_dump_append(self):
        td = TextDump('test_dump_append.txt')
        td.write(self.data)
        td.append(list(map(lambda x: '2: ' + x, self.data)))


if __name__ == '__main__':
    unittest.main()
