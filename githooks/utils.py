"""sc-githooks - Utility functions

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from os import environ, access, X_OK


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


def decode_str(string):
    """trying decode a string

    first try to decode using utf-8,
    if error occurred then using gbk, if still fail then return the original string

    :param string: the string to be decoded
    :return: decoded string
    """
    try:
        return string.decode('utf-8')
    except UnicodeDecodeError:
        try:
            return string.decode('gbk')
        except UnicodeDecodeError:
            return string
