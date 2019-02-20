# Copies an entire folder and its contents into a zip file whose filename increments.
import os
import shutil
from zipfile import ZipFile
from tqdm import tqdm
from dirutility import DirPaths


class ZipBackup:
    def __init__(self, source, destination=None, compress_level=0, delete_source=False, overwrite=False):
        """
        Create zip file backup of a directory.

        Backup the entire contents of "source" into a zip file.
        or
        Backup all "source" files to destination zip file.

        :param source: Source folder path or iterable of paths
        :param destination: Defaults source parent directory
        :param compress_level: Compression level
        """
        # TODO: Add multiprocessing support
        self.compress_level = compress_level
        self.delete_source = delete_source
        self.overwrite = overwrite
        self.source, self.zip_filename = self._set_paths(source, destination)

    def __call__(self, *args, **kwargs):
        self.backup()
        return self.zip_filename

    def __str__(self):
        return self.zip_filename

    @staticmethod
    def _resolve_file_name(source, destination):
        """Create a filename for the destination zip file."""
        number = 1
        if os.path.exists(os.path.join(destination, os.path.basename(source) + '.zip')):
            while True:
                zip_filename = os.path.join(destination, os.path.basename(source) + '_' + str(number) + '.zip')
                if not os.path.exists(zip_filename):
                    break
                number = number + 1
        else:
            zip_filename = os.path.join(destination, os.path.basename(source) + '.zip')
        return zip_filename

    def _set_paths(self, source, destination):
        # make sure folder is absolute
        source = os.path.abspath(source)

        # Set destination to next to source folder if not manually set
        if not destination:
            destination = os.path.dirname(source)

        # Create new file_name
        if not self.overwrite:
            zip_filename = self._resolve_file_name(source, destination)
        else:
            zip_filename = os.path.join(destination, os.path.basename(source) + '.zip')
            if os.path.exists(zip_filename):
                os.remove(zip_filename)

        return source, zip_filename

    def _get_paths(self):
        return DirPaths(self.source, full_paths=True).walk()

    def _backup_compresslevel(self, dirs):
        """Create a backup file with a compresslevel parameter."""
        # Only supported in Python 3.7+
        with ZipFile(self.zip_filename, 'w', compresslevel=self.compress_level) as backup_zip:
            for path in tqdm(dirs, desc='Writing Zip Files', total=len(dirs)):
                backup_zip.write(path, path[len(self.source):len(path)])

    def _backup_pb_gui(self, dirs):
        """Create a zip backup with a GUI progress bar."""
        import PySimpleGUI as sg
        # Legacy support
        with ZipFile(self.zip_filename, 'w') as backup_zip:
            for count, path in enumerate(dirs):
                backup_zip.write(path, path[len(self.source):len(path)])
                if not sg.OneLineProgressMeter('Writing Zip Files', count + 1, len(dirs) - 1, 'Files'):
                    break

    def _backup_pb_tqdm(self, dirs):
        """Create a backup with a tqdm progress bar."""
        with ZipFile(self.zip_filename, 'w') as backup_zip:
            for path in tqdm(dirs, desc='Writing Zip Files', total=len(dirs)):
                backup_zip.write(path, path[len(self.source):len(path)])

    def backup(self, paths=None):
        """Backup method driver."""
        if not paths:
            paths = self._get_paths()

        try:
            self._backup_compresslevel(paths)
        except TypeError:
            try:
                self._backup_pb_gui(paths)
            except ImportError:
                self._backup_pb_tqdm(paths)

        # Delete source if specified
        if self.delete_source:
            shutil.rmtree(self.source)
        return self.zip_filename


def main():
    try:
        from dirutility.gui import BackupZipGUI
        root = BackupZipGUI().source
        ZipBackup(root).backup()
    except ImportError:
        print('**pip install PySimpleGUI to run BackupZipGUI module**')
        from argparse import ArgumentParser

        # Declare argparse argument descriptions
        usage = 'ZipBackup your files'
        description = 'Create a zip backup of a file or directory.'
        helpers = {
            'files': "Input paths you would like to zip",
        }

        # construct the argument parse and parse the arguments
        ap = ArgumentParser(usage=usage, description=description)
        ap.add_argument('files', help=helpers['files'], nargs='+')
        args = vars(ap.parse_args())

        for f in args['files']:
            ZipBackup(f).backup()


if __name__ == "__main__":
    main()
