import os
from looptools import Counter


class Crawler:
    def __init__(self, directory, filters, full_paths, topown, _printer):
        """Sub class of DirPaths used for sequential directory parsing"""
        self.directory = directory
        self.filters = filters
        self.topdown = topown
        self._printer = _printer

        self.filepaths = []

        if full_paths:
            self.add_path = self._add_filepath_absolute
            self._printer('Absolute paths')
        else:
            self.add_path = self._add_filepath_relative
            self._printer('Relative paths')

    def __iter__(self):
        return iter(self.filepaths)

    def __len__(self):
        return len(self.filepaths)

    def _add_filepath_relative(self, directory, fullname):
        self.filepaths.append(fullname)

    def _add_filepath_absolute(self, directory, fullname):
        self.filepaths.append(os.path.join(directory, fullname))

    def crawler(self):
        if self.filters:
            self._printer('Filtering enabled')
            self.filter()
        else:
            self._printer('Filtering disabled')
            self.encompass()
        return self.filepaths

    def encompass(self):
        """
        Called when parallelize is False.
        This function will generate the file names in a directory tree by walking the tree either top-down or
        bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple
        (dirpath, dirnames, filenames).
        """
        self._printer('Standard Walk')
        count = Counter(length=3)
        for directory in self.directory:
            for root, directories, files in os.walk(directory, topdown=self.topdown):
                root = root[len(str(directory)) + 1:]
                self._printer(str(count.up) + ": Explored path - " + str(root), stream=True)
                for filename in files:
                    fullname = os.path.join(root, filename)
                    # Join the two strings in order to form the full filepath.
                    self.add_path(directory, fullname)

    def filter(self):
        """
        Called when parallelize is False.
        This function will generate the file names in a directory tree by walking the tree either top-down or
        bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple
        (dirpath, dirnames, filenames).
        """
        self._printer('Standard Walk')
        count = Counter(length=3)
        for directory in self.directory:
            self._printer('Searching ' + directory)
            for root, directories, files in os.walk(directory, topdown=self.topdown):
                root = root[len(str(directory)) + 1:]
                self._printer(str(count.up) + ": Explored path - " + str(root), stream=True)
                if self.filters.validate(root):
                    # Check that non-empty folders flag is on and we're at the max directory level
                    if self.filters.non_empty_folders and self.filters.get_level(root) == self.filters.max_level:
                        # Check that the path is not an empty folder
                        if os.path.isdir(directory + os.sep + root):
                            # Get paths in folder without walking directory
                            paths = os.listdir(directory + os.sep + root)

                            # Check that any of the paths are files and not just directories
                            if paths and any(os.path.isfile(os.path.join(directory, p)) for p in paths):
                                self.add_path(directory, root)

                    else:
                        for filename in files:
                            fullname = os.path.join(root, filename)
                            if self.filters.validate(fullname):
                                # Join the two strings in order to form the full filepath.
                                self.add_path(directory, fullname)
