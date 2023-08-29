import argparse
from parsers.log_format import LogFormat
from parsers.clf_parser import analyze_clf_data
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
                        help='Just print the log file without parsing.')

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
    print("0. EVERYTHING")


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

        # q for closing the app
        if choice == 'q':
            return 'q'

        # 0 for getting all keys
        if choice == '0':
            return keys

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


def print_selected_data(parsed_data, selected_keys, max_width=50):
    """
    Print the values of the selected keys from the parsed data with adjusted width.

    Args:
        parsed_data (list): List of dictionaries containing the parsed log entries.
        selected_keys (list): List of selected keys to print.
        max_width (int): Maximum width for any column.
    """

    # Step 1: Determine the maximum width for each key
    key_widths = {}
    for key in selected_keys:
        # Getting the max length of the values associated with a key
        max_length = max(len(str(entry[key])) for entry in parsed_data)
        # Include the key's own length in the consideration
        max_length = max(max_length, len(key))
        # Limiting the width to the max_width parameter
        key_widths[key] = min(max_length, max_width)

    # Print a separator
    print('-' * (sum(key_widths.values()) + len(selected_keys) * 5 - 3))
    # Print the headers (keys) first
    header_values = [key.ljust(key_widths[key]) for key in selected_keys]
    print("  |  ".join(header_values))
    # Print a separator
    print('-' * (sum(key_widths.values()) + len(selected_keys) * 5 - 3))

    # Step 2: Print the data using the determined widths
    for entry in parsed_data:
        formatted_values = [str(entry[key]).ljust(key_widths[key])
                            for key in selected_keys]
        print("  |  ".join(formatted_values))


def user_interaction2(parsed_data):
    """
    Interact with the user: display available keys, get user's choice, and display selected data.

    Args:
        parsed_data (list): Parsed log data.
    """
    # Welcome text
    display_welcome_message()

    # Print the analyzed log file
    analyze_clf_data(parsed_data)

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


def user_interaction(parsed_data):
    """
    Interact with the user: display available keys, get user's choice, and display selected data.

    Args:
        parsed_data (list): Parsed log data.
    """
    # Welcome text
    display_welcome_message()

    action = input(
        "Would you like to (A)nalyze the log or (S)elect keys to view? Enter 'A' or 'S'. Or enter 'Q' to quit: ").lower()

    if action == 'q':
        print("Exiting the program. Goodbye!")
        return

    if action == 'a':
        # Print the analyzed log file
        analyze_clf_data(parsed_data)

    elif action == 's':
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
    else:
        print("Invalid choice. Please select 'A' or 'S'.")
