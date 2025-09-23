import json
from .base_parser import BaseParser
from utils import get_range, time_difference, get_counts

class JSONParser(BaseParser):
    """
    Parser for log files where each line is a JSON object.
    """

    # For JSON, we don't use a regex pattern. We override parse_line instead.
    pattern = None

    # Analysis configuration for common JSON log fields
    analysis_config = {
        "level": [get_counts],
        "service": [get_counts],
    }

    def parse_line(self, line):
        """
        Overrides the base method to parse a line as a JSON object.

        Args:
            line (str): A single line from the log file.

        Returns:
            dict or None: A dictionary representing the log entry, or None if parsing fails.
        """
        # Skip empty lines
        if not line.strip():
            return None

        try:
            # The core of the parser: load the line as a JSON object
            data = json.loads(line)
            
            # It's good practice to normalize common keys. For example, some logs
            # might use 'time' or 'ts' instead of 'timestamp'. We can handle that here.
            if 'time' in data and 'timestamp' not in data:
                data['timestamp'] = data.pop('time')
            if 'ts' in data and 'timestamp' not in data:
                data['timestamp'] = data.pop('ts')

            return data
        except json.JSONDecodeError:
            # If a line is not valid JSON, we simply ignore it.
            # Alternatively, you could log a warning here.
            return None