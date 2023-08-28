import re
from .base_parser import BaseParser


class SystemdJournalParser(BaseParser):
    # Regular expression to parse the syslog format
    pattern = re.compile(
        r'(?P<timestamp>[A-Za-z]{3} \d{1,2} \d{1,2}:\d{1,2}:\d{1,2}) '  # Timestamp
        r'(?P<hostname>[\w\-\.]+) '                                   # Hostname
        r'(?P<service>\w+)(?:\[(?P<pid>\d+)\])?: '                     # Service/Program with optional PID
        r'(?P<message>.*)'                                            # Message
        )
