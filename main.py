import argparse
import os
import re

def find_sensitive_data(filepath, encoding):
    patterns = [
        r'\bpassword\s*=\s*.+',  # Matches simple password assignments
        r'\buser(name)?\s*=\s*.+',  # Matches simple username assignments
    ]
    matches = []
    with open(filepath, 'r', encoding=encoding, errors='ignore') as file:
        for line_number, line in enumerate(file, 1):  # Start counting from line 1
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    matches.append((line_number, line.strip()))
    return matches

def process_file(filepath, encoding):
    print(f"Processing file: {filepath}")
    matches = find_sensitive_data(filepath, encoding)
    for line_number, match in matches:
        print(f"Possible sensitive data found on line {line_number}: {match}")
    return {"matches": matches, "line_number": line_number}

def process_directory(directory, encoding='utf-8'):
    for root, _, files in os.walk(directory):
        for file in files:
            process_file(os.path.join(root, file), encoding)


def main():
    parser = argparse.ArgumentParser(description="Scan files or directories for sensitive data.")
    parser.add_argument('path', type=str, help="Path to the file or directory to scan.")
    parser.add_argument('-r', '--recursive', action='store_true', help="Recursively scan directories.")
    parser.add_argument('-e', '--encoding', type=str, default='utf-8', help="File encoding (defaults to utf-8).")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.path) and args.recursive:
        process_directory(args.path, args.encoding)

    elif (not os.path.isdir(args.path)) and args.recursive:
        print("The specified path is not a directory")

    elif os.path.isfile(args.path):
        process_file(args.path, args.encoding)

    else:
        print("The specified path does not exist.")

if __name__ == "__main__":
    main()
