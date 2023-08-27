# Import necessary functions and modules
from cli import parse_arguments
from utils import read_log_file, print_log_lines
from parsers import get_parser_for_format

def main():
    try:    
        # Capture CLI arguments
        args = parse_arguments()
        
        # Check if you just want to print the file lines or parse them
        if args.print:  # Assuming you have a --print option in your CLI
            print_log_lines(args.file_path)
            return

        # Get the appropriate parser based on the format
        parser = get_parser_for_format(args.format)

        # Read the log file and parse lines
        parsed_data = []
        for line in read_log_file(args.file_path):
            parsed_line = parser.parse_line(line)
            if parsed_line:  # Filter out possible None results
                parsed_data.append(parsed_line)

        # Further process the parsed data as needed
        # For instance, you might insert them into a database, save in a file, etc.

        # For now, just print the parsed data
        for entry in parsed_data:
            print(entry)

    except FileNotFoundError as e:
        print(f"Fehler: {e}")
    except ValueError as e:  # Dies könnte z.B. durch das `get_parser_for_format` ausgelöst werden.
        print(f"Ungültiger Wert: {e}")
    except Exception as e:   # Dies fängt allgemeine Fehler ab
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    main()
