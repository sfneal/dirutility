from tqdm import tqdm


def unique(list1, list2):
    """
    Get unique items in two lists.
    :return: List1, list2 tuple containing the unique values from each list
    """
    set1 = set(list1)
    set2 = set(list2)

    list1_unique = [x for x in tqdm(list1, desc='List 1 Uniques', total=len(list1)) if x not in set2]
    list2_unique = [x for x in tqdm(list2, desc='List 2 Uniques', total=len(list2)) if x not in set1]

    return list1_unique, list2_unique
