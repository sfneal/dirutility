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

    def __init__(self, func, iterable, cpus=cpu_count(), cpu_reduction=0, filter_nulls=False):
        """
        Multiprocessing helper function for performing looped operation using multiple processors.

        :param func: Function to call
        :param iterable: Iterable object to perform each function on
        :param cpus: Number of cpu cores, defaults to system's cpu count
        :param cpu_reduction: Number of cpu core's to not use
        :param filter_nulls: Bool, when true None values are removed from the result list before return
        """
        self._func = func
        self._iterable = iterable
        self.cpu_count = cpus - abs(cpu_reduction)
        self.filter_nulls = filter_nulls

        self._result = None

    @property
    def result(self):
        """Return the results returned by map_return or map_tqdm methods."""
        # Remove None values from self._result if filter_nulls is enabled
        return [i for i in self._result if i is not None] if self.filter_nulls else self._result

    def map(self):
        """Perform a function on every item in an iterable."""
        with Pool(self.cpu_count) as pool:
            pool.map(self._func, self._iterable)
            pool.close()
        return True

    def map_return(self):
        """Perform a function on every item and return a list of yield values."""
        with Pool(self.cpu_count) as pool:
            self._result = pool.map(self._func, self._iterable)
            pool.close()
            return self.result

    def map_tqdm(self, desc=None, unit='it'):
        """
        Perform a function on every item while displaying a progress bar.

        :param desc: Optional, progress bar description
        :param unit: Optional, progress bar units (default is 'it' for 'iteration')
        :return: A list of yielded values
        """
        tqdm_args = dict(total=len(self._iterable),
                         desc=desc,
                         unit=unit)
        with Pool(self.cpu_count) as pool:
            self._result = [v for v in tqdm(pool.imap_unordered(self._func, self._iterable), **tqdm_args)]
            pool.close()
            return self.result
