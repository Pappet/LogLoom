import re
from datetime import datetime
from utils import calculate_time_difference
from .base_parser import BaseParser


class CLFParser(BaseParser):
    """
    Parser for the Common Log Format (CLF).
    """
    # Regular expression to match the CLF format
    pattern = re.compile(r'(?P<ip>\d+\.\d+\.\d+\.\d+) '           # IP Address
                         # Remote log name
                         r'(?P<remote_log_name>\S+) '
                         r'(?P<user_id>\S+) '                     # User id
                         r'\[(?P<timestamp>.*?)\] '               # Timestamp
                         r'"(?P<request>.*?)" '                   # Request
                         r'(?P<status>\d+) '                      # Status Code
                         r'(?P<size>\d+|-)'                       # Size or '-'
                         )


def analyze_clf_data(parsed_data):
    """
    Analyze the parsed CLF data to extract useful insights.

    Args:
        parsed_data (list): List of dictionaries containing parsed CLF log entries.

    Returns:
        dict: A dictionary containing the insights from the analysis.
    """
    # Initializing counters and placeholders
    timestamps = []
    status_codes = {}

    for entry in parsed_data:
        # Assuming 'timestamp' and 'status' are the keys for timestamp and status code respectively
        timestamp = entry['timestamp']
        status = entry['status']

        # Collecting timestamps
        # Convert string timestamp to datetime object for easier processing
        timestamps.append(datetime.strptime(timestamp, '%d/%b/%Y %H:%M:%S'))

        # Counting status codes
        if status in status_codes:
            status_codes[status] += 1
        else:
            status_codes[status] = 1

    insights = {
        'earliest_timestamp': min(timestamps),
        'latest_timestamp': max(timestamps),
        'status_code_counts': status_codes
    }

    """Display insights in a formatted manner."""

    separator = "=" * 50
    insights_header = "Log File Insights".center(50)

    # Extract status and count for the first item
    first_status, first_count = list(insights['status_code_counts'].items())[0]
    # Prepare formatted status code counts with appropriate indentation for the remaining items
    indented_status_counts = ["    {}: {}".format(
        status, count) for status, count in list(insights['status_code_counts'].items())[1:]]

    # Combine first item with the rest
    status_counts = "{}: {}\n".format(
        first_status, first_count) + "\n".join(indented_status_counts)

    time_diff_in_minutes = calculate_time_difference(
        insights['earliest_timestamp'], insights['latest_timestamp'])

    message = f"""
    {separator}
    {insights_header}
    {separator}

    Time Range:
    From: {insights['earliest_timestamp']} 
    To:   {insights['latest_timestamp']}
    Difference: {time_diff_in_minutes} minutes
    Log Length: {len(parsed_data)} lines

    Status Code Counts:
    {status_counts}

    Enjoy diving deeper into your logs with LogLoom!
    """

    print(message)
