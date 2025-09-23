import argparse
from parsers.log_format import LogFormat
from parsers.clf_parser import analyze_clf_data
from utils import *
from output_cli import display_insights


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


def get_user_input(prompt, valid_choices=None, validation_func=None):
    """
    Prompt the user for input and validate it.

    Args:
        prompt (str): Message to display to the user.
        valid_choices (list or None): List of valid choices if applicable, None otherwise.
        validation_func (func): Optional validation function to provide custom validation.

    Returns:
        str: User's input.
    """
    while True:
        choice = input(prompt).strip().lower()

        # Check against valid_choices
        if valid_choices and choice not in valid_choices:
            print("Invalid choice. Please try again.")
            continue

        # Check with validation_func
        if validation_func:
            is_valid, message = validation_func(choice)
            if not is_valid:
                print(message)
                continue

        return choice


def validate_choice_for_keys(choice, keys):
    """
    Validate user choice for keys selection.

    Args:
        choice (str): User's choice to validate.
        keys (list): List of keys for validation context.

    Returns:
        tuple: (is_valid (bool), message (str))
    """
    if choice == 'q' or choice == '0':
        return True, ""

    for ch in choice.split(","):
        ch = ch.strip()
        if not ch.isdigit() or not (1 <= int(ch) <= len(keys)):
            return False, f"Invalid choice: '{ch}'. Use numbers from the list or 'q'."

    return True, ""


def get_user_choice(keys):
    """
    Prompt the user to select keys by entering their corresponding numbers.

    Args:
        keys (list): List of keys available in the parsed data.

    Returns:
        list or str: List of selected keys or 'q' if the user chooses to quit.
    """
    prompt = ("\nChoose keys to view by entering their numbers separated by commas (e.g., '1,3'). "
              "Enter '0' for all keys or 'q' to return to the main menu: ")

    while True:
        choice = get_user_input(
            prompt, validation_func=lambda x: validate_choice_for_keys(x, keys))

        if choice == 'q':
            return 'q'

        if choice == '0':
            return keys

        selected_keys = [keys[int(ch) - 1]
                         for ch in choice.split(",") if ch.strip().isdigit()]
        return selected_keys


def user_interaction(parsed_data, args):
    """
    Interact with the user: display available keys, get user's choice, and display selected data.

    Args:
        parsed_data (list): Parsed log data.
    """
    display_welcome_message()

    valid_choices = ['a', 's', 'q', 'w']
    prompt = "Would you like LogLoom to (A)nalyze the log, (S)elect keys to view or display the (W)elcome Message? Enter 'a', 's' or 'w'. Or enter 'q' to quit: "

    while True:
        action = get_user_input(prompt, valid_choices)

        if action == 'q':
            print("Exiting the program. Goodbye!")
            break

        if action == 'a':
            insights = analyze_log_data(parsed_data, systemd_config)
            lines_in_file = count_lines_in_file(args.file_path)
            lines_in_parsed_data = count_lines_in_list(parsed_data)
            display_insights(insights, lines_in_file, lines_in_parsed_data)
            # analyze_clf_data(parsed_data)
        elif action == 's':
            keys = list(parsed_data[0].keys())
            while True:
                display_available_keys(keys)
                selected_keys = get_user_choice(keys)

                if selected_keys == 'q':
                    print("Returning to main menu.")
                    break
                if not selected_keys:
                    continue
                print_selected_data(parsed_data, selected_keys)
        elif action == 'w':
            display_welcome_message()
