#!/usr/bin/python3

import sys
import re
import signal

total_file_size = 0
status_code_counts = {}

def parse_log_entry(line):
    pattern = r'^([\d\.]+) - \[(.*?)\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)'
    match = re.match(pattern, line)
    if match:
        ip_address = match.group(1)
        status_code = int(match.group(3))
        file_size = int(match.group(4))
        return ip_address, status_code, file_size
    return None

def print_statistics():
    print(f"Total file size: {total_file_size}")
    for code in sorted(status_code_counts):
        print(f"{code}: {status_code_counts[code]}")

def signal_handler(sig, frame):
    print_statistics()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

line_count = 0

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
