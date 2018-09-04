from platform import system


if system() is 'Darwin':
    directory = "/Users/Stephen/Dropbox/stephenneal.net/cis381"
elif system() is 'Windows':
    directory = "/Users/Stephen/Dropbox/stephenneal.net/cis381"
else:
    directory = "/Users/Stephen/Dropbox/stephenneal.net/cis381"


__all__ = ['directory']
