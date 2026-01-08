import os
import json
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Database file path
DB_FILE = BASE_DIR / "data.json"

# Default settings
default_settings = {
    "robokassa_enabled": False,
    "robokassa_merchant_login": "",
    "robokassa_password1": "",
    "robokassa_password2": "",
    "test_mode": True
}

def load_settings():
    """Load settings from database file."""
    try:
        if DB_FILE.exists():
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
                settings = data.get('settings', {})
                # Ensure all default settings exist
                for key, value in default_settings.items():
                    if key not in settings:
                        settings[key] = value
                return settings
        else:
            return default_settings.copy()
    except Exception as e:
        print(f"Error loading settings: {e}")
        return default_settings.copy()

def save_settings(settings):
    """Save settings to database file."""
    try:
        # Load existing data
        if DB_FILE.exists():
            with open(DB_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {}
        
        # Update settings
        data['settings'] = settings
        
        # Save back to file
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def get_setting(key, default=None):
    """Get a specific setting value."""
    settings = load_settings()
    return settings.get(key, default if default is not None else default_settings.get(key))

def set_setting(key, value):
    """Set a specific setting value."""
    settings = load_settings()
    settings[key] = value
    return save_settings(settings)

def initialize_database():
    """Initialize the database with default settings if it doesn't exist."""
    if not DB_FILE.exists():
        save_settings(default_settings.copy())
