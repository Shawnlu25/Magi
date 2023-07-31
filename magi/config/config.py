import yaml
import os
import logging
import pkg_resources
import shutil
from typing import Dict
from pathlib import Path
from .paths import CONFIG_PATH
from packaging import version

"""
Load Magi config file at ~/.magi/config.yaml

config_path: Path to config file, including the filename, e.g. ~/.magi/config.yaml
"""

def load_config(config_path: Path = CONFIG_PATH) -> Dict:
    if not os.path.exists(config_path):
        logging.info(f'Config file not found at {config_path}, initialize new config file at {config_path}')
        _initialize_config(config_path)
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}
    return config


"""
Initialize config file at stated location

config_path: Path to config file, including the filename, e.g. ~/.magi/config.yaml
"""

def _initialize_config(config_path: Path = CONFIG_PATH):
    if not os.path.exists(os.path.dirname(config_path)):
        try:
            os.makedirs(os.path.dirname(config_path))
        except Exception as e:
            logging.error(f'Failed to create directory {os.path.dirname(config_path)}: {e}')
    
    try:
        source = pkg_resources.resource_filename(__name__, 'config.yaml')
        shutil.copy(source, config_path)
        logging.info(f'Config file initialized at {config_path}')
    except Exception as e:
        logging.error(f'Failed to initialize config file: {e}')
        raise e

"""
Merge config file with new config
"""
def _check_and_update_config(config: Dict):
    try:
        source = pkg_resources.resource_filename(__name__, 'config.yaml')
        with open(source, 'r') as f:
            default_config = yaml.safe_load(f)
    except Exception as e:
        logging.error(f'Failed to load default config: {e}')
        raise e
    if version.parse(default_config["version"]) == version.parse(config["version"]):
        return
    merged_config = _deep_merge(config, default_config)
    merged_config["version"] = default_config["version"]
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(merged_config, f, sort_keys=False)
        logging.info(f'Config file updated to {default_config["version"]} at {CONFIG_PATH}')
    
def _deep_merge(source_dict, merge_dict):
    result = source_dict.copy()
    for key, value in merge_dict.items():
        if key in result:
            if isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result