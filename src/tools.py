import os
from typing import Any, Dict
import yaml

class Tools:
    @staticmethod
    def check_and_load(path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            return "File not found: {}".format(path)
        else:
            try:
                with open(path, "r") as config_file:
                    config: Dict[str, Any] = yaml.safe_load(config_file)
                return config
            except yaml.YAMLError as e:
                return f"Error loading Yaml file: {e}"