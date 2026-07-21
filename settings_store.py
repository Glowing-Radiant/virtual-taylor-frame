# Settings Store for Virtual Taylor Frame
# Persists user preferences (default toggle states) across sessions.

import json
import os


DEFAULT_SETTINGS_DIR = os.path.join(os.path.expanduser("~"), ".virtual_taylor_frame")
DEFAULT_SETTINGS_PATH = os.path.join(DEFAULT_SETTINGS_DIR, "settings.json")


class SettingsStore:
    """Persists user preferences, such as whether Auto-shift and Smart
    delete should start on or off each time the program launches.

    Stored as JSON in the user's home directory rather than next to the
    executable, since a PyInstaller build's install location (or its
    _MEIPASS extraction folder) isn't reliably writable.
    """

    def __init__(self, path=None):
        self.path = path or DEFAULT_SETTINGS_PATH
        self.data = {
            "version": 1,
            "auto_shift_default": False,
            "smart_delete_default": False,
        }
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict):
                self.data.update(loaded)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    def save(self):
        try:
            dir_name = os.path.dirname(self.path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=True, indent=2)
        except OSError:
            pass

    def get_auto_shift_default(self):
        """Whether Auto-shift should start on when the program launches"""
        return bool(self.data.get("auto_shift_default", False))

    def set_auto_shift_default(self, value):
        self.data["auto_shift_default"] = bool(value)
        self.save()

    def get_smart_delete_default(self):
        """Whether Smart delete should start on when the program launches"""
        return bool(self.data.get("smart_delete_default", False))

    def set_smart_delete_default(self, value):
        self.data["smart_delete_default"] = bool(value)
        self.save()
