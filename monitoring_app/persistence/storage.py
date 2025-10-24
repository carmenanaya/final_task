import json   # For saving/loading alarms as JSON, JavaScript Object Notation
from pathlib import Path    # For file path operations
from monitor.monitor import Alarm   # Import Alarm class

ALARM_FILE = Path("alarms.json")


# Save alarms to a JSON file. Convert each alarm to a dictionary and write them to alarms.json. This file have been created by itself.
def save_alarms(alarms):
    data = [{"id": a.id, "type": a.type, "level": a.level} for a in alarms]   # Convert alarms to list of dicts
    with ALARM_FILE.open("w", encoding="utf-8") as f:   # Open file for writing
        json.dump(data, f)   # Write JSON data to file


# Load alarms from a JSON file
def load_alarms():
    if not ALARM_FILE.exists():
        return []
    with ALARM_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [Alarm(a["type"], a["level"]) for a in data]