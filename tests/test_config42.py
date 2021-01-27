import unittest

from config42 import ConfigManager

from githooks.config import config


class MyTestCase(unittest.TestCase):

    def test_get_config(self):
        defaults = ConfigManager(path="sample_config/default.yml")
        env_config = ConfigManager(prefix="SC_GITHOOKS", defaults=defaults)
        environment = env_config.get("environment")

        self.assertEqual(environment, 'development')
        self.assertEqual(env_config.get("dev.dev_mode"), False)
        self.assertEqual(env_config.get("commit_check.commit_summary_max_length"), 50)

    def test_create_config(self):
        self.assertIsNotNone(config)
        environment = config.get("environment")

        self.assertEqual(environment, 'development')
        self.assertEqual(config.get("dev.dev_mode"), True)
        self.assertEqual(config.get("commit_check.commit_summary_max_length"), 50)


if __name__ == '__main__':
    unittest.main()
