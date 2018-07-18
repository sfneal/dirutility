# Copies an entire folder and its contents into a zip file whose filename increments.
import os
from zipfile import ZipFile
from tqdm import tqdm
from dirutility import DirPaths
from looptools import ActiveTimer


class ZipBackup:
    def __init__(self, source, destination=None, print_output=False):
        """
        Create zip file backup of a directory.
        :param source: Source folder path
        :param destination: Defaults source parent directory
        :param print_output: Prints directories parsed to console
        """
        self.source, self.zip_filename = self._set_paths(source, destination)
        self.dirs = self._get_dirs(print_output)
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
        while True:
            zip_filename = os.path.join(destination, os.path.basename(source) + '_' + str(number) + '.zip')
            if not os.path.exists(zip_filename):
                break
            number = number + 1
        return source, zip_filename

    def _get_dirs(self, print_output):
        print('Parsing %s...' % self.source)
        return list(DirPaths(self.source, full_paths=True, console_stream=print_output).walk())

    def backup(self):
        print('Creating %s...' % self.zip_filename)
        backup_zip = ZipFile(self.zip_filename, 'w')
        self._write_zip(backup_zip)
        backup_zip.close()
        print('Done.')

    def _write_zip(self, backup_zip):
        for paths in tqdm(self.dirs, desc='Writing Zip Files', total=len(self.dirs)):
            backup_zip.write(paths)


def main():
    from dirutility.gui import BackupZipGUI
    root = BackupZipGUI().source
    with ActiveTimer(ZipBackup):
        ZipBackup(root)


if __name__ == "__main__":
    main()
