def read_log_file(file_path):
    """
    Read a log file and return its lines.
    
    Args:
        file_path (str): Path to the log file to be read.
    
    Returns:
        list: List of lines from the log file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading the file '{file_path}': {e}")
        return []
    
def print_log_lines(file_path):
    """
    Print each line of the log file.
    
    Args:
        file_path (str): Path to the log file to be printed.
    """
    lines = read_log_file(file_path)
    
    if not lines:
        print(f"No content found in '{file_path}'.")
        return
    
    for line in lines:
        print(line, end="")  # The 'end=""' prevents double line breaks, as the lines will already have newline characters.
