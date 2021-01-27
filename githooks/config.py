"""sc-githooks - Configurations

Copyright (c) 2021 Scott Lau
"""

import os

from config42 import ConfigManager
from githooks.configs.default import DEFAULT_CONFIG
from githooks.configs.development import DEV_CONFIG


class Config:

    @staticmethod
    def create():
        # load defaults from defaults.py file
        config = ConfigManager(defaults=DEFAULT_CONFIG)
        # load defaults from home directory
        config_file = os.path.join(os.path.expanduser('~'), '.sc-githooks/default.yml')
        if os.path.exists(config_file):
            config.set_many(ConfigManager(path=config_file))
        # load environment configurations from environment variables
        env_config = ConfigManager(prefix="SC_GITHOOKS")
        config.set_many(env_config.as_dict())

        environment = env_config.get("environment")
        if environment is None:
            # use production configuration if not specified environment
            environment = "production"
        if environment == "development":
            config.set_many(DEV_CONFIG)
        # load environment configurations from file
        env_config_file = os.path.join(os.path.expanduser('~'), '.sc-githooks/{}.yml'.format(environment))
        if os.path.exists(env_config_file):
            config.set_many(ConfigManager(path=env_config_file).as_dict())
        return config


# =========================================
#       INSTANCES
# --------------------------------------
try:
    config = Config.create()

except Exception as error:
    print('WARN: {0}'.format(error))
