import argparse
from parsers.log_format import LogFormat
from utils import *


def parse_arguments():
    """
    Capture and process user inputs.

    Returns:
        args: A Namespace object containing the provided arguments.
    """
    parser = argparse.ArgumentParser(
        description="LogLoom: A tool for parsing log files.")

    # Argument for the path to the log file
    parser.add_argument('file_path', type=str,
                        help='Path to the log file to be parsed.')

    # Argument for the log format (e.g., "CLF", "Syslog", ...)
    parser.add_argument('-f', '--format', type=str, choices=[
                        log_format.value for log_format in LogFormat], default=LogFormat.CLF.value, help='The format of the log file.')

    # Optional: Additional arguments, such as filter options, can be added here.
    parser.add_argument('-p', '--print', action='store_true',
                        help='Just print the parsed log file.')

    args = parser.parse_args()
    return args


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
    while True:
        choice = input(
            "\nEnter numbers corresponding to keys from the list above separated by commas (e.g., '1,3') to view their data, or 'q' to quit: ")

        # Remove trailing comma, if present
        if choice.endswith(","):
            choice = choice[:-1]

        if choice == 'q':
            return 'q'

        selected_keys = []
        invalid_choice = False
        for ch in choice.split(","):
            ch = ch.strip()
            if ch.isdigit() and 1 <= int(ch) <= len(keys):
                selected_keys.append(keys[int(ch) - 1])
            else:
                print(
                    f"Invalid choice: '{ch}'. Please select valid numbers or 'q' to quit.")
                invalid_choice = True
                break  # Break out of the loop if an invalid choice is found

        if not invalid_choice:
            return selected_keys


def print_selected_data(parsed_data, selected_keys):
    """
    Print the values of the selected keys from the parsed data.

    Args:
        parsed_data (list): List of dictionaries containing the parsed log entries.
        selected_keys (list): List of selected keys to print.
    """
    for entry in parsed_data:
        # Create a list of the values for each selected key and join them with the separator
        values_to_print = [entry[key] for key in selected_keys]
        print("  |  ".join(values_to_print))


def user_interaction(parsed_data):
    """
    Interact with the user: display available keys, get user's choice, and display selected data.

    Args:
        parsed_data (list): Parsed log data.
    """
    keys = list(parsed_data[0].keys())
    while True:
        display_available_keys(keys)
        selected_keys = get_user_choice(keys)

        if selected_keys == 'q':
            print("Exiting the program. Goodbye!")
            break
        if not selected_keys:
            continue
        print_selected_data(parsed_data, selected_keys)
