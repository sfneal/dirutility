from multiprocessing import cpu_count
from multiprocessing.pool import Pool
from tqdm import tqdm


def pool_process(func, iterable, cpus=cpu_count(), return_vals=False, cpu_reduction=0, progress_bar=False):
    """
    Multiprocessing helper function for performing looped operation using multiple processors.

    :param func: Function to call
    :param iterable: Iterable object to perform each function on
    :param cpus: Number of cpu cores, defaults to system's cpu count
    :param return_vals: Bool, returns output values when True
    :param cpu_reduction: Number of cpu core's to not use
    :param progress_bar: Display text based progress bar
    :return:
    """
    with Pool(cpus - abs(cpu_reduction)) as pool:
        # Return values returned by 'func'
        if return_vals:
            # Show progress bar
            if progress_bar:
                vals = [v for v in tqdm(pool.imap_unordered(func, iterable), total=len(iterable))]

            # No progress bar
            else:
                vals = pool.map(func, iterable)

            # Close pool and return values
            pool.close()
            # pool.join()
            return vals

        # Don't capture values returned by 'func'
        else:
            pool.map(func, iterable)
            pool.close()
            return True


class PoolProcess:
    _func = None
    _iterable = None

    def __init__(self, func, iterable, cpus=cpu_count(), cpu_reduction=0):
        """
        Multiprocessing helper function for performing looped operation using multiple processors.

        :param func: Function to call
        :param iterable: Iterable object to perform each function on
        :param cpus: Number of cpu cores, defaults to system's cpu count
        :param cpu_reduction: Number of cpu core's to not use
        """
        self._func = func
        self._iterable = iterable
        self.cpu_count = cpus - abs(cpu_reduction)

    def map(self):
        """Perform a function on every item in an iterable."""
        with Pool(self.cpu_count) as pool:
            pool.map(self._func, self._iterable)
            pool.close()
        return True

    def map_return(self):
        """Perform a function on every item and return a list of yield values."""
        with Pool(self.cpu_count) as pool:
            vals = pool.map(self._func, self._iterable)
            pool.close()
            return vals

    def map_tqdm(self):
        """
        Perform a function on every item while displaying a progress bar.

        :return: A list of yielded values
        """
        with Pool(self.cpu_count) as pool:
            vals = [v for v in tqdm(pool.imap_unordered(self._func, self._iterable), total=len(self._iterable))]
            pool.close()
            return vals
