import re
from .base_parser import BaseParser


class SyslogParser(BaseParser):
    # Regulärer Ausdruck für das Parsen der Syslog-Nachricht
    pattern = re.compile(
        r'\<(?P<priority>\d{1,3})\>'     # PRI (Priority)
        r' (?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z)'  # TIMESTAMP
        r' (?P<hostname>[\w\-\.]+)'     # HOSTNAME
        r' (?P<appname>\w+)'            # APP-NAME
        r' (?P<procid>\-|\w+)'          # PROCID
        r' (?P<msgid>\-|\w+)'           # MSGID
        r' (?P<message>.*)'             # MESSAGE
    )
