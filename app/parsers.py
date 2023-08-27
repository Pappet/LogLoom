import re

class BaseParser:
    """
    Base parser class. All format-specific parsers should inherit from this class.
    """
    def parse_line(self, line):
        raise NotImplementedError("Each parser must implement the 'parse_line' method.")

class CLFParser(BaseParser):
    """
    Parser for the Common Log Format (CLF).
    """
    # Regular expression to match the CLF format
    pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) (\S+) (\S+) \[(.*?)\] "(.*?)" (\d+) (\d+|-)')
    
    # Regular expression to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    
    def parse_line(self, line):
        # Remove ANSI escape codes
        line = self.ansi_escape.sub('', line)
        
        match = self.pattern.match(line)
        if match:
            return {
                'ip': match.group(1),
                'remote_log_name': match.group(2),  # often '-'
                'user_id': match.group(3),  # authenticated user, '-' if not authenticated
                'date_time': match.group(4),  # with timezone offset
                'request': match.group(5),
                'status': match.group(6),
                'bytes_sent': match.group(7)  # '-' means unavailable data
            }
        return None

# More parsers like SyslogParser can be added here...
class SyslogParser(BaseParser):
    # Regulärer Ausdruck für das Parsen der Syslog-Nachricht
    pattern = re.compile(r'\<(\d+)\>([A-Za-z]{3} \d{1,2} \d{1,2}:\d{1,2}:\d{1,2}) ([\w\-\.]+) (\w+): (.*)')

    def parse_line(self, line):
        match = self.pattern.match(line)
        if match:
            return {
                'priority': int(match.group(1)),
                'timestamp': match.group(2),
                'hostname': match.group(3),
                'app': match.group(4),
                'message': match.group(5)
            }
        else:
            return None

class SyslogFedoraParser:
    # Regular expression to parse the syslog format
    pattern = re.compile(
            r'(?P<timestamp>\w{3} \d{1,2} \d{2}:\d{2}:\d{2}) '  # Timestamp
            r'(?P<hostname>\S+) '                               # Hostname
            r'(?P<service>\S+): '                               # Service/Program
            r'(?P<message>.+)'                                  # Message
        )

    def parse_line(self, line):
        match = self.pattern.match(line)
        if match:
            return match.groupdict()
        else:
            return None


def get_parser_for_format(log_format):
    """
    Return the appropriate parser for a given log format.
    
    Args:
        log_format (str): The format of the log (e.g., "CLF", "Syslog").
    
    Returns:
        BaseParser: An instance of the appropriate parser.
    """
    if log_format == "CLF":
        return CLFParser()
    # Add more formats as needed, e.g.:
    elif log_format == "Syslog":
        return SyslogParser()
    elif log_format == "Fedora":
        return SyslogFedoraParser()
    else:
        raise ValueError(f"Unsupported log format: {log_format}")
