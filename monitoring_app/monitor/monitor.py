import threading    # For threading operations
import psutil           # For system monitoring
import time     # For sleep and timing
import uuid     # For generating unique IDs

class Alarm:    # Alarm class to hold alarm details
    def __init__(self, alarm_type, level):      # Initialize alarm with type and level
        self.id = str(uuid.uuid4())      # Unique identifier for the alarm
        self.type = alarm_type          # Type of alarm: "cpu", "minne", or "disk"
        self.level = level             # Threshold level for the alarm

class Monitor(threading.Thread):
    def __init__(self, alarms=None, logger=None):
        super().__init__()
        self.alarms = alarms or []
        self.running = False
        self.stop_event = threading.Event()
        self.suppress_alarms = threading.Event()
        self.logger = logger

    #   Thread run method
    def run(self):
        self.running = True
        while not self.stop_event.is_set():
            cpu, mem, disk = self.get_current_status()
            self._check_alarms("cpu", cpu)
            self._check_alarms("minne", mem[0])
            self._check_alarms("disk", disk[0])
            time.sleep(2)       # Check every 2 seconds
        self.running = False        # Mark as not running when stopped

    # Stop monitoring
    def stop(self):
        self.stop_event.set()   #  Signal the thread to stop
        self.join()         # Wait for the thread to finish

    # Get current system status
    def get_current_status(self):
        cpu = psutil.cpu_percent()      # CPU usage percentage
        mem = psutil.virtual_memory()   # Memory usage details
        disk = psutil.disk_usage('/')   # Disk usage details
        return cpu, (mem.percent, mem.used, mem.total), (disk.percent, disk.used, disk.total)  # Return CPU, memory, and disk status

    # Add a new alarm
    def add_alarm(self, alarm):
        self.alarms.append(alarm)     # Add alarm to the list

    # Check and trigger alarms
    def _check_alarms(self, alarm_type, value):     # Check and trigger alarms
        if self.suppress_alarms.is_set():  # Do not spam menu
            return

        # Trigger only the highest alarm for this type
        relevant_alarms = [a for a in self.alarms if a.type == alarm_type and value > a.level]
        if not relevant_alarms:
            return
        highest_alarm = max(relevant_alarms, key=lambda a: a.level)
        print(f"***VARNING: {highest_alarm.type.upper()} överstiger {highest_alarm.level}% ({value:.1f}%)***")
