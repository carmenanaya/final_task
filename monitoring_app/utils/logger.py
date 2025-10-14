import logging
from datetime import datetime
from pathlib import Path

def setup_logger():     # Function to set up logging
    log_dir = Path("logs")  # Directory for log files
    log_dir.mkdir(exist_ok=True)  # Create directory if it doesn't exist
    log_file = log_dir / f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"  # Log file name with timestamp

    # Set up logger
    logger = logging.getLogger("monitor_app")   # Logger name
    logger.setLevel(logging.INFO)       # Log level

    handler = logging.FileHandler(log_file, encoding="utf-8")       # File handler
    formatter = logging.Formatter("%(asctime)s_%(message)s", datefmt="%d/%m/%Y_%H:%M")   # Log format
    handler.setFormatter(formatter)   # Set formatter for handler
    logger.addHandler(handler)  # Add handler to logger
    return logger       # Return configured logger