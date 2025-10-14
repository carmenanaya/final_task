import json
from pathlib import Path
from monitor.monitor import Alarm

ALARM_FILE = Path("alarms.json")

def save_alarms(alarms):
    data = [{"id": a.id, "type": a.type, "level": a.level} for a in alarms]
    with ALARM_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f)

def load_alarms():
    if not ALARM_FILE.exists():
        return []
    with ALARM_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [Alarm(a["type"], a["level"]) for a in data]