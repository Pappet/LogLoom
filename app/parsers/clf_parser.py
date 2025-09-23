import re
from datetime import datetime
from utils import calculate_time_difference
from .base_parser import BaseParser


class CLFParser(BaseParser):
    """
    Parser for the Common Log Format (CLF).
    """
    # Regular expression to match the CLF format
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) '  # IP Address
                         r'(?P<remote_log_name>\S+) '   # Remote log name
                         r'(?P<user_id>\S+) '           # User id
                         r'\[(?P<timestamp>.*?)\] '     # Timestamp
                         r'"(?P<request>.*?)" '         # Request
                         r'(?P<status>\d+) '            # Status Code
                         r'(?P<size>\d+|-)'             # Size or '-'
                         )
