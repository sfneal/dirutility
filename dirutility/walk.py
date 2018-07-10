import os
from pathlib import Path
from tqdm import tqdm
from functools import reduce
from looptools import Counter


class DirPaths:
    def __init__(self, directory, full_paths=False, topdown=True, to_include=None, to_exclude=None,
                 console_output=False, only_files=False, only_folders=False):
        """
        This class generates a list of either files and or folders within a root directory.  The walk method
        generates a directory list of files by walking the file tree top down or bottom up.  The files and folders
        method generate a list of files or folders in the top level of the tree.
        :param directory: Starting directory file path
        :param full_paths: Bool, when true full paths are concatenated to file paths list
        :param topdown: Bool, when true walk method walks tree from the topdwon. When false tree is walked bottom up
        :param to_include: None by default.  List of filters acceptable to find within file path string return
        :param to_exclude: None by default.  List of filters NOT acceptable to return
        :param console_output: Bool, when true console output is printed
        :param only_files: Bool, when true only files in the root directory are returned
        :param only_folders: Bool, when true only folders in the root directort are returned
        """
        self.directory = directory
        self.full_paths = full_paths
        self.topdown = topdown
        self.to_include = to_include
        self.to_exclude = to_exclude
        self.console_output = console_output
        self.filepaths = []

        if only_files:
            self.files()
        elif only_folders:
            self.folders()
        else:
            self.walk()

    def __iter__(self):
        return iter(self.filepaths)

    def __str__(self):
        return str(self.filepaths)

    def _printer(self, message):
        """Prints message to console when console_output is True"""
        if self.console_output:
            print(message)

    def _get_filepaths(self):
        """Filters list of file paths to remove non-included, remove excluded files and concatenate full paths."""
        if self.to_include:
            self.filepaths = [path for path in self.filepaths
                              for inc in self.to_include
                              if inc in os.path.basename(Path(path))]
        if self.to_exclude:
            excludes = [path for path in self.filepaths
                        for ex in self.to_exclude
                        if ex in os.path.basename(Path(path))]
            self.filepaths = list(set(self.filepaths).difference(set(excludes)))
        if self.full_paths:
            self.filepaths = [os.path.join(self.directory, files) for files in self.filepaths]
        self._printer("\t" + str(len(self.filepaths)) + " file paths have passed filter checks.")
        return self.filepaths

    def walk(self):
        """
        This function will generate the file names in a directory tree by walking the tree either top-down or
        bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple
        (dirpath, dirnames, filenames).
        """
        count = Counter()
        for root, directories, files in os.walk(self.directory, topdown=self.topdown):
            root = root[len(str(self.directory))+1:]
            for filename in files:
                if not filename.startswith('.'):
                    # Join the two strings in order to form the full filepath.
                    self.filepaths.append(os.path.join(root, filename))
                    count.up
        self._printer("\t" + str(count.total) + " file paths have been parsed.")
        return self._get_filepaths()

    def files(self):
        """
        Return list of files in root directory
        """
        for path in os.listdir(self.directory):
            if os.path.isfile(os.path.join(self.directory, path)):
                if not path.startswith('.'):
                    self.filepaths.append(path)
        return self._get_filepaths()

    def folders(self):
        """
        Return list of folders in root directory
        """
        for path in os.listdir(self.directory):
            if os.path.isdir(os.path.join(self.directory, path)):
                if not path.startswith('.'):
                    self.filepaths.append(path)
        return self._get_filepaths()


class DirTree:
    def __init__(self, root, branches=None):
        """
        Generate a tree dictionary of the contents of a root directory.
        :param root: Starting directory
        :param branches: List of function tuples used for filtering
        """
        self.tree_dict = {}
        self.directory = Path(root)
        self.start = str(self.directory).rfind(os.sep) + 1
        self.branches = branches
        self.get()

    def __iter__(self):
        return iter(self.tree_dict.items())

    def __str__(self):
        return str(self.tree_dict)

    @property
    def dict(self):
        return self.tree_dict

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

    def get(self):
        """
        Generate path, dirs, files tuple for each path in directory.  Executes filters if branches are not None
        :return:
        """
        for path, dirs, files in os.walk(self.directory):
            folders = path[self.start:].split(os.sep)
            if self.branches:
                if self._filter(folders, 'folders'):
                    files = dict.fromkeys(files)
                    parent = reduce(dict.get, folders[:-1], self.tree_dict)
                    parent[folders[-1]] = files
            else:
                files = dict.fromkeys(files)
                parent = reduce(dict.get, folders[:-1], self.tree_dict)
                parent[folders[-1]] = files
        return self.tree_dict
