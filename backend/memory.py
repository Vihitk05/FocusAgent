import json
import os
from datetime import datetime, timedelta

LOG_PATH = "data/logs.json"

class TaskMemory:
    def __init__(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        if not os.path.exists(LOG_PATH):
            with open(LOG_PATH, "w") as f:
                json.dump([], f)

    def _load_data(self):
        try:
            with open(LOG_PATH, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def retrieve_recent(self, days=3):
        data = self._load_data()
        cutoff = datetime.now() - timedelta(days=days)
        recent = [entry for entry in data if datetime.fromisoformat(entry.get("date", "1970-01-01")) >= cutoff]
        return recent

    def store_feedback(self, feedback):
        data = self._load_data()
        data.append({"date": datetime.now().isoformat(), "feedback": feedback})
        with open(LOG_PATH, "w") as f:
            json.dump(data, f, indent=2)