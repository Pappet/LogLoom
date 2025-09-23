# Import necessary functions and modules
from cli import *
from utils import *
from parsers import parsers_util


def main():
    """
    Main entry point for the log parser.
    """
    try:
        args = parse_arguments()

        # Check if the user just wants to print the file or parse it
        if args.print:
            print_log_lines(args.file_path)
            return

        parsed_data, parser_instance = parsers_util.process_log_file(
            args.file_path, args.format)

        # If there's any parsed data, proceed with user interaction
        if parsed_data:
            user_interaction(parsed_data, args, parser_instance)
        else:
            print("No data was parsed from the log file. Check the file format and content.")
    # Handle possible exceptions
    except FileNotFoundError:
        print(f"Error: The file '{args.file_path}' was not found.")
    except ValueError as e:
        print(f"Invalid value: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()