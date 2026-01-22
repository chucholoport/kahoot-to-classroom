import os
import sys
import configparser
from typing import Dict, Any

from cfgparser.config import kahoot_to_classroom

k2c = kahoot_to_classroom()

def load_config(path: str) -> Dict[str, Any]:

    parser = configparser.ConfigParser()
    parser.read(path)

    # Validate required sections dynamically
    for section in k2c.required_sections:
        if section not in parser:
            sys.stderr.write(f"error: missing section [{section}] in {path}\n")
            sys.exit(os.EX_CONFIG)

    # Extract and validate values dynamically
    config_values: Dict[str, Any] = {}
    for section, keys in k2c.required_keys.items():
        for key in keys:
            value = parser[section].get(key)
            if not value:
                sys.stderr.write(f"error: missing key '{key}' in section [{section}] of {path}\n")
                sys.exit(os.EX_CONFIG)

            # Validate file paths for certs and data
            if section == k2c.certs.name:
                if not os.path.exists(value):
                    sys.stderr.write(f"error: credentials file not found: {value}\n")
                    sys.exit(os.EX_NOINPUT)
                if not value.lower().endswith(".json"):
                    sys.stderr.write(f"error: credentials file must be .json: {value}\n")
                    sys.exit(os.EX_DATAERR)

            if section == k2c.data.name:
                if not os.path.exists(value):
                    sys.stderr.write(f"error: student list file not found: {value}\n")
                    sys.exit(os.EX_NOINPUT)
                if not value.lower().endswith(".txt"):
                    sys.stderr.write(f"error: student list must be .txt: {value}\n")
                    sys.exit(os.EX_DATAERR)

            config_values[key] = value

    # Return dictionary
    return config_values