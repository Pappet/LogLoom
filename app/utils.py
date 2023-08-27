def read_log_file(file_path):
    """
    Read a log file and yield its lines.
    
    Args:
        file_path (str): Path to the log file to be read.
    
    Yields:
        str: A line from the log file.
    """
    with open(file_path, 'r') as file:
        for line in file:
            yield line


def print_log_lines(file_path):
    """
    Print each line of the log file.
    
    Args:
        file_path (str): Path to the log file to be printed.
    """
    for line in read_log_file(file_path):
        print(line, end="")  # Prevents double line breaks
