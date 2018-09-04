from dirutility import DirPaths
from databasetools import DictTools
import time
from looptools.timer import ActiveTimer


def test_case(case):
    test_cases = {
        'projects': {
            'rootpath': '/Volumes/Storage/HPA Design',
            'exclude': ['20080081_Rosenfeld_Realty',
                        '20080082_Clarewood_Homes_WEB',
                        '20080083_Dipersio_WEB',
                        '20080084_Olivieri',
                        '20080085_Greymont',
                        '20080086_Colonial_Builders',
                        '20080087_Jolin_Corporation_WEB',
                        '20080088_Atlantic_Construction_',
                        '20080089_Mariner_Development_WEB',
                        '20080090_Marinella_Construction',
                        '20080091_Homestead_Construction_WEB'],
            'include': ['20080094_Meadowfield_WEB',
                        '20080095_Marinella_Construction',
                        '20080096_Rosenfeld_Realty',
                        '20080097_Atlantic_Construction_']
        },
        'projects2': {
            'rootpath': '/Volumes/Storage/HPA Design',
            'exclude': None,
            'include': None
        },
        'projects3': {
            'rootpath': '/Volumes/Storage II/HPA Design/Projects/2008',
            'exclude': None,
            'include': None
        },
    }

    return test_cases[case]['rootpath'], test_cases[case]['exclude'], test_cases[case]['include']


if __name__ == "__main__":
    save = '/Users/Stephen/Desktop'
    iters = 1
    root = "/Volumes/Projects"
    root = "/Volumes/Storage II/HPA Design/Projects"

    max_level = 3
    to_exclude = ['.xls', '.doc']
    years = set(range(2007, 2008))
    filters = {
        0: {'include': years,
            'exclude': {'prism'}},
        1: {'exclude': {'temp projects', 'temp', 'temps', 'copy of temp folder', 'new project folders', 'new folder',
                        'al bonfilio', 'new project folders - copy', '00000001_ilivtests'}},
        2: {'include': {'Con Docs', 'Design Development', 'Marketing', 'Photos', 'Plot Files'}}
    }

    with ActiveTimer(DirPaths):
        for i in range(0, iters):
            paths = DirPaths(root, console_output=True, parallelize=True, to_exclude=to_exclude, max_level=max_level,
                             filters=filters, console_stream=False, pool_size=16, non_empty_folders=True)
        paths_sorted = sorted(paths)
        DictTools(save, 'DirPaths_filters_projects_1B').save(list(paths_sorted))

    with ActiveTimer(DirPaths):
        for i in range(0, iters):
            paths2 = DirPaths(root, console_output=True, console_stream=False, to_exclude=to_exclude,
                              max_level=max_level, filters=filters, non_empty_folders=True)
        paths_sorted = sorted(paths2)
        DictTools(save, 'DirPaths_filters_projects_2').save(list(paths_sorted))

    # with MyTimer(list_compare):
    #     unique1, unique2 = list_compare(paths, paths2)
    #     DictTools(save, 'DirPaths_filters_projects_1_u').save(list(unique1))
    #     DictTools(save, 'DirPaths_filters_projects_2_u').save(list(unique2))

