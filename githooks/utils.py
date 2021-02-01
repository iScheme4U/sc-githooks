"""sc-githooks - Utility functions

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

import logging
import logging.handlers
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from os import environ, access, X_OK

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_FILE_NAME = os.environ.get('LOG_FILE_NAME', 'logs/sys.log')
LOG_FORMAT = os.environ.get('LOG_FORMAT', '%(asctime)s [%(levelname)s]: %(message)s')


def get_exe_path(exe):
    for dir_path in environ['PATH'].split(':'):
        path = dir_path.strip('"') + '/' + exe
        if access(path, X_OK):
            return path


def iter_buffer(iterable, amount):
    assert amount > 1
    memo = []
    for elem in iterable:
        if elem is not None:
            memo.append(elem)
            if len(memo) < amount:
                continue
        yield memo.pop(0)

    for elem in memo:
        yield elem


def get_extension(file_path):
    if '.' not in file_path:
        return None
    return file_path.rsplit('.', 1)[1]


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def log_init():
    ensure_dir(LOG_FILE_NAME)
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    file_handler = TimedRotatingFileHandler(LOG_FILE_NAME, when='D', interval=1, backupCount=32)
    formatter = logging.Formatter(LOG_FORMAT)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
