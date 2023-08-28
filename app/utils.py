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


def display_available_keys(keys):
    """
    Display the available keys in the parsed data.

    Args:
        keys (list): List of keys available in the parsed data.
    """
    print("\nAvailable keys in the parsed data:")
    for idx, key in enumerate(keys, 1):
        print(f"{idx}. {key}")


def get_user_choice(keys):
    """
    Prompt the user to select keys by entering their corresponding numbers.

    Args:
        keys (list): List of keys available in the parsed data.

    Returns:
        list or None: List of selected keys or None if the user chooses to quit.
    """
    choice = input(
        "\nEnter numbers corresponding to keys from the list above separated by commas (e.g., '1,3') to view their data, or 'q' to quit: ")

    # Remove trailing comma, if present
    if choice.endswith(","):
        choice = choice[:-1]

    if choice == 'q':
        return 'q'

    selected_keys = []
    for ch in choice.split(","):
        ch = ch.strip()
        if ch.isdigit() and 1 <= int(ch) <= len(keys):
            selected_keys.append(keys[int(ch) - 1])
        else:
            print("Invalid choice. Please select valid numbers or 'q' to quit.")
            return []  # Returning an empty list to indicate invalid choice

    return selected_keys


def print_selected_data(parsed_data, selected_keys):
    """
    Print the values of the selected keys from the parsed data.

    Args:
        parsed_data (list): List of dictionaries containing the parsed log entries.
        selected_keys (list): List of selected keys to print.
    """
    for entry in parsed_data:
        for key in selected_keys:
            # Separator between values
            print(entry[key], end="  |  ")
        print()  # Separator between entries
