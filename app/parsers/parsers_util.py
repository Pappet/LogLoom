from .log_format import LogFormat
from .clf_parser import CLFParser
from .syslog_parser import SyslogParser
from .systemd_journal_parser import SystemdJournalParser
from .json_parser import JSONParser
from utils import read_log_file
from datetime import datetime
import re


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
    elif log_format == LogFormat.JSON.value:
        return JSONParser()
    else:
        raise ValueError(f"Unsupported log format: {log_format}")


def convert_to_standard_timestamp(timestamp_str, parser):
    """
    Convert given timestamp string to a standardized format.
    This version manually replaces month names to be locale-independent.

    Args:
        timestamp_str (str): Timestamp string to be converted.
        parser (BaseParser): The parser instance which holds the timestamp format(s).

    Returns:
        str: Converted timestamp string in the format "YYYY-MM-DD HH:MM:SS".
    """
    # Define a mapping for English month abbreviations
    month_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    # Use regex to find and replace the month abbreviation
    # This is safer than a simple string replace
    month_search = re.search(r"([A-Z][a-z]{2})", timestamp_str)
    if month_search:
        month_abbr = month_search.group(1)
        if month_abbr in month_map:
            # Replace the month name with its number
            timestamp_str = timestamp_str.replace(month_abbr, month_map[month_abbr])
            # Adjust the format strings to expect a numeric month (%m)
            formats_to_try = [fmt.replace('%b', '%m') for fmt in getattr(parser, 'timestamp_formats', [])]
        else:
            formats_to_try = getattr(parser, 'timestamp_formats', [])
    else:
        formats_to_try = getattr(parser, 'timestamp_formats', [])

    if isinstance(formats_to_try, str):
        formats_to_try = [formats_to_try]
        
    if not formats_to_try:
        return timestamp_str

    datetime_obj = None
    for fmt in formats_to_try:
        try:
            datetime_obj = datetime.strptime(timestamp_str, fmt)
            break
        except ValueError:
            continue
    print(f'{datetime_obj} and {timestamp_str} and {formats_to_try}')
    if datetime_obj is None:
        raise ValueError(f"Time data '{timestamp_str}' does not match any known format.")

    if parser.__class__.__name__ == "SystemdJournalParser":
        datetime_obj = datetime_obj.replace(year=datetime.now().year)

    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")


def process_log_file(file_path, format_type):
    """
    Select the appropriate parser based on the given format and process the file.

    Args:
        file_path (str): Path to the log file to be processed.
        format_type (str): Log file format.

    Returns:
        tuple: A tuple containing (list of parsed data, parser instance).
    """
    parser = get_parser_for_format(format_type)
    parsed_data = []
    line_number = 0
    for line in read_log_file(file_path):
        line_number += 1
        parsed_line = parser.parse_line(line)
        if parsed_line and 'timestamp' in parsed_line:
            try:
                parsed_line['timestamp'] = convert_to_standard_timestamp(
                    parsed_line['timestamp'], parser)
                parsed_data.append(parsed_line)
            except ValueError as e:
                print(f"Warning: Skipping line {line_number} due to timestamp error. Details: {e}")
                
    return parsed_data, parser