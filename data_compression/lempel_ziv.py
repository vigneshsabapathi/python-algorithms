"""
One of the several implementations of Lempel-Ziv-Welch compression algorithm
https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

LZW compresses data by building a dictionary of previously seen sequences.
Instead of transmitting raw data, it transmits dictionary indices which are
shorter than the sequences they represent.

This module provides in-memory compress/decompress for string data, plus
the original file-based binary compress from TheAlgorithms.
"""

from __future__ import annotations

import math
import os
import sys


# ---------------------------------------------------------------------------
# In-memory string-based LZW (interview-friendly)
# ---------------------------------------------------------------------------

def lzw_compress(text: str) -> list[int]:
    """
    Compress a string using LZW algorithm.

    Returns a list of integer codes.

    >>> lzw_compress("ABABABA")
    [65, 66, 256, 258]
    >>> lzw_compress("TOBEORNOTTOBEORTOBEORNOT")
    [84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263]
    >>> lzw_compress("")
    []
    """
    if not text:
        return []

    # Initialize dictionary with single characters
    dictionary: dict[str, int] = {chr(i): i for i in range(256)}
    next_code = 256

    result: list[int] = []
    current = ""

    for char in text:
        current_plus = current + char
        if current_plus in dictionary:
            current = current_plus
        else:
            result.append(dictionary[current])
            dictionary[current_plus] = next_code
            next_code += 1
            current = char

    if current:
        result.append(dictionary[current])

    return result


def lzw_decompress(codes: list[int]) -> str:
    """
    Decompress a list of LZW codes back to the original string.

    >>> lzw_decompress([65, 66, 256, 258])
    'ABABABA'
    >>> lzw_decompress([84, 79, 66, 69, 79, 82, 78, 79, 84, 256, 258, 260, 265, 259, 261, 263])
    'TOBEORNOTTOBEORTOBEORNOT'
    >>> lzw_decompress([])
    ''
    """
    if not codes:
        return ""

    # Initialize dictionary with single characters
    dictionary: dict[int, str] = {i: chr(i) for i in range(256)}
    next_code = 256

    result = [dictionary[codes[0]]]
    previous = result[0]

    for code in codes[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = previous + previous[0]
        else:
            raise ValueError(f"Invalid LZW code: {code}")

        result.append(entry)
        dictionary[next_code] = previous + entry[0]
        next_code += 1
        previous = entry

    return "".join(result)


# ---------------------------------------------------------------------------
# Binary file-based compress (from TheAlgorithms)
# ---------------------------------------------------------------------------

def read_file_binary(file_path: str) -> str:
    """
    Reads given file as bytes and returns them as a long string of 0s and 1s.

    >>> import tempfile, os
    >>> f = tempfile.NamedTemporaryFile(delete=False, suffix='.bin')
    >>> _ = f.write(b'\\x41')
    >>> f.close()
    >>> read_file_binary(f.name)
    '01000001'
    >>> os.unlink(f.name)
    """
    result = ""
    try:
        with open(file_path, "rb") as binary_file:
            data = binary_file.read()
        for dat in data:
            curr_byte = f"{dat:08b}"
            result += curr_byte
        return result
    except OSError:
        print("File not accessible")
        sys.exit()


def add_key_to_lexicon(
    lexicon: dict[str, str], curr_string: str, index: int, last_match_id: str
) -> None:
    """
    Adds new strings (curr_string + "0",  curr_string + "1") to the lexicon.
    """
    lexicon.pop(curr_string)
    lexicon[curr_string + "0"] = last_match_id

    if math.log2(index).is_integer():
        for curr_key, value in lexicon.items():
            lexicon[curr_key] = f"0{value}"

    lexicon[curr_string + "1"] = bin(index)[2:]


def compress_data(data_bits: str) -> str:
    """
    Compresses given data_bits using LZW compression algorithm
    and returns the result as a string.

    >>> compress_data("01000001")  # doctest: +SKIP
    '...'
    """
    lexicon = {"0": "0", "1": "1"}
    result, curr_string = "", ""
    index = len(lexicon)

    for i in range(len(data_bits)):
        curr_string += data_bits[i]
        if curr_string not in lexicon:
            continue

        last_match_id = lexicon[curr_string]
        result += last_match_id
        add_key_to_lexicon(lexicon, curr_string, index, last_match_id)
        index += 1
        curr_string = ""

    while curr_string != "" and curr_string not in lexicon:
        curr_string += "0"

    if curr_string != "":
        last_match_id = lexicon[curr_string]
        result += last_match_id

    return result


def add_file_length(source_path: str, compressed: str) -> str:
    """
    Adds given file's length in front (using Elias gamma coding) of the
    compressed string.
    """
    file_length = os.path.getsize(source_path)
    file_length_binary = bin(file_length)[2:]
    length_length = len(file_length_binary)
    return "0" * (length_length - 1) + file_length_binary + compressed


def write_file_binary(file_path: str, to_write: str) -> None:
    """
    Writes given to_write string (should only consist of 0's and 1's)
    as bytes in the file.
    """
    byte_length = 8
    try:
        with open(file_path, "wb") as opened_file:
            result_byte_array = [
                to_write[i : i + byte_length]
                for i in range(0, len(to_write), byte_length)
            ]

            if len(result_byte_array[-1]) % byte_length == 0:
                result_byte_array.append("10000000")
            else:
                result_byte_array[-1] += "1" + "0" * (
                    byte_length - len(result_byte_array[-1]) - 1
                )

            for elem in result_byte_array:
                opened_file.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("File not accessible")
        sys.exit()


def compress(source_path: str, destination_path: str) -> None:
    """
    Reads source file, compresses it and writes the compressed result in
    destination file.
    """
    data_bits = read_file_binary(source_path)
    compressed = compress_data(data_bits)
    compressed = add_file_length(source_path, compressed)
    write_file_binary(destination_path, compressed)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
