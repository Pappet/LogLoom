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
