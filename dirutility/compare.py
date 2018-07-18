from tqdm import tqdm
from dirutility import DirPaths


def unique(list1, list2):
    """
    Get unique items in list1 that are not in list2
    :return: Unique items only in list 1
    """
    set2 = set(list2)
    list1_unique = [x for x in tqdm(list1, desc='Unique', total=len(list1)) if x not in set2]
    return list1_unique


def unique_venn(list1, list2):
    """Get unique items that are only in list1 and only in list2"""
    return unique(list1, list2), unique(list2, list1)


def compare_trees(dir1, dir2):
    """Parse two directories and return lists of unique files"""
    paths1 = DirPaths(dir1).walk()
    paths2 = DirPaths(dir2).walk()
    return unique_venn(paths1, paths2)


def main():
    from dirutility.gui import CompareTreesGUI
    params = CompareTreesGUI().sources
    src = params['source']
    dir1_u, dir2_u = compare_trees(src['dir1'], src['dir2'])

    if params['save']:
        from databasetools import CSVExport, DictTools
        save = params['save']
        if save['csv']:
            CSVExport(list(dir1_u), cols=['files'], file_path=save['directory'], file_name='dir1_unique')
            CSVExport(list(dir2_u), cols=['files'], file_path=save['directory'], file_name='dir2_unique')
        if save['json']:
            DictTools(save['directory'], 'dir1_unique').save(list(dir1_u))
            DictTools(save['directory'], 'dir2_unique').save(list(dir2_u))
    print('Done!')


if __name__ == "__main__":
    main()
