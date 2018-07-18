from tqdm import tqdm
from dirutility import DirPaths
from databasetools import DictTools


def unique(list1, list2):
    """
    Get unique items in list1 that are not in list2
    :return: Unique items only in list 1
    """
    set2 = set(list2)
    list1_unique = [x for x in tqdm(list1, desc='List 1 Uniques', total=len(list1)) if x not in set2]
    return list1_unique


def unique_venn(list1, list2):
    """Get unique items that are only in list1 and only in list2"""
    return unique(list1, list2), unique(list2, list1)


def compare_trees(dir1, dir2):
    paths1 = DirPaths(dir1).walk()
    paths2 = DirPaths(dir2).walk()
    return unique_venn(paths1, paths2)


if __name__ == '__main__':
    dir1 = '/Users/Stephen/Users'
    dir2 = '/Users/Stephen/Users 2'
    list1, list2 = compare_trees(dir1, dir2)
    DictTools('/Users/Stephen', 'list1').save(list1)
    DictTools('/Users/Stephen', 'list2').save(list2)