import re

class BaseParser:
    # Regular expression to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    """
    Base parser class. All format-specific parsers should inherit from this class.
    """
    def parse_line(self, line):
        # Remove ANSI escape codes
        line = self.ansi_escape.sub('', line)
        
        match = self.pattern.match(line)
        if match:
            return match.groupdict()
        else:
            return None