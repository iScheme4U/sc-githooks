"""Configurations

Copyright (c) 2021 Scott Lau
"""

import os
import logging

from config42 import ConfigManager

from githooks.configs.default import DEFAULT_CONFIG
from githooks.configs.development import DEV_CONFIG


class Config:

    @staticmethod
    def _get_config_file_path(project_name, environment):
        config_directory = '.{}'.format(project_name)
        return os.path.join(os.path.expanduser('~'), '{}/{}.yml'.format(config_directory, environment))

    @staticmethod
    def create():
        project_name = "sc-githooks"
        prefix = project_name.upper()
        prefix = prefix.replace("-", "_")
        # load defaults from defaults.py file
        config = ConfigManager(defaults=DEFAULT_CONFIG)
        # load defaults from home directory
        config_file = Config._get_config_file_path(project_name, "default")
        if os.path.exists(config_file):
            logging.getLogger(__name__).info("loading default configurations from %s", config_file)
            config.set_many(ConfigManager(path=config_file).as_dict())
        # load environment configurations from environment variables
        env_config = ConfigManager(prefix=prefix)
        config.set_many(env_config.as_dict())

        key_env = "environment"
        environment = env_config.get(key_env)
        if environment is None:
            # use production configuration if not specified environment
            environment = "production"
            logging.getLogger(__name__).info("did not specify environment, using %s", environment)
            config.set(key_env, environment)
        else:
            logging.getLogger(__name__).info("using environment: %s", environment)
        if environment == "development":
            config.set_many(DEV_CONFIG)
        # load environment configurations from file
        env_config_file = Config._get_config_file_path(project_name, environment)
        if os.path.exists(env_config_file):
            logging.getLogger(__name__).info("loading environmental configurations from %s", env_config_file)
            config.set_many(ConfigManager(path=env_config_file).as_dict())
        return config


# =========================================
#       INSTANCES
# --------------------------------------
try:
    config = Config.create()
except Exception as error:
    logging.getLogger(__name__).exception("failed to read configuration", exc_info=error)
