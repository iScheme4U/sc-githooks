"""Configurations

Copyright (c) 2021 Scott Lau
"""

from sys import stdout, stderr
from traceback import print_exc

from scconfig.config import Config

from githooks.base_check import BaseCheck
from githooks.configs.default import DEFAULT_CONFIG

# =========================================
#       INSTANCES
# --------------------------------------
try:
    config = Config.create(project_name="sc-githooks", defaults=DEFAULT_CONFIG)
except Exception as e:
    stdout.flush()
    print(file=stderr)
    print('{} failed to read configuration: {}'.format(BaseCheck.ERROR_MSG_PREFIX, e), file=stderr)
    print_exc()
