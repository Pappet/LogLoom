from datetime import datetime


def read_log_file(file_path):
    """
    Read a log file and yield its lines.

    Args:
        file_path (str): Path to the log file to be read.

    Yields:
        str: A line from the log file.
    """
    with open(file_path, 'r') as file:
        for line in file:
            yield line


def display_welcome_message():
    """Display the welcome message for LogLoom."""
    separator = "=" * 62
    welcome_header = "WELCOME TO LogLoom - Your Log Companion".center(62)

    message = f"""
    {separator}
    {welcome_header}
    {separator}

    Navigating the world of log files can be daunting. With LogLoom, it doesn't have to be. 

    HOW IT WORKS:
    1. **INPUT**: Provide a path to your log file and specify its format (e.g., CLF, Syslog, etc.).
    2. **ANALYZE**: LogLoom will parse the log data, providing insights such as time range, status codes, and more.
    3. **DISPLAY**: Choose specific keys or details you'd like to view, filter, and analyze.
    4. **FILTER**: Optionally, extract specific entries based on criteria you provide for a focused view.

    KEY TIPS:
    - Use the '--help' option to see all available commands and options.
    - For better display experience, LogLoom adjusts column widths based on content. Say goodbye to cluttered views!
    - Easily expand LogLoom's capabilities by adding custom parsers for new log formats.

    Ready to weave through your logs? Let's get started!

    For any feedback or issues, visit [YourSupportLinkHere].
    Enjoy your journey with LogLoom!
    """

    print(message)


def calculate_time_difference(start_time, end_time, time_format='%Y-%m-%d %H:%M:%S'):
    """Calculate the difference in minutes between two timestamps."""

    # Ensure that start_time and end_time are datetime objects
    if isinstance(start_time, str):
        start_datetime = datetime.strptime(start_time, time_format)
    else:
        start_datetime = start_time

    if isinstance(end_time, str):
        end_datetime = datetime.strptime(end_time, time_format)
    else:
        end_datetime = end_time

    difference = end_datetime - start_datetime
    return int(difference.total_seconds() / 60)  # Convert to minutes


def get_range(items):
    """Gets the range of items."""
    return {"range": (min(items), max(items))}


def time_difference(items):
    """Calculates time difference between earliest and latest timestamp."""
    times = [datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in items]
    delta = max(times) - min(times)
    return {"time_difference": delta.total_seconds() / 60}


def get_counts(items):
    """Gets the counts of each unique item."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return {"counts": counts}


def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)


def count_lines_in_list(lst):
    """Returns the number of items in a list."""
    return len(lst)


def analyze_log_data(parsed_data, config):
    insights = {}
    for key, functions in config.items():
        for function in functions:
            items = [entry[key] for entry in parsed_data]
            result = function(items)
            if key in insights:
                insights[key].update(result)
            else:
                insights[key] = result
    return insights


clf_config = {
    "timestamp": [get_range, time_difference],
    "status": [get_counts],
    "ip": [get_counts]
}

systemd_config = {
    "timestamp": [get_range, time_difference],
    "hostname": [get_counts],
    "service": [get_counts],
    "pid": [get_counts]
}
