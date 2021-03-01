"""Configurations

Copyright (c) 2021 Scott Lau
"""

from sys import stderr
from traceback import print_exc

from scconfig.config import Config

from githooks.configs.default import DEFAULT_CONFIG

# =========================================
#       INSTANCES
# --------------------------------------
try:
    config = Config.create(project_name="sc-githooks", defaults=DEFAULT_CONFIG)
except Exception as error:
    print(file=stderr)
    print('failed to read configuration', file=stderr)
    print_exc()
