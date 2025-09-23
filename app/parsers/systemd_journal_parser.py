import re
from .base_parser import BaseParser
from utils import get_range, time_difference, get_counts

class SystemdJournalParser(BaseParser):
    """
    Parser for the Systemd Journal format.
    """
    # Timestamp format used in Systemd logs
    timestamp_format = "%b %d %H:%M:%S"

    # Analysis configuration for Systemd data
    analysis_config = {
        "timestamp": [get_range, time_difference],
        "hostname": [get_counts],
        "service": [get_counts],
        "pid": [get_counts]
    }

    # Regular expression to parse the syslog format
    pattern = re.compile(
        r'(?P<timestamp>[A-Za-z]{3} \d{1,2} \d{1,2}:\d{1,2}:\d{1,2}) '  # Timestamp
        r'(?P<hostname>[\w\-\.]+) '                                   # Hostname
        r'(?P<service>\w+)(?:\[(?P<pid>\d+)\])?: '                     # Service/Program with optional PID
        r'(?P<message>.*)'                                            # Message
        )