import os
import shutil
from tqdm import tqdm
from pathlib import Path
from dirutility.walk import DirPaths


class FlattenTree:
    def __init__(self, directory, target='root'):
        """
        Loops through parent folders in a root directory and moves child files out of sub folders and into parent folder
        :param root: Starting directory
        :param target: Target destination for files.  Default is 'directory' which will move files into corresponding
        directory under parent root.  If set to 'root' then files will be moved into root folder
        """
        self.directory = directory
        self.target = target
        self.root_paths = [Path(self.directory + os.sep + dirs) for dirs in os.listdir(self.directory)]
        self.flatten()

    @staticmethod
    def remove_path_dirname(path):
        """
        Removes file paths directory if the directory is empty
        :param path: Filepath
        """
        dir_to_remove = os.path.dirname(path)
        if not os.listdir(dir_to_remove):
            shutil.rmtree(dir_to_remove)
        else:
            if len(os.listdir(dir_to_remove)) == 1:
                if os.listdir(dir_to_remove)[0].startswith('.'):
                    shutil.rmtree(dir_to_remove)

    def flatten(self):
        for dirs in tqdm(self.root_paths, desc='Flattening file tree', total=len(self.root_paths)):
            files = DirPaths(dirs)
            for f in files:
                if self.target == 'directory':
                    shutil.move(f, dirs)
                    self.remove_path_dirname(f)

                elif self.target == 'root':
                    shutil.move(f, self.directory)
                    self.remove_path_dirname(f)
                    self.remove_path_dirname(os.path.dirname(f))


class CreateTree:
    """
    Create file tree from directory of indexed files
    :param root: Starting directory
    :param delimiter: Character separating filename attributes
    :param prefix: Prefix string to be concatenated with lowest level folder
    :param suffix: Suffix string to be concatenated with lowest level folder
    """

    def __init__(self, root, delimiter="_", prefix=None, suffix=None):
        self.files = DirPaths(root).files()
        self.delimiter = delimiter
        self.prefix = prefix
        self.suffix = suffix
        self.create()

    def rename(self, path):
        split = os.path.basename(path).split(self.delimiter)[:-1]
        if self.prefix:
            split[-1] = self.prefix + self.delimiter + split[-1]
        if self.suffix:
            split[-1] = split[-1] + self.delimiter + self.suffix
        return split

    def create(self):
        # Generate lists of files and folders in root directory
        for path in self.files:
            child_dirs = self.rename(path)
            directory = os.path.dirname(path)
            for each in child_dirs:
                directory = os.path.join(directory, each)
                if not os.path.isdir(directory):
                    os.mkdir(directory)
            shutil.move(path, directory)


def move_files_to_folders(directory):
    """
    Loops through a parent directory and nests files within folders that already exists and have matching prefixs
    :param directory: Starting directory
    """
    # Generate lists of files and folders in root directory
    files, folders, files_to_move = [], [], []
    for path in os.listdir(directory):
        if os.path.isdir(path):
            folders.append(path)
        elif os.path.isfile(path):
            files.append(path)

    # Loop through folders in root directory
    for path in folders:
        # Generate list of files with same prefix as current folder
        child_files = [f for f in files if f.startswith(path)]
        files_to_move.append((path, child_files))

    # Move child files into parent folder
    for each in files_to_move:
        folder, files = each
        for f in files:
            shutil.move(f, folder)
