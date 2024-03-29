import argparse
import os
import re
import json

def load_patterns(pattern_file):
    with open(pattern_file, 'r') as file:
        data = json.load(file)
    return data['patterns']

def find_sensitive_data(filepath, encoding, patterns):

    matches = []
    with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
        for line_number, line in enumerate(file, 1):  # Start counting from line 1
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((line_number, line.strip()))
    return matches

def process_file(filepath, encoding, patterns, output_file=None):
    output = f"Processing file: {filepath}"
    print(output)
    if output_file:
        with open(output_file, 'w') as f:
            f.write(output + '\n')
    matches = find_sensitive_data(filepath, encoding, patterns)
    for line_number, match in matches:
        output = f"\tPossible sensitive data found on line {line_number}: {match}"
        print(output)

        if output_file:
            with open(output_file, 'w') as f:
                f.write(output + '\n')
    return {"matches": matches, "line_number": line_number}

def process_directory(directory, patterns, encoding='utf-8', output_file=None):
    for root, _, files in os.walk(directory):
        for file in files:
            process_file(os.path.join(root, file), encoding, patterns, output_file)


def main():
    parser = argparse.ArgumentParser(description="Scan files or directories for sensitive data.")
    parser.add_argument('path', type=str, help="Path to the file or directory to scan.")
    parser.add_argument('-r', '--recursive', action='store_true', help="Recursively scan directories.")
    parser.add_argument('-e', '--encoding', type=str, default='utf-8', help="File encoding (defaults to utf-8).")
    parser.add_argument('-p', '--patterns', type=str, help="JSON file containing patterns to search for.")
    parser.add_argument('-t', '--text', type=str, help="Generate a text file output with the specified filename.")


    args = parser.parse_args()
    
    patterns = [
        r'\bpassword\s*=\s*.+',  # Matches simple password assignments
        r'\buser(name)?\s*=\s*.+',  # Matches simple username assignments
    ]

    if args.text and not args.text.strip():
        print("Please provide a filename for the text output.")
        return

    if args.patterns:
        patterns = load_patterns(args.patterns)

    if os.path.isdir(args.path) and args.recursive:
        process_directory(args.path, patterns, args.encoding, args.text)

    elif (not os.path.isdir(args.path)) and args.recursive:
        print("The specified path is not a directory")

    elif os.path.isfile(args.path):
        process_file(args.path, args.encoding, patterns, args.text)

    else:
        print("The specified path does not exist.")

if __name__ == "__main__":
    main()
