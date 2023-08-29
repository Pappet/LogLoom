from .log_format import LogFormat
from .clf_parser import CLFParser
from .syslog_parser import SyslogParser
from .systemd_journal_parser import SystemdJournalParser
from utils import read_log_file


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
            parsed_data.append(parsed_line)
    return parsed_data
