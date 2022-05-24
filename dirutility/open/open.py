import os
import tempfile
from contextlib import contextmanager
from typing import Dict, Union, TextIO

from dirutility.error import InvalidAbsoluteDirectoryError
from dirutility.open.clazz import TempDir, TarFile, ZipFile


@contextmanager
def tempdir(absdirpath: str, prefix='', suffix='') -> TempDir:
    """
    Create and return a temporary directory.  This has the same
    behavior as mkdtemp but can be used as a context manager.  For
    example:

        with tempdir('/home/dirutility/temp', prefix='prefix_', suffix='_suffix') as tmpdir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.

    :param absdirpath:
    :param prefix:
    :param suffix:
    :return:
    :rtype: TempDir
    """
    with tempfile.TemporaryDirectory(prefix=prefix, suffix=suffix, dir=absdirpath) as tmpdir_path:
        if os.path.isabs(absdirpath) and os.path.isdir(absdirpath):
            dir_obj = TempDir(tmpdir_path)
            yield dir_obj
        else:
            raise InvalidAbsoluteDirectoryError(absdirpath)


@contextmanager
def tartempdir(
        absfilepath: str, tempdir: TempDir, mode: str = 'w:gz', temp: bool = True, force: bool = True) -> TarFile:
    """
    Create and return a tarfile directory.  This has the same
    behavior as mkdtemp then create tarfile from temp dir but can be used as a context manager.  For
    example:

        with tardir('/home/dirutility/temp/bac.tar', 'haha.tar') as tardir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.

    :param absfilepath: archive file create abs path
    :param tempdir: temporary directory object
    :param mode: tarfile mode
    :param temp: temporary file
    :param force: force create file
    :return:
    :rtype: TarFile
    """
    file_create_by_me = False
    try:
        if force:
            yield _create_archive(absfilepath, tempdir, mode)
            file_create_by_me = True
        elif not os.path.exists(absfilepath):
            yield _create_archive(absfilepath, tempdir, mode)
        else:
            raise FileExistsError(absfilepath)
    finally:
        if temp and file_create_by_me:
            os.remove(absfilepath)
        else:
            pass


def _create_archive(absfilepath, tempdir, mode) -> TarFile:
    """

    :param absfilepath:
    :param tempdir:
    :param mode:
    :return:
    """
    if mode.endswith('zip'):
        return ZipFile(absfilepath, tempdir, mode)
    else:
        return TarFile(absfilepath, tempdir, mode)


@contextmanager
def tardir(
        absfilepath: str, mode: str = 'w:gz', temp: bool = True, force: bool = True, withdir: bool = False,
        **paths: Dict[str, Union[dict, str, TextIO, None]]) -> TarFile:
    """
    Create and return a tarfile directory.  This has the same
    behavior as mkdtemp then create tarfile from temp dir but can be used as a context manager.  For
    example:

        with tardir('/home/dirutility/temp/bac.tar', 'haha.tar') as tardir:
            ...

    Upon exiting the context, the directory and everything contained
    in it are removed.

    :param absfilepath: archive file create abs path
    :param mode: tarfile mode
    :param temp: temporary file
    :param force: force create file
    :param withdir: if or not with dir in archive file
    :param paths: directory paths objects
    :return:
    :rtype: TarFile
    """
    absdirpath = absfilepath.rsplit('/', 1)[0]
    with tempdir(absdirpath) as temp_obj:
        temp_obj.create_structure(**paths)
        with tartempdir(absfilepath, temp_obj, mode=mode, temp=temp, force=force) as tar_obj:
            tar_obj.create_archive(withdir=withdir)
            yield tar_obj
