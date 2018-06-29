import time


class Timer:
    def __init__(self):
        self.start = time.time()

    @property
    def end(self):
        end = time.time()
        elapsed = end - self.start
        if elapsed < 60:
            elapsed = str('sec: ' + str(elapsed))
        else:
            elapsed = str('min: ' + str(elapsed/60))
        # times_dict = {self.function: elapsed}
        return elapsed