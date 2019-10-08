from __future__ import annotations

import abc
import os
import tarfile
from typing import Union, Dict, TextIO, List

from dirutility.error import InvalidFileNameError, InvalidDirStructureError


class DirStructure:
    def __init__(self, **paths: Dict[str, Union[dict, str, TextIO, None]]):
        self._content = {}
        for pathname, _c in paths.items():
            if isinstance(_c, dict):
                self._content[pathname] = DirStructure(**_c)
            else:
                self._content[pathname] = _c

    @property
    def content(self):
        return self._content.copy()

    @property
    def dirsname(self) -> List[str]:
        res = list(self._content.keys())
        res.sort()
        return res

    def _is_filename_valid(self, filename):
        if isinstance(filename, str) and filename.strip():
            return True
        else:
            return False

    def validate_filename(self, filename):
        if not self._is_filename_valid(filename):
            raise InvalidFileNameError(filename)

    def create(self, prefix_dir: str):
        for filename, _c in self._content.items():
            self.validate_filename(filename)
            path = '{}/{}'.format(prefix_dir, filename)
            if _c is None:
                fd = open(path, 'w')
                fd.close()
            if isinstance(_c, str):
                with open(path, 'w') as fd:
                    fd.write(_c)
            elif isinstance(_c, dict):
                os.mkdir(path)
            elif isinstance(_c, DirStructure):
                os.mkdir(path)
                _c.create(path)
            else:
                with open(path, 'w') as fd:
                    for _l in _c:
                        fd.write(_l)


class DirBase(metaclass=abc.ABCMeta):
    def __init__(self, dirpath: str, structure: Union[DirStructure, None] = None):
        self._dirpath = dirpath
        self._structure = structure

    @property
    def dirname(self) -> str:
        return self.dirpath.rsplit('/', 1)[1]

    @property
    def dirpath(self) -> str:
        return self._dirpath

    def dirs(self, relative=True) -> List[str]:
        if relative:
            return self._structure.dirsname
        else:
            return ['{}/{}'.format(self._dirpath, _name) for _name in self._structure.dirsname]

    def create_structure(self, **paths: Dict[str, Union[dict, str, TextIO, None]]):
        self._structure = DirStructure(**paths)
        self._structure.create(self._dirpath)


class TempDir(DirBase):
    pass


class TarFile(object):
    def __init__(self, filepath: str, tempdir: TempDir, mode: str = 'w:gz'):

        self._mode = mode.strip()
        _ar = self._mode.split(':')
        if len(_ar) > 0 and _ar[-1].strip():
            self._compress_type = _ar[-1].strip()
        else:
            self._compress_type = None
        self._filepath = filepath.strip()
        self._validate_filename(self._filepath)
        self._tempdir = tempdir

    def _is_filename_valid(self, filename):
        if filename.endswith(self._compress_type):
            return True
        else:
            return False

    def _validate_filename(self, filename):
        if not self._is_filename_valid(filename):
            raise InvalidFileNameError(filename)

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def tempdir(self) -> TempDir:
        return self._tempdir

    def create_tarfile(self):
        with tarfile.open(self._filepath, mode=self._mode) as tar:
            for dirpath, dirname in zip(self._tempdir.dirs(relative=False), self._tempdir.dirs()):
                tar.add(dirpath, arcname=dirname, recursive=True)
