import os
import sys
from datetime import datetime
import logging


class LogOutput:
    def __init__(self, save_directory, name):
        self.filename = str(save_directory) + '/_logs/' + str(datetime.now().strftime("%Y-%m-%d")) + '.txt'
        self.name = name
        self.log_file = self.setup_custom_logger()

    def logger(self, msg):
        print(str('\n' + msg))
        self.log_file.info(msg)

    def setup_custom_logger(self):
        formatter = logging.Formatter(fmt='%(asctime)s %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p: ')
        if os.path.exists(self.filename):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        handler = logging.FileHandler(self.filename, mode=append_write)
        handler.setFormatter(formatter)
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        # logger.addHandler(screen_handler)
        return logger
