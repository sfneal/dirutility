import os
from pathlib import Path
from math import inf
from multiprocessing.pool import Pool
from multiprocessing import Manager
from multiprocessing import cpu_count
from functools import reduce
from looptools import Counter


class DirPaths:
    def __init__(self, directory, full_paths=False, topdown=True, to_include=None, to_exclude=None,
                 min_level=0, max_level=inf, only_files=False, only_folders=False, parallelize=False,
                 pool_size=cpu_count(), console_output=False, console_stream=False):
        """
        This class generates a list of either files and or folders within a root directory.  The walk method
        generates a directory list of files by walking the file tree top down or bottom up.  The files and folders
        method generate a list of files or folders in the top level of the tree.
        :param directory: Starting directory file path
        :param full_paths: Bool, when true full paths are concatenated to file paths list
        :param topdown: Bool, when true walk method walks tree from the topdwon. When false tree is walked bottom up
        :param to_include: None by default.  List of filters acceptable to find within file path string return
        :param to_exclude: None by default.  List of filters NOT acceptable to return
        :param min_level: 0 by default.  Minimum directory level to save paths from
        :param max_level: Infinity by default.  Maximum directory level to save paths from
        :param only_files: Bool, when true only files in the root directory are returned
        :param only_folders: Bool, when true only folders in the root directort are returned
        :param parallelize: Bool, when true pool processing is enabled within walk method
        :param pool_size: Number of CPUs for pool processing, default is number of processors
        :param console_output: Bool, when true console output is printed
        :param console_stream: Bool, when true loops print live results
        """
        self.full_paths = full_paths
        self.topdown = topdown
        self.to_include = to_include
        self.to_exclude = to_exclude
        self.min_level = min_level
        self.max_level = max_level
        self.console_output = console_output
        self.console_stream = console_stream

        # Check that parallelization is enabled
        if parallelize:
            self.parallelize = True
            self.pool_size = pool_size
            self.filepaths = Manager().list()
            self.unsearched = Manager().Queue()
        else:
            self.parallelize = False
            self.filepaths = []

        # Check if files only or folders only params have been set
        if only_files and not only_folders:
            func = self.files
        elif only_folders and not only_files:
            func = self.folders
        else:
            func = self.walk

        # Check if directory is a singular (1) string or if it is a list of strings (multiple)
        try:
            if os.path.isdir(directory):
                self.directory = [str(directory)]
        except TypeError:
            self.directory = [str(dirs) for dirs in directory]

        func()  # Run declared function

        self._printer("\t" + str(self.__len__()) + " file paths have been parsed.")
        self._get_filepaths()  # Return filepaths

    def __iter__(self):
        return iter(self.filepaths)

    def __str__(self):
        return str(self.filepaths)

    def __len__(self):
        return len(self.filepaths)

    def _printer(self, message, stream=False):
        """Prints message to console when console_output is True"""
        if not stream:
            if self.console_output:
                print(message)
        else:
            if self.console_stream:
                print(message)

    def _get_filepaths(self):
        """Filters list of file paths to remove non-included, remove excluded files and concatenate full paths."""
        if self.full_paths:
            self.filepaths = [os.path.join(base, path) for base, path in self.filepaths]
        else:
            self.filepaths = [path for base, path in self.filepaths]
        self._printer("\t" + str(len(self.filepaths)) + " file paths have passed filter checks.")
        return self.filepaths

    @staticmethod
    def _get_level(path):
        return len(path.split(os.sep))

    def _check_level(self, path):
        if self.min_level <= self._get_level(path) <= self.max_level:
            return True
        else:
            return False

    def _apply_filters(self, path):
        """Ryb path against filter sets and return True if all pass"""
        # Check that current path is within level limitation
        if not self._check_level(path):
            return False

        # Exclude hidden files and folders with '.' prefix
        if os.path.basename(path).startswith('.'):
            return False

        # Handle exclusions
        if self.to_exclude:
            if any(ex in path for ex in self.to_exclude):
                return False

        # Handle inclusions
        if self.to_include:
            if not any(inc in path for inc in self.to_include):
                return False

        return True

    def _parallel_get_root_files(self, directory):
        """Retrive files within the root directory"""
        if len(self.filepaths) is 0:
            root_files = [(directory, f) for f in os.listdir(directory)
                          if os.path.isfile(os.path.join(directory, f))
                          and self._apply_filters(f)]
            self.filepaths.extend(root_files)

    def parallel_explore_path(self, task_num, dirpath):
        """
        Explore path to discover unsearched directories and save filepaths
        :param task_num: Processor ID
        :param dirpath: Tuple (base directory, path), path information pulled from unsearched Queue
        :return: Directories to add to unsearched Queue
        """
        base, path = dirpath
        directories = []
        nondirectories = []
        self._printer("Task: " + str(task_num) + " >>> Explored path: " + path, stream=True)
        # Loop through paths
        for filename in os.listdir(base + os.sep + path):
            fullname = os.path.join(path, filename)
            # Append to directories if dir
            if os.path.isdir(base + os.sep + fullname):
                directories.append((base, fullname))
            # Pass filters and append to nondirectories if file
            elif self._apply_filters(fullname):
                nondirectories.append((base, fullname))
        self.filepaths.extend(nondirectories)
        return directories

    def parallel_worker(self, task_num):
        """
        Continuously pulls directories from the Queue until it is empty.
        Gets child directories from parent and adds them to Queue.
        Executes task_done() to remove directory from unsearched Queue
        :param task_num: Processor ID
        """
        while True:
            base, path = self.unsearched.get()
            dirs = self.parallel_explore_path(task_num, (base, path))
            for newdir in dirs:
                self.unsearched.put(newdir)
            self.unsearched.task_done()

    def sprinter(self):
        """
        Called when parallelize is True.
        This function will generate the file names in a directory tree by adding directories to a Queue and
        continuously exploring directories in the Queue until Queue is emptied.
        Significantly faster than crawler method for larger directory trees.
        """
        self._printer('\tMultiprocess Walk')
        # Loop through directories in case there is more than one (1)
        for directory in self.directory:
            self._parallel_get_root_files(directory)  # Add file within root directory if filepaths is empty
            # acquire the list of paths
            first_level_dirs = next(os.walk(directory))[1]
            for path in first_level_dirs:
                self.unsearched.put((directory, path))
        pool = Pool(self.pool_size)
        pool.map_async(self.parallel_worker, range(self.pool_size))
        pool.close()
        self.unsearched.join()

    def crawler(self):
        """
        Called when parallelize is False.
        This function will generate the file names in a directory tree by walking the tree either top-down or
        bottom-up. For each directory in the tree rooted at directory top (including top itself), it yields a 3-tuple
        (dirpath, dirnames, filenames).
        """
        self._printer('\tStandard Walk')
        count = Counter(length=3)
        for directory in self.directory:
            for root, directories, files in os.walk(directory, topdown=self.topdown):
                root = root[len(str(directory)) + 1:]
                self._printer(str(count.up) + ": Explored path - " + str(root), stream=True)
                for filename in files:
                    fullname = os.path.join(root, filename)
                    if self._apply_filters(fullname):
                        # Join the two strings in order to form the full filepath.
                        self.filepaths.append((directory, fullname))

    def walk(self):
        """
        Default file path retrieval function.
        sprinter() - Generates file path list using pool processing and Queues
        crawler() - Generates file path list using os.walk() in sequence
        """
        if self.parallelize:
            self.sprinter()
        else:
            self.crawler()

    def files(self):
        """
        Return list of files in root directory
        """
        self._printer('\tFiles Walk')
        for directory in self.directory:
            for path in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, path)):
                    if not path.startswith('.'):
                        self.filepaths.append((directory, path))

    def folders(self):
        """
        Return list of folders in root directory
        """
        for directory in self.directory:
            for path in os.listdir(directory):
                if os.path.isdir(os.path.join(directory, path)):
                    if not path.startswith('.'):
                        self.filepaths.append((directory, path))


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
