import os
from pathlib import Path
from tqdm import tqdm
from functools import reduce
from looptools import Counter


class DirectoryPaths:
    def __init__(self, directory, map_full_paths=True, files_to_include=None, files_to_exclude=None):
        self.map_full_paths = map_full_paths
        self.files_to_include = files_to_include
        self.files_to_exclude = files_to_exclude
        self.directory = directory
        self.filepaths = []

    def __iter__(self):
        return iter(self.filepaths)

    def _filepaths(self):
        self._filter()
        if self.map_full_paths:
            self._map_full_paths()
        return self.filepaths

    def _filter(self):
        if self.files_to_include:
            self.filepaths = [path for path in self.filepaths if Path(path).suffix in self.files_to_include]
        if self.files_to_exclude:
            self.filepaths = [path for path in self.filepaths if Path(path).suffix not in self.files_to_exclude]

    def _map_full_paths(self):
        self.filepaths = [os.path.join(self.directory, path) for path in self.filepaths]

    def basic(self):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        count = Counter()
        base = len(self.directory) + 1
        for root, directories, files in tqdm(os.walk(self.directory), desc='Walking Directory'):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root[base:], filename)
                if '.ds' not in str(filepath.lower()):
                    self.filepaths.append(filepath[:4] + "/" + filepath)  # Add it to the list.
                    count.up
        print("\t" + str(count.total) + " file paths have been parsed.")
        return self.filepaths  # Self-explanatory.

    @property
    def walk(self):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        # Set map full paths to false because roots are automatically joined
        for root, directories, files in os.walk(self.directory):
            for filename in files:
                if not filename.startswith('.'):
                    # Join the two strings in order to form the full filepath.
                    self.filepaths.append(os.path.join(root, filename))
        return self._filepaths()

    @property
    def files(self):
        """
        Return list of files in root directory
        """
        for path in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, path)):
                if not path.startswith('.'):
                    self.filepaths.append(path)
        return self._filepaths()

    @property
    def folders(self):
        """
        Return list of folders in root directory
        """
        for path in os.listdir(self.directory):
            if os.path.isdir(os.path.join(self.directory, path)):
                if not path.startswith('.'):
                    self.filepaths.append(path)
        return self._filepaths()


class DirectoryTree:
    def __init__(self, directory, branches=None):
        """
        Creates a nested dictionary that represents the folder structure of rootdir
        """
        self.dir = {}
        self.directory = directory.rstrip(os.sep)
        self.start = self.directory.rfind(os.sep) + 1
        self.branches = branches

    def __iter__(self):
        return iter(self.dir)

    def _filter(self, folders, folder_or_file):
        for index in range(0, len(folders)):
            filters = self.branches[index][folder_or_file]
            if filters:
                exclude = filters.get
                include = filters.get

                if exclude and folders[index] in exclude:
                    return False
                if include and folders[index] not in include:
                    return False
        return True

    @property
    def get(self):
        for path, dirs, files in os.walk(self.directory):
            folders = path[self.start:].split(os.sep)
            if self.branches:
                if self._filter(folders, 'folders'):
                    files = dict.fromkeys(files)
                    parent = reduce(dict.get, folders[:-1], self.dir)
                    parent[folders[-1]] = files
            else:
                files = dict.fromkeys(files)
                parent = reduce(dict.get, folders[:-1], self.dir)
                parent[folders[-1]] = files
        return self.dir
