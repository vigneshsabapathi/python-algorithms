"""
One of the several implementations of Lempel-Ziv-Welch decompression algorithm
https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

This module provides the decompression counterpart to lempel_ziv.py.
It reads a compressed binary file, removes the Elias gamma prefix,
decompresses the data using the LZW algorithm, and writes the result.

For interview-friendly in-memory decompress, see lempel_ziv.lzw_decompress().
"""

from __future__ import annotations

import math
import sys


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


def decompress_data(data_bits: str) -> str:
    """
    Decompresses given data_bits using Lempel-Ziv-Welch compression algorithm
    and returns the result as a string.

    >>> decompress_data("01")
    '0'
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
        lexicon[curr_string] = last_match_id + "0"

        if math.log2(index).is_integer():
            new_lex = {}
            for curr_key in list(lexicon):
                new_lex["0" + curr_key] = lexicon.pop(curr_key)
            lexicon = new_lex

        lexicon[bin(index)[2:]] = last_match_id + "1"
        index += 1
        curr_string = ""
    return result


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

            for elem in result_byte_array[:-1]:
                opened_file.write(int(elem, 2).to_bytes(1, byteorder="big"))
    except OSError:
        print("File not accessible")
        sys.exit()


def remove_prefix(data_bits: str) -> str:
    """
    Removes size prefix that compressed file should have.

    >>> remove_prefix("0011010data")
    '10data'
    """
    counter = 0
    for letter in data_bits:
        if letter == "1":
            break
        counter += 1

    data_bits = data_bits[counter:]
    data_bits = data_bits[counter + 1 :]
    return data_bits


def decompress(source_path: str, destination_path: str) -> None:
    """
    Reads source file, decompresses it and writes the result in destination file.
    """
    data_bits = read_file_binary(source_path)
    data_bits = remove_prefix(data_bits)
    decompressed = decompress_data(data_bits)
    write_file_binary(destination_path, decompressed)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
