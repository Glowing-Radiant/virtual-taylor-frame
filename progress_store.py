# Progress Store for Virtual Taylor Frame
# Persists a single student's tutorial progress (completion, best stars,
# unlock state) across sessions.

import json
import os


DEFAULT_PROGRESS_DIR = os.path.join(os.path.expanduser("~"), ".virtual_taylor_frame")
DEFAULT_PROGRESS_PATH = os.path.join(DEFAULT_PROGRESS_DIR, "progress.json")


class ProgressStore:
    """Tracks tutorial completion, best star ratings, and level-unlock state.

    Stored as JSON in the user's home directory rather than next to the
    executable, since a PyInstaller build's install location (or its
    _MEIPASS extraction folder) isn't reliably writable.
    """

    def __init__(self, path=None):
        self.path = path or DEFAULT_PROGRESS_PATH
        self.data = {"version": 1, "tutorials": {}}
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            if isinstance(loaded, dict) and isinstance(loaded.get("tutorials"), dict):
                self.data = loaded
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

    def _entry(self, tutorial_id):
        return self.data["tutorials"].get(tutorial_id, {
            "completed": False,
            "best_stars": 0,
            "plays": 0,
        })

    def is_completed(self, tutorial_id):
        """Whether this tutorial has been finished at least once"""
        return self._entry(tutorial_id)["completed"]

    def get_best_stars(self, tutorial_id):
        """Best star rating (0-3) ever earned on this tutorial"""
        return self._entry(tutorial_id)["best_stars"]

    def record_completion(self, tutorial_id, stars):
        """Record finishing a tutorial with the given star rating"""
        entry = self._entry(tutorial_id)
        entry["completed"] = True
        entry["best_stars"] = max(entry["best_stars"], stars)
        entry["plays"] = entry["plays"] + 1
        self.data["tutorials"][tutorial_id] = entry
        self.save()

    def total_stars(self, tutorial_ids):
        """Sum of best stars across the given tutorial ids"""
        return sum(self.get_best_stars(tid) for tid in tutorial_ids)

    def completed_count(self, tutorial_ids):
        """Count of the given tutorial ids that have been completed"""
        return sum(1 for tid in tutorial_ids if self.is_completed(tid))

    def is_unlocked(self, tutorial_id, order):
        """Whether a tutorial is playable given the fixed progression order.

        The first tutorial in `order` is always unlocked; each subsequent
        one unlocks once the previous tutorial in the sequence has been
        completed at least once.
        """
        if tutorial_id not in order:
            return True
        index = order.index(tutorial_id)
        if index == 0:
            return True
        return self.is_completed(order[index - 1])
