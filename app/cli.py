import argparse
from parsers.log_format import LogFormat

def parse_arguments():
    """
    Capture and process user inputs.
    
    Returns:
        args: A Namespace object containing the provided arguments.
    """
    parser = argparse.ArgumentParser(description="LogLoom: A tool for parsing log files.")

    # Argument for the path to the log file
    parser.add_argument('file_path', type=str, help='Path to the log file to be parsed.')

    # Argument for the log format (e.g., "CLF", "Syslog", ...)
    parser.add_argument('-f', '--format', type=str, choices=[log_format.value for log_format in LogFormat], default=LogFormat.CLF.value, help='The format of the log file.')

    # Optional: Additional arguments, such as filter options, can be added here.
    parser.add_argument('-p', '--print', action='store_true', help='Just print the parsed log file.')

    args = parser.parse_args()
    return args

