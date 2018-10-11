# Copies an entire folder and its contents into a zip file whose filename increments.
import os
from zipfile import ZipFile
from tqdm import tqdm
from dirutility import DirPaths
from looptools import Timer


class ZipBackup:
    def __init__(self, source, destination=None):
        """
        Create zip file backup of a directory.
        :param source: Source folder path
        :param destination: Defaults source parent directory
        :param print_output: Prints directories parsed to console
        """
        self.source, self.zip_filename = self._set_paths(source, destination)
        self.backup()

    @staticmethod
    def _set_paths(source, destination):
        # Backup the entire contents of "folder" into a zip file.
        source = os.path.abspath(source)  # make sure folder is absolute

        # Set destination to next to source folder if not manually set
        if not destination:
            destination = os.path.dirname(source)

        # Figure out the filename
        number = 1
        if os.path.exists(os.path.join(destination, os.path.basename(source) + '.zip')):
            while True:
                zip_filename = os.path.join(destination, os.path.basename(source) + '_' + str(number) + '.zip')
                if not os.path.exists(zip_filename):
                    break
                number = number + 1
        else:
            zip_filename = os.path.join(destination, os.path.basename(source) + '.zip')
        return source, zip_filename

    def _get_dirs(self):
        return DirPaths(self.source, full_paths=True).walk()

    def backup(self):
        dirs = self._get_dirs()
        with ZipFile(self.zip_filename, 'w') as backup_zip:
            for path in tqdm(dirs, desc='Writing Zip Files', total=len(dirs)):
                backup_zip.write(path, path[len(self.source):len(path)])


def main():
    from dirutility.gui import BackupZipGUI
    root = BackupZipGUI().source
    with Timer():
        ZipBackup(root)


if __name__ == "__main__":
    main()
