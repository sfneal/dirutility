import os
from argparse import ArgumentParser


class TextDump:
    def __init__(self, file_path, verbose=0):
        self.file_path = file_path
        self._verbose = verbose

    def printer(self, statement):
        if self._verbose > 0:
            print(statement)

    @staticmethod
    def _encode_data(data, split=None, skip=None):
        """Encode data as a string in order to write to a text file."""
        data = data.split(split) if split else data
        if isinstance(data, (list, tuple, set)):
            data = [d for d in data if skip not in d] if skip else data
            return '\n'.join(data)
        else:
            return data

    def read(self, return_type=None):
        self.printer('Reading from text file `{}`'.format(self.file_path))
        with open(self.file_path, 'r') as txt:
            if str(return_type) == 'list':
                return ' '.join(txt.read().splitlines())
            else:
                return txt.read()

    def write(self, data, split=None, unique=False, skip=None):
        self.printer('Writing to text file `{}`'.format(self.file_path))
        with open(self.file_path, 'w') as txt:
            result = txt.write(self._encode_data(data, split, skip))

        # Remove repeated lines if unique is True
        if unique:
            self.write(list(set(self.read().split('\n'))))

    def append(self, data, split=None, unique=False, skip=None):
        self.printer('Appending to text file `{}`'.format(self.file_path))
        write_newline = False
        if os.path.exists(self.file_path):
            write_newline = True if len(self.read(list)) > 0 else False
        with open(self.file_path, 'a') as txt:
            if write_newline:
                txt.write('\n')
            result = txt.write(self._encode_data(data, split, skip))

        # Remove repeated lines if unique is True
        if unique:
            self.write(list(set(self.read().split('\n'))))


def reader(file_path, return_type):
    """Read a text file and return its contents."""
    return TextDump(file_path).read(return_type)


def writer(file_path, data, split=None, unique=False, skip=False):
    """Write to a text file and return its contents."""
    return TextDump(file_path).write(data, split, unique, skip)


def appender(file_path, data, split=None, unique=False, skip=False):
    """Append a text file and return its contents."""
    return TextDump(file_path).append(data, split, unique, skip)


def main():
    """
    Example Usage:

    $ text-dump append --file-path domains.txt --data "projects.localhost" --split ' ' --unique
    $ text-dump write --file-path domains.txt --data "dev.hpadesign.com staging.hpadesign.com beta.hpadesign.com public.localhost" --split ' ' --skip 'localhost'
    $ text-dump read --file-path domains.txt
    public.localhost"
    """
    # Declare argparse argument descriptions
    usage = 'Text dump utility.'
    description = 'Read, write and append text files.'
    helpers = {
        'file-path': "Path to text file to read/write to.",
        'data': "Data to write/append to the text file.",
        'split': "Character used separate a plain text list.",
        'unique': "Only write unique values to the text file.",
        'skip': "Skip writing a datapoint if the 'skip string' is found.",
        'return-type': "Type to return data in.",
    }

    # construct the argument parse and parse the arguments
    parser = ArgumentParser(usage=usage, description=description)
    sub_parser = parser.add_subparsers()

    # Read
    parser_read = sub_parser.add_parser('read')
    parser_read.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_read.add_argument('-t', '--return-type', help=helpers['return-type'], type=str)
    parser_read.set_defaults(func=reader)

    # Write
    parser_write = sub_parser.add_parser('write')
    parser_write.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_write.add_argument('-d', '--data', help=helpers['data'])
    parser_write.add_argument('-s', '--split', help=helpers['split'], type=str, default=None)
    parser_write.add_argument('-u', '--unique', help=helpers['unique'], action='store_true', default=False)
    parser_write.add_argument('--skip', help=helpers['skip'], type=str, default=False)
    parser_write.set_defaults(func=writer)

    # Append
    parser_write = sub_parser.add_parser('append')
    parser_write.add_argument('-f', '--file-path', help=helpers['file-path'], type=str)
    parser_write.add_argument('-d', '--data', help=helpers['data'])
    parser_write.add_argument('-s', '--split', help=helpers['split'], type=str, default=None)
    parser_write.add_argument('-u', '--unique', help=helpers['unique'], action='store_true', default=False)
    parser_write.add_argument('--skip', help=helpers['skip'], type=str, default=False)
    parser_write.set_defaults(func=appender)

    # Parse Arguments
    args = vars(parser.parse_args())
    func = args.pop('func')
    return func(**args)


if __name__ == '__main__':
    main()
