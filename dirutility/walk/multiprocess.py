import os
from multiprocessing.pool import Pool
from multiprocessing import Manager


class Sprinter:
    def __init__(self, directory, filters, full_paths, pool_size, _printer):
        """DirPaths sub class for directory parsing using parallel processing."""
        self.directory = directory
        self.filters = filters
        self.pool_size = pool_size
        self._printer = _printer

        if self.filters:
            self._printer('Filtering enabled')
            self.explore_path = self.explore_path_filter
        else:
            self._printer('Filtering disabled')
            self.explore_path = self.explore_path_encompass

        self.filepaths = Manager().list()
        self.unsearched = Manager().Queue()

        if full_paths:
            self._printer('Absolute paths')
            self.add_path = self._add_filepath_absolute
        else:
            self._printer('Relative paths')
            self.add_path = self._add_filepath_relative

    def __iter__(self):
        return iter(self.filepaths)

    def __len__(self):
        return len(self.filepaths)

    def _add_filepath_relative(self, paths):
        for directory, fullname in paths:
            self.filepaths.append(fullname)

    def _add_filepath_absolute(self, paths):
        for directory, fullname in paths:
            self.filepaths.append(os.path.join(directory, fullname))

    def _get_root_files(self, directory):
        """Retrieve files within the root directory"""
        if len(self.filepaths) is 0:
            if self.filters:
                root_files = [(directory, f) for f in os.listdir(directory)
                              if os.path.isfile(os.path.join(directory, f))
                              and self.filters.validate(f)
                              and self.filters.get_level(f) == self.filters.max_level]
            else:
                root_files = [(directory, f) for f in os.listdir(directory)
                              if os.path.isfile(os.path.join(directory, f))]
            self.add_path(root_files)

    def explore_path_filter(self, task_num, dirpath):
        """
        Explore path to discover unsearched directories and save filepaths
        :param task_num: Processor ID
        :param dirpath: Tuple (base directory, path), path information pulled from unsearched Queue
        :return: Directories to add to unsearched Queue
        """
        base, path = dirpath
        directories = []
        nondirectories = []
        if self.filters.validate(path):
            self._printer("Task: " + str(task_num) + " >>> Explored path: " + path, stream=True)
            # Loop through paths
            for filename in os.listdir(base + os.sep + path):
                fullname = os.path.join(path, filename)
                if self.filters.validate(fullname):
                    # Check that non-empty folders flag is on and we're at the max directory level
                    if self.filters.non_empty_folders and self.filters.get_level(fullname) == self.filters.max_level:
                        # Check that the path is not an empty folder
                        if os.path.isdir(base + os.sep + fullname):
                            # Get paths in folder without walking directory
                            paths = os.listdir(base + os.sep + fullname)

                            # Check that any of the paths are files and not just directories
                            if paths and any(os.path.isfile(os.path.join(base, fullname, p)) for p in paths):
                                nondirectories.append((base, fullname))
                    else:
                        # Append to directories if dir
                        if os.path.isdir(base + os.sep + fullname):
                            directories.append((base, fullname))
                        # Pass filters and append to nondirectories if file
                        elif self.filters.validate(fullname):
                            nondirectories.append((base, fullname))
            self.add_path(nondirectories)
        return directories

    def explore_path_encompass(self, task_num, dirpath):
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
            else:
                nondirectories.append((base, fullname))
        self.add_path(nondirectories)
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
            dirs = self.explore_path(task_num, (base, path))
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
        self._printer('Multiprocess Walk')
        # Loop through directories in case there is more than one (1)
        for directory in self.directory:
            self._get_root_files(directory)  # Add file within root directory if filepaths is empty
            # acquire the list of paths
            first_level_dirs = next(os.walk(directory))[1]
            for path in first_level_dirs:
                self.unsearched.put((directory, path))
        self._printer('Pool Processing STARTED')
        pool = Pool(self.pool_size)
        pool.map_async(self.parallel_worker, range(self.pool_size))
        pool.close()
        self.unsearched.join()
        self._printer('Pool Processing ENDED')
        return self.filepaths
