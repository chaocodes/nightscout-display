import configparser

config = configparser.ConfigParser()
config.read("config.ini")

required_keys = {"nightscout": ["base_url"]}

for section, keys in required_keys.items():
    if not config.has_section(section):
        raise ValueError(f"{section} section not found in config.ini")
    for key in keys:
        if not config.has_option(section, key):
            raise ValueError(f"{section} {key} not found in config.ini")


def get_config() -> configparser.ConfigParser:
    return config
