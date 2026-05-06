import json
import os
import sys
from types import SimpleNamespace

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

MANDATORY_SETTINGS = [
    "model.host",
    "model.name",
    "model.headers",
    "model.provider",
    "agent.max_messages",
    "agent.max_loop_iterations",
    "agent.show_thinking",
    "tools.show_usage",
    "tools.websearch_max_results",
    "mcp.servers"
]

def dict_to_namespace(data, key_name=""):
    """
    Recursively converts dictionaries into SimpleNamespace objects,
    but keeps 'headers' as a regular dictionary for library compatibility.
    """
    if isinstance(data, dict):
        # We check if the current key is 'headers' to keep it as a dict
        if key_name == "headers":
            return data
        return SimpleNamespace(**{k: dict_to_namespace(v, k) for k, v in data.items()})
    return data

def validate_settings(data):
    """Checks if all mandatory settings are present in the loaded dictionary."""
    for setting in MANDATORY_SETTINGS:
        keys = setting.split('.')
        temp = data
        for key in keys:
            if isinstance(temp, dict) and key in temp:
                temp = temp[key]
            else:
                print(f"❌ ERROR: Missing mandatory setting: '{setting}'")
                sys.exit(1)

def load_config():
    """Loads, validates, and transforms the JSON config into an object."""
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ ERROR: Configuration file not found at: {CONFIG_PATH}")
        sys.exit(1)

    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Validate before converting to object
            validate_settings(data)
            
            # Convert to namespace but preserving dictionaries where needed
            return dict_to_namespace(data)
            
    except json.JSONDecodeError as e:
        print(f"❌ ERROR: 'config.json' has invalid syntax: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected ERROR loading config: {e}")
        sys.exit(1)

# Initialize the global config object
config = load_config()