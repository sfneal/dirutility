from multiprocessing import cpu_count
from multiprocessing.pool import Pool


def pool_process(func, iterable, cpus=cpu_count(), return_vals=False, cpu_reduction=0):
    """
    Multiprocessing helper function for performing looped operation using multiple processors.

    :param func: Function to call
    :param iterable: Iterable object to perform each function on
    :param cpus: Number of cpu cores, defaults to system's cpu count
    :param return_vals: Bool, returns output values when True
    :param cpu_reduction: Number of cpu core's to not use
    :return:
    """
    with Pool(cpus - abs(cpu_reduction)) as pool:
        if return_vals:
            vals = pool.map(func, iterable)
            pool.close()
            return vals
        else:
            pool.map(func, iterable)
            pool.close()
