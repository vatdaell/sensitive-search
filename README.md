# 🕵️ Sensitive Search

Sensitive search is a configurable cli tool to find sensitive information stored in files such as passwords and usernames that need to be stored in an environment variable or vault.

## Installation

### Prerequisites

* Python 3.6 or later
* Git

### Clone Repository

```bash
git clone https://github.com/vatdaell/sensitive-search.git
```

### Basic Usage

To scan a single file for sensitive data:

```bash
python main.py path/to/your/file.txt
```

### Scan a Directory Recursively

To scan an entire directory and its subdirectories for sensitive data:

```bash
python main.py -r path/to/your/directory 
```

### Specify File Encoding

If your file uses a specific encoding, you can specify it with the `-e` or `--encoding` option, the default encoding is UTF-8:

```bash
python main.py path/to/your/file.txt -e encoding
```

For example, to use UTF-8 encoding:

```bash
python script.py path/to/your/file.txt -e utf-8
```

### Use Custom Patterns from a JSON File

To use custom patterns for scanning, specify a JSON file containing your patterns with the `-p` or `--patterns` option:

```bash
python main.py path/to/your/file.txt -p path/to/your/patterns.json
```

patterns.json

```json
{
  "patterns": [
    "\\bpassword\\s*=\\s*.+",
    "\\buser(name)?\\s*=\\s*.+",
    "...other patterns..."
  ]
}
```

### Generate a Text File Output

To generate a text file output of the scan results, use the `-t` or `--text` option followed by the desired output filename:

```bash
python main.py path/to/your/file.txt -t output.txt
```

## Note

Please ensure that the paths to files or directories, pattern JSON file, and output text file are correctly specified according to your filesystem.
