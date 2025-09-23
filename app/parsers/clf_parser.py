import re
from datetime import datetime
from utils import calculate_time_difference, get_range, time_difference, get_counts
from .base_parser import BaseParser


class CLFParser(BaseParser):
    """
    Parser for the Common Log Format (CLF).
    """
    # List of possible timestamp formats, from most to least specific.
    timestamp_formats = [
        "%d/%b/%Y %H:%M:%S %z",  # Format with timezone
        "%d/%b/%Y %H:%M:%S"      # Format without timezone
    ]

    # Analysis configuration for CLF data
    analysis_config = {
        "timestamp": [get_range, time_difference],
        "status": [get_counts],
        "ip": [get_counts]
    }

    # Regular expression to match the CLF format
    # The request part is now non-greedy to handle potential extra content after it.
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) '  # IP Address
                         r'(?P<remote_log_name>\S+) '   # Remote log name
                         r'(?P<user_id>\S+) '           # User id
                         r'\[(?P<timestamp>.*?)\] '     # Timestamp
                         r'"(?P<request>.*?)" '         # Request
                         r'(?P<status>\d+) '            # Status Code
                         r'(?P<size>\d+|-)'             # Size or '-'
                         )