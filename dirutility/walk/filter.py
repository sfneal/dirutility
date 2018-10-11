import os


class PathFilters:
    def __init__(self, to_include=None, to_exclude=None, min_level=0, max_level=12, filters=None,
                 non_empty_folders=None):
        self.to_include = to_include
        self.to_exclude = to_exclude
        self.min_level = min_level
        self.max_level = max_level
        self.filters = filters
        self.non_empty_folders = non_empty_folders

    @staticmethod
    def get_level(path):
        return len(path.split(os.sep))

    def check_level(self, path):
        # Check that current path level is more than min path and less than max path
        if self.min_level <= self.get_level(path) <= self.max_level:
            return True

    def _level_filters(self, path):
        path_list = path.split(os.sep)
        for i in range(0, len(path_list)):
            if i in self.filters:
                if 'exclude' in self.filters[i]:
                    if any(ex.lower() in path_list[i].lower() for ex in self.filters[i]['exclude']):
                        return False

                if 'include' in self.filters[i]:
                    inclusion = 0
                    for inc in self.filters[i]['include']:
                        if str(inc).lower() in path_list[i].lower():
                            inclusion = 1
                    if inclusion != 1:
                        return False
        return True

    def validate_non_empty_folder(self, base, fullname):
        # Check that path is a directory
        if os.path.isdir(base + os.sep + fullname):
            # Check that path is not empty
            if os.listdir(base + os.sep + fullname):
                # Check that path level is equal to max_level
                if self.filters.get_level(fullname) == self.filters.max_level:
                    return True

    def validate(self, path):
        """Run path against filter sets and return True if all pass"""
        # Exclude hidden files and folders with '.' prefix
        if os.path.basename(path).startswith('.'):
            return False

        # Check that current path level is more than min path and less than max path
        if not self.check_level(path):
            return False

        if self.filters:
            if not self._level_filters(path):
                return False

        # Force include and exclude iterations to be strings in case of integer filters
        # Handle exclusions
        if self.to_exclude:
            if any(str(ex).lower() in path.lower() for ex in self.to_exclude):
                return False

        # Handle inclusions
        if self.to_include:
            if not any(str(inc).lower() in path.lower() for inc in self.to_include):
                return False

        return True
