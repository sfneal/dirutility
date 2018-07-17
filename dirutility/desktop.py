import os


def desktop():
    try:
        home = os.environ['HOMEPATH']
    except KeyError:
        home = os.environ['HOME']
    return os.path.join(home, 'Desktop')