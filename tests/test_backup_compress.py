import os
import shutil
from dirutility.backup import ZipBackup


directory = '/Users/Stephen/Dropbox/Projects/SharpHockey/data_nhlapi/games/20172018'
destination = os.path.join(os.path.dirname(__file__), 'data')
if os.path.exists(destination):
    shutil.rmtree(destination)
if not os.path.exists(destination):
    os.mkdir(destination)


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
    d = ZipBackup(directory, destination, compress_level=i).backup()
    print(humanize_bytes(os.path.getsize(str(d))), d)

