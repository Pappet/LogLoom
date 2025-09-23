import re

class BaseParser:
    # Regular expression to match ANSI escape codes
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    """
    Base parser class. All format-specific parsers should inherit from this class.
    """
    def parse_line(self, line):
        """
        Removes ANSI codes and then matches the line against the parser's pattern.
        """
        # First, remove any ANSI escape codes from the entire line.
        cleaned_line = self.ansi_escape.sub('', line)
        
        # Then, try to match the pattern on the cleaned line.
        match = self.pattern.match(cleaned_line)
        if match:
            return match.groupdict()
        else:
            return None