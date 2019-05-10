import os
import re


class Versions:
    def __init__(self, versions_list):
        """Sort and manipulate list of semver formatting versions."""
        self._versions_list = versions_list
        self._versions = None

    @property
    def versions(self):
        """Retrieve a dictionary of version part values from a list of versions."""
        if not self._versions:
            self._versions = {
                tag: {'major': int(tag.split('.', 2)[0]),
                      'minor': int(tag.split('.', 2)[1]),
                      'patch': int(tag.split('.', 2)[2] if '-' not in tag else tag.split('.', 2)[2].split('-', 1)[0]),
                      'cycle': '' if '-' not in tag else tag.split('.', 2)[2].split('-', 1)[1]}
                for tag in [s for s in self._versions_list if len(s) > 0 and not s.startswith('latest')]
            }
        return self._versions

    @property
    def sorted(self):
        """Sort a list of semver formatted versions by major, minor, path and cycle."""
        sort = [k for k, v in sorted(self.versions.items(),
                                     reverse=True,
                                     key=lambda kv: (kv[1]['major'], kv[1]['minor'], kv[1]['patch'], kv[1]['cycle']))]
        if 'latest' in self._versions_list:
            sort.insert(0, 'latest')
        return sort

    def latest(self):
        """Retrieve the latest version."""
        return self.sorted[0]


def get_version(source):
    """
    Retrieve the version of a python distribution.

    version_file default is the <project_root>/_version.py

    :param source: Path to project root
    :return: Version string
    """
    version_str_lines = open(os.path.join(source, os.path.basename(source), '_version.py'), "rt").read()
    version_str_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(version_str_regex, version_str_lines, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." % os.path.join(source, os.path.basename(source)))


def set_version(source):
    """
    Set the version of a python distribution.

    version_file default is the <project_root>/_version.py

    :param source: Path to project root
    :return: Version string
    """
    with open(os.path.join(source, os.path.basename(source), '_version.py'), "r+") as version_file:
        # Read existing version file
        version_str_lines = version_file.read()

        # Extract current version
        current_version = version_str_lines[version_str_lines.index("'") + 1:len(version_str_lines) - 2]
        parts = current_version.split('.')
        parts[-1] = str(int(parts[-1]) + 1)

        # Concatenate new version parts
        new_version = '.'.join(parts)

        # Write new version
        version_file.seek(0)
        version_file.truncate()
        version_file.write(version_str_lines.replace(current_version, new_version))
    return new_version
