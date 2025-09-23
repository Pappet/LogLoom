from .log_format import LogFormat
from .clf_parser import CLFParser
from .syslog_parser import SyslogParser
from .systemd_journal_parser import SystemdJournalParser
from utils import read_log_file
from datetime import datetime


def get_parser_for_format(log_format):
    """
    Return the appropriate parser for a given log format.

    Args:
        log_format (str): The format of the log (e.g., "CLF", "Syslog").

    Returns:
        BaseParser: An instance of the appropriate parser.
    """
    if log_format == LogFormat.CLF.value:
        return CLFParser()
    elif log_format == LogFormat.SYSLOG.value:
        return SyslogParser()
    elif log_format == LogFormat.SYSTEMD.value:
        return SystemdJournalParser()
    else:
        raise ValueError(f"Unsupported log format: {log_format}")


def convert_to_standard_timestamp(timestamp_str, format_type):
    """
    Convert given timestamp string to a standardized format.

    Args:
        timestamp_str (str): Timestamp string to be converted.
        format_type (str): Type of log format to determine the original timestamp format.

    Returns:
        str: Converted timestamp string in the format "YYYY-MM-DD HH:MM:SS".
    """
    if format_type == "Systemd":
        original_format = "%b %d %H:%M:%S"
    elif format_type == "CLF":
        original_format = "%d/%b/%Y:%H:%M:%S %z"
    else:
        raise ValueError("Unknown format type")

    datetime_obj = datetime.strptime(timestamp_str, original_format)
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


def process_log_file(file_path, format_type):
    """
    Select the appropriate parser based on the given format and process the file.

    Args:
        file_path (str): Path to the log file to be processed.
        format_type (str): Log file format.

    Returns:
        list: A list of parsed data.
    """
    parser = get_parser_for_format(format_type)
    parsed_data = []
    for line in read_log_file(file_path):
        parsed_line = parser.parse_line(line)
        if parsed_line:
            # Convert the timestamp
            timestamp_key = "timestamp" if format_type == "Systemd" else "timestamp"
            parsed_line[timestamp_key] = convert_to_standard_timestamp(
                parsed_line[timestamp_key], format_type)
            parsed_data.append(parsed_line)
    return parsed_data
