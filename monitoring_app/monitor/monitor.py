import threading
import psutil
import time
import uuid

class Alarm:
    def __init__(self, alarm_type, level):
        self.id = str(uuid.uuid4())
        self.type = alarm_type
        self.level = level

class Monitor(threading.Thread):
    def __init__(self, alarms=None, logger=None):
        super().__init__()
        self.alarms = alarms or []
        self.running = False
        self.stop_event = threading.Event()
        self.suppress_alarms = threading.Event()
        self.logger = logger

    def run(self):
        self.running = True
        while not self.stop_event.is_set():
            cpu, mem, disk = self.get_current_status()
            self._check_alarms("cpu", cpu)
            self._check_alarms("minne", mem[0])
            self._check_alarms("disk", disk[0])
            time.sleep(2)
        self.running = False

    def stop(self):
        self.stop_event.set()
        self.join()

    def get_current_status(self):
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return cpu, (mem.percent, mem.used, mem.total), (disk.percent, disk.used, disk.total)

    def add_alarm(self, alarm):
        self.alarms.append(alarm)

    def _check_alarms(self, alarm_type, value):
        if self.suppress_alarms.is_set():  # Do not spam menu
            return

        # Trigger only the highest alarm for this type
        relevant_alarms = [a for a in self.alarms if a.type == alarm_type and value > a.level]
        if not relevant_alarms:
            return
        highest_alarm = max(relevant_alarms, key=lambda a: a.level)
        print(f"***VARNING: {highest_alarm.type.upper()} överstiger {highest_alarm.level}% ({value:.1f}%)***")
