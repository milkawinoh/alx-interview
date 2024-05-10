#!/usr/bin/python3
def validUTF8(data):
    """
    Validate whether a given list of integers represents a
    valid UTF-8 encoding.

    Parameters:
    - data (list of int): A list of integers representing bytes of data.

    Returns:
    - bool: True if data is a valid UTF-8 encoding, False otherwise.
    Algorithm:
    1. Initialize a counter to track expected number of bytes.
    2. Iterate through each byte in the data list.
    3. Check if the byte is the start of a UTF-8 sequence:
        - If yes, determine the number of bytes to follow based on
        the leading bits.
        - If no, check if it's a continuation byte and validate accordingly.
    4. Return True if the entire data represents a valid UTF-8 encoding,
    otherwise False.

    UTF-8 Encoding Rules:
    - Single-byte character (ASCII): Leading bit is 0 (0xxxxxxx).
    - Two-byte character: Leading bits are 110 (110xxxxx).
    - Three-byte character: Leading bits are 1110 (1110xxxx).
    - Four-byte character: Leading bits are 11110 (11110xxx).
    - Continuation byte: Leading bits are 10 (10xxxxxx).

    Example Usage:
    >>> data = [65]
    >>> validUTF8(data)
    True
    >>> data = [80, 121, 116, 104, 111, 110, 32, 105, 115, 32, 99]
    >>> validUTF8(data)
    True
    >>> data = [229, 65, 127, 256]
    >>> validUTF8(data)
    False
    """
    # Implementation of UTF-8 validation algorithm
    num_bytes_to_follow = 0
    for byte in data:
        if num_bytes_to_follow == 0:
            if byte >> 7 == 0b0:
                num_bytes_to_follow = 0
            elif byte >> 5 == 0b110:
                num_bytes_to_follow = 1
            elif byte >> 4 == 0b1110:
                num_bytes_to_follow = 2
            elif byte >> 3 == 0b11110:
                num_bytes_to_follow = 3
            else:
                return False
        else:
            if byte >> 6 != 0b10:
                return False
            num_bytes_to_follow -= 1
            if num_bytes_to_follow == -1:
                return False
    return num_bytes_to_follow == 0
