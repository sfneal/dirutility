from platform import system


if system() is 'Darwin':
    directory = "/Users/Stephen/Sites/stephenneal.net/HTML"
elif system() is 'Windows':
    directory = "/Users/Stephen/Sites/stephenneal.net/HTML"
else:
    directory = "/Users/Stephen/Sites/stephenneal.net/HTML"


__all__ = ['directory']
