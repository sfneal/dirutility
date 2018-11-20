import os
import shutil
import platform
from pathlib import Path
from math import inf
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
from functools import reduce
from hashlib import md5
from datetime import datetime
from operator import itemgetter

from dirutility.walk.filter import PathFilters
from dirutility.walk.multiprocess import Sprinter
from dirutility.walk.sequential import Crawler
from looptools import Timer


class Printer:
    def __init__(self, console_output, console_stream):
        """Printer function initialized with classes. Used for optional printing"""
        self.console_output = console_output
        self.console_stream = console_stream

    def printer(self, message, stream=False):
        if not stream:
            if self.console_output:
                print('\t' + message)
        else:
            if self.console_stream:
                print('\t' + message)


def pool_process(func, iterable, process_name='Pool processing', cpus=cpu_count()):
    """
    Apply a function to each element in an iterable and return a result list.

    :param func: A function that returns a value
    :param iterable: A list or set of elements to be passed to the func as the singular parameter
    :param process_name: Name of the process, for printing purposes only
    :param cpus: Number of CPUs
    :return: Result list
    """
    with Timer('\t{0} ({1}) completed in'.format(process_name, str(func))):
        pool = Pool(cpus)
        vals = pool.map(func, iterable)
        pool.close()
    return vals


def md5_hash(file_path):
    """Open a file path and hash the contents."""
    with open(file_path, 'rb') as fp:
        return md5(fp.read()).hexdigest()


def md5_tuple(file_path):
    """Returns a file_path, hash tuple."""
    return file_path, md5_hash(file_path)


def pool_hash(path_list):
    """Pool process file hashing."""
    return pool_process(md5_tuple, path_list, 'MD5 hashing')


def remover(file_path):
    """Delete a file or directory path only if it exists."""
    if os.path.isfile(file_path):
        os.remove(file_path)
        return True
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
        return True
    else:
        return False


def creation_date(path_to_file, return_datetime=True):
    """
    Retrieve a file's creation date.

    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.

    See http://stackoverflow.com/a/39501288/1709587 for explanation.

    :param path_to_file: File path
    :param return_datetime: Bool, returns value in Datetime format
    :return: Creation date
    """
    if platform.system() == 'Windows':
        created_at = os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            created_at = stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            created_at = stat.st_mtime

    if return_datetime:
        return datetime.fromtimestamp(created_at)
    else:
        return created_at


def creation_date_tuple(file_path):
    """Returns a (file_path, creation_date) tuple."""
    return file_path, creation_date(file_path)


def pool_creation_date(path_list):
    """Pool process file creation dates."""
    return pool_process(creation_date_tuple, path_list, 'File creation dates')


class DirPaths:
    def __init__(self, directory, full_paths=False, topdown=True, to_include=None, to_exclude=None,
                 min_level=0, max_level=inf, filters=None, non_empty_folders=False, parallelize=False,
                 pool_size=cpu_count(), console_output=False, console_stream=False, hash_files=False):
        """
        This class generates a list of either files and or folders within a root directory.

        The walk method generates a directory list of files by walking the file tree top down or bottom up.  The
        files and folders method generate a list of files or folders in the top level of the  tree.

        :param directory: Starting directory file path
        :param full_paths: Bool, when true full paths are concatenated to file paths list
        :param topdown: Bool, when true walk method walks tree from the topdwon. When false tree is walked bottom up
        :param to_include: None by default.  List of filters acceptable to find within file path string return
        :param to_exclude: None by default.  List of filters NOT acceptable to return
        :param min_level: 0 by default.  Minimum directory level to save paths from
        :param max_level: Infinity by default.  Maximum directory level to save paths from
        :param parallelize: Bool, when true pool processing is enabled within walk method
        :param pool_size: Number of CPUs for pool processing, default is number of processors
        :param console_output: Bool, when true console output is printed
        :param console_stream: Bool, when true loops print live results
        :param hash_files: Bool, when true walk() method return a dictionary file_paths and hashes
        """
        self.timer = Timer()
        self.full_paths = full_paths
        self.topdown = topdown

        # Exclude .DS_Store by default, set to_exclude to False to include .DS_Store
        to_exclude = ['.DS_Store'] if to_exclude is None else to_exclude
        if any(i for i in [to_include, to_exclude, filters]) or min_level != 0 or max_level != inf:
            self.filters = PathFilters(to_include, to_exclude, min_level, max_level, filters, non_empty_folders)
        else:
            self.filters = False

        self.console_output = console_output
        self.console_stream = console_stream
        self._hash_files = hash_files

        self._printer = Printer(console_output, console_stream).printer
        self._printer('DIRPATHS')

        # Check that parallelization is enabled
        if parallelize:
            self.pool_size = pool_size
        self.parallelize = parallelize
        self.filepaths = []

        # Check if directory is a singular (1) string or if it is a list of strings (multiple)
        try:
            self.directory = [str(directory)]
        except TypeError:
            self.directory = [str(dirs) for dirs in directory]

    def __iter__(self):
        return iter(list(self.filepaths))

    def __str__(self):
        return str(self.filepaths)

    def __len__(self):
        return len(self.filepaths)

    def _get_filepaths(self):
        """Filters list of file paths to remove non-included, remove excluded files and concatenate full paths."""
        self._printer(str(self.__len__()) + " file paths have been parsed in " + str(self.timer.end))
        if self._hash_files:
            return pool_hash(self.filepaths)
        else:
            return self.filepaths

    def creation_dates(self, sort=True):
        """
        Return a list of (file_path, creation_date) tuples created from list of walked paths.

        :param sort: Bool, sorts file_paths on created_date from newest to oldest.
        :return: List of (file_path, created_date) tuples.
        """
        if not sort:
            return pool_creation_date(self.filepaths)
        else:
            pcd = pool_creation_date(self.filepaths)
            pcd.sort(key=itemgetter(1), reverse=True)
            return pcd

    def walk(self):
        """
        Default file path retrieval function.
        sprinter() - Generates file path list using pool processing and Queues
        crawler() - Generates file path list using os.walk() in sequence
        """
        if self.parallelize:
            self.filepaths = Sprinter(self.directory, self.filters, self.full_paths, self.pool_size, self._printer).sprinter()
        else:
            self.filepaths = Crawler(self.directory, self.filters, self.full_paths, self.topdown, self._printer).crawler()
        return self._get_filepaths()

    def files(self):
        """Return list of files in root directory"""
        self._printer('\tFiles Walk')
        for directory in self.directory:
            for path in os.listdir(directory):
                full_path = os.path.join(directory, path)
                if os.path.isfile(full_path):
                    if not path.startswith('.'):
                        self.filepaths.append(full_path)
        return self._get_filepaths()

    def folders(self):
        """Return list of folders in root directory"""
        for directory in self.directory:
            for path in os.listdir(directory):
                full_path = os.path.join(directory, path)
                if os.path.isdir(full_path):
                    if not path.startswith('.'):
                        self.filepaths.append(full_path)
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


def gui():
    from dirutility.gui import WalkGUI
    gui = WalkGUI()
    params = gui.parsing()
    parse = params['parse']

    paths = DirPaths(parse['directory'], console_stream=parse['console_stream'], parallelize=parse['parallelize'],
                     max_level=parse['max_level'], non_empty_folders=parse['non_empty_folders']).walk()

    if params['save']:
        from databasetools import CSVExport, DictTools
        save = params['save']
        if save['csv']:
            CSVExport(list(paths), cols=['files'], file_path=save['directory'],
                      file_name=os.path.basename(parse['directory']))
        if save['json']:
            DictTools(save['directory'], os.path.basename(parse['directory'])).save(list(paths))
    print('Done!')


if __name__ == "__main__":
    gui()
