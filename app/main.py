# Import necessary functions and modules
from cli import parse_arguments
from utils import *
from parsers import parsers_util


def main():
    try:
        # Capture CLI arguments
        args = parse_arguments()

        # Check if you just want to print the file lines or parse them
        if args.print:  # Assuming you have a --print option in your CLI
            print_log_lines(args.file_path)
            return

        # Get the appropriate parser based on the format
        parser = parsers_util.get_parser_for_format(args.format)

        # Read the log file and parse lines
        parsed_data = []
        for line in read_log_file(args.file_path):
            parsed_line = parser.parse_line(line)
            if parsed_line:  # Filter out possible None results
                parsed_data.append(parsed_line)

        # If there's any parsed data, process further
        if parsed_data:
            keys = list(parsed_data[0].keys())

            while True:
                display_available_keys(keys)
                selected_keys = get_user_choice(keys)

                if selected_keys == 'q':  # User decided to quit
                    print("Exiting the program. Goodbye!")
                    break

                # If the user provides an invalid choice, continue with the loop to re-prompt
                if not selected_keys:
                    continue

                print_selected_data(parsed_data, selected_keys)
        else:
            print("No data was parsed from the log file.")

    except FileNotFoundError as e:
        print(f"Fehler: {e}")
    # Dies könnte z.B. durch das `get_parser_for_format` ausgelöst werden.
    except ValueError as e:
        print(f"Ungültiger Wert: {e}")
    except Exception as e:   # Dies fängt allgemeine Fehler ab
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


if __name__ == "__main__":
    main()
