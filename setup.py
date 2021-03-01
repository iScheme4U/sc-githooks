#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""sc-githooks - Setup

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

import os

from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open('README.rst') as fd:
    readme = fd.read()

setup(
    name='sc-githooks',
    version=get_version("githooks/__init__.py"),
    url='https://github.com/Scott-Lau/sc-githooks',
    packages=find_packages(),
    author='Scott Lau',
    author_email='exceedego@126.com',
    license='MIT',
    platforms='POSIX',
    description='Git pre-receive hook to check commits',
    long_description=readme,
    keywords=(
        'git git-hook python pre-receive hook'
    ),
    entry_points={
        'console_scripts': [
            'sc-pre-receive=githooks.pre_receive:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    python_requires='>=3.6',
    install_requires=[
        'sc-config>=0.0.3',
    ],
)
