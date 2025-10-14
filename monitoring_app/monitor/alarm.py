from monitor.monitor import Alarm  # Import the Alarm class from monitor.py

# Function to create a new alarm
def create_alarm(alarm_type, level):
    return Alarm(alarm_type, level) # Return the created Alarm object
