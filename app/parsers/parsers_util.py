from .log_format import LogFormat
from .clf_parser import CLFParser
from .syslog_parser import SyslogParser
from .systemd_journal_parser import SystemdJournalParser

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
