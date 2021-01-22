#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""sc-githooks - Setup

Copyright (c) 2021 Scott Lau
Portions Copyright (c) 2021 InnoGames GmbH
Portions Copyright (c) 2021 Emre Hasegeli
"""

from setuptools import setup, find_packages

from githooks import VERSION
from githooks.config import checks

with open('README.rst') as fd:
    readme = fd.read()

setup(
    name='sc-githooks',
    version='.'.join(str(v) for v in VERSION),
    url='https://github.com/Scott-Lau/sc-githooks',
    packages=find_packages(),
    author='Scott Lau',
    author_email='exceedego@126.com',
    license='MIT',
    platforms='POSIX',
    description='Git pre-receive hook to check commits',
    long_description=readme,
    keywords=(
            'syntax-checker git git-hook python ' +
            ' '.join(c.args[0] for c in checks if hasattr(c, 'args'))
    ),
    entry_points={
        'console_scripts': [
            'sc-pre-receive=githooks.pre_receive:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)
