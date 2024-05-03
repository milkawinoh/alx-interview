#!/usr/bin/python3

import sys
import re
import signal
from typing import Optional, Tuple, Dict

total_file_size: int = 0
status_code_counts: Dict[int, int] = {}


def parse_log_entry(line: str) -> Optional[Tuple[str, int, int]]:
    """
    Parse a log entry string and extract IP address, status code,
    and file size.

    Args:
        line (str): Log entry string to parse.

    Returns:
        Optional[Tuple[str, int, int]]: A tuple containing IP address,
        status code, and file size,
            or None if the log entry does not match the expected format.
    """
    patn = r'^([\d\.]+) - \[(.*?)\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)'
    match = re.match(patn, line)
    if match:
        ip_address = match.group(1)
        status_code = int(match.group(3))
        file_size = int(match.group(4))
        return ip_address, status_code, file_size
    return None


def print_statistics() -> None:
    """
    Print computed statistics: total file size and count of each status code.
    """
    print(f"Total file size: {total_file_size}")
    for code in sorted(status_code_counts):
        print(f"{code}: {status_code_counts[code]}")


def signal_handler(sig: int, frame) -> None:
    """
    Signal handler to print statistics and exit upon receiving SIGINT.

    Args:
        sig (int): Signal number.
        frame: Current stack frame (not used).
    """
    print_statistics()
    sys.exit(0)


def main() -> None:
    """
    Main function to read log entries from stdin, parse them,
    and compute statistics.
    """
    signal.signal(signal.SIGINT, signal_handler)
    line_count: int = 0

    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                log_entry = parse_log_entry(line)
                if log_entry:
                    _, status_code, file_size = log_entry
                    total_file_size += file_size
                    if status_code in status_code_counts:
                        status_code_counts[status_code] += 1
                    else:
                        status_code_counts[status_code] = 1
                    line_count += 1

                    if line_count % 10 == 0:
                        print_statistics()

    except KeyboardInterrupt:
        # Handle KeyboardInterrupt (Ctrl+C) gracefully
        print_statistics()
        sys.exit(0)


if __name__ == "__main__":
    main()
