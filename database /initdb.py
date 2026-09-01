import json
import os

DATA_FILE = "data_store.json"

def get_default_db():
    return {
        "session": {},
        "questions": [],
        "evaluations": []
    }

def load_db():
    """Loads session state from local JSON storage."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return get_default_db()
    return get_default_db()

def save_db(data):
    """Persists current state into local JSON storage."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
