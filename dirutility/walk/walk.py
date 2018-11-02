import os
import shutil
from pathlib import Path
from math import inf
from multiprocessing.pool import Pool
from multiprocessing import cpu_count
from functools import reduce
from hashlib import md5

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


def md5_hash(file_path):
    """Open a file path and hash the contents."""
    with open(file_path, 'rb') as fp:
        return md5(fp.read()).hexdigest()


def md5_tuple(file_path):
    """Returns a file_path, hash tuple."""
    return file_path, md5_hash(file_path)


def pool_hash(path_list):
    """Pool process file hashing."""
    with Timer('\tMD5 hashing completed in'):
        pool = Pool(cpu_count())
        vals = pool.map(md5_tuple, path_list)
        pool.close()
    return vals


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
