import os
from dirutility.backup import ZipBackup


directory = '/Users/Stephen/Dropbox/Projects/SharpHockey/data_nhlapi/games/20172018'


def humanize_bytes(bytes, precision=2):
    """Return a humanized string representation of a number of bytes."""
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytes == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytes >= factor:
            break
    return '%.*f %s' % (precision, bytes / factor, suffix)


for i in range(0, 10):
    d = ZipBackup(directory, os.path.join(os.path.dirname(__file__), 'data'), compress_level=i).backup()
    print(humanize_bytes(os.path.getsize(str(d))), d)

