import json
import os

SETTINGS_FILE = "settings.json"

# DEFAULT SETTINGS
default_settings = {
    "instagram_token": "",
    "instagram_id": "",
    "openai_key": "",
    "autoreply": True
}

# LOAD EXISTING OR CREATE NEW
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        settings_data = json.load(f)
else:
    settings_data = default_settings.copy()
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_data, f)


def load_settings():
    """Return current settings"""
    return settings_data


def save_settings(data: dict):
    """Update settings & write to disk"""
    global settings_data

    # update internal dict
    for key, value in data.items():
        settings_data[key] = value

    # save to json
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings_data, f, indent=4)

    return {"status": "saved", "settings": settings_data}
