import yaml
import os


def load_config():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_path = os.path.join(root_dir, "config.yaml")

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config