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
