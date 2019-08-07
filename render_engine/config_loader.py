from pathlib import Path
import logging
import yaml

def load_config(config_path, section):
    """Tests for a valid config file and loads a section of the yaml file,
    or if not specified, the entire configuration
    """

    config_path = Path(config_path)
    # config path needs to be a valid yaml file that exists
    # logging for config_path
    if not config_path.exists:
        logging.warn(f'Config path f{config_path} does not exist! Ignoring Path')
    elif config_path.suffix != '.yaml':
        logging.warn(f'Config Path not a valid yaml file')

    # Succesful config_path
    else:
        logging.debug(f'Config Path: {config_path} found. Loading...')
        config = yaml.safe_load(config_path.read_text())

        if section in config:
            return config[section]
        else:
            return config
