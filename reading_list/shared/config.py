from typing import Any, Dict, Optional
from inspect import getmembers
import os
import json


class AConfig:
    """Required abstract class indicating a new configuration."""
    pass


class TinyDbConfig(AConfig):
    location: str = os.getenv('RL_TINY_DB_LOCATION', './db.json')


class DbDriverConfigOptions(AConfig):
    tiny_db: TinyDbConfig = TinyDbConfig()


class Config(AConfig):
    db: DbDriverConfigOptions = DbDriverConfigOptions()


DEFAULT_CONFIGS = Config()


def merge_configs(config: AConfig, custom_config: Optional[Dict[str, Any]] = None) -> AConfig:
    """Examples:

    >>> from unittest.mock import patch, MagicMock

    >>> default_config_value = "bar"
    >>> class TestConfigClass(AConfig):
    ...     class TestConfigClassEmbedded(AConfig):
    ...         foo = default_config_value
    ...     sub_config = TestConfigClassEmbedded()
    ...     foo = default_config_value
    ...     
    ...     def __str__(self):
    ...         return f'foo: {self.foo}, sub_config: foo: {self.sub_config.foo}'
    ...
    >>> def get_test_config():
    ...     return TestConfigClass()

    1. merge_configs: returns base config without changes if no custom configs are supplied
    >>> test_config = get_test_config()
    >>> result_config = merge_configs(test_config)
    >>> test_config.foo == result_config.foo == default_config_value
    True
    >>> test_config.sub_config.foo == result_config.sub_config.foo == default_config_value
    True

    2. merge_configs: returns partially merged config values if a partial custom config is given
    >>> test_config = get_test_config()
    >>> custom_config = {'foo': 'zed'}
    >>> result_config = merge_configs(test_config, custom_config)
    >>> result_config.foo == custom_config['foo']
    True
    >>> test_config.sub_config.foo == result_config.sub_config.foo == default_config_value
    True

    3. merge_configs: returns fully merged config values if full custom config is given
    >>> test_config = get_test_config()
    >>> custom_config = {'foo': 'zed', 'sub_config': {'foo': 'zar'}}
    >>> result_config = merge_configs(test_config, custom_config)
    >>> result_config.foo == custom_config['foo']
    True
    >>> result_config.sub_config.foo == custom_config['sub_config']['foo']
    True
    """

    def _update_config(base_config: AConfig, custom_config: Dict[str, Any]) -> AConfig:
        members = getmembers(base_config)
        for (key, value) in members:
            if isinstance(value, AConfig) and key in custom_config:
                _update_config(value, custom_config[key])
            elif key in custom_config and not hasattr(value, '__dict__'):
                setattr(base_config, key, custom_config[key])
        return base_config

    return _update_config(config, custom_config) if custom_config else config


def initialize_custom_configs(config_path: str) -> AConfig:
    with open(config_path) as f:
        custom_config: Dict[str, Any] = json.load(f)
    base_configs = Config()
    return merge_configs(base_configs, custom_config)
