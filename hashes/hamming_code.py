"""
Hamming Code -- a family of linear error-correcting codes.

Hamming codes can detect up to two-bit errors or correct one-bit errors
without detection of uncorrected errors. By contrast, the simple parity
code cannot correct errors, and can detect only an odd number of bits
in error.

The implementation consists of:
  - emitter_converter: encodes a message with parity bits
  - receptor_converter: decodes and verifies data integrity
  - text_to_bits / text_from_bits: binary conversion utilities

source: https://en.wikipedia.org/wiki/Hamming_code
"""

import math


def text_to_bits(text: str, encoding: str = "utf-8", errors: str = "surrogatepass") -> str:
    """
    Convert text string to binary string.

    >>> text_to_bits("msg")
    '011011010111001101100111'
    >>> text_to_bits("A")
    '01000001'
    """
    bits = bin(int.from_bytes(text.encode(encoding, errors), "big"))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def text_from_bits(bits: str, encoding: str = "utf-8", errors: str = "surrogatepass") -> str:
    """
    Convert binary string back to text.

    >>> text_from_bits('011011010111001101100111')
    'msg'
    >>> text_from_bits('01000001')
    'A'
    """
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, "big").decode(encoding, errors) or "\0"


def emitter_converter(size_par: int, data: str) -> list[str]:
    """
    Encode data bits with Hamming parity bits.

    :param size_par: number of parity bits
    :param data: information bits as a string of '0's and '1's
    :return: encoded message with parity bits inserted

    >>> emitter_converter(4, "101010111111")
    ['1', '1', '1', '1', '0', '1', '0', '0', '1', '0', '1', '1', '1', '1', '1', '1']
    >>> emitter_converter(5, "101010111111")
    Traceback (most recent call last):
        ...
    ValueError: size of parity don't match with size of data
    """
    if size_par + len(data) <= 2**size_par - (len(data) - 1):
        raise ValueError("size of parity don't match with size of data")

    data_out = []
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data) + 1)]

    data_ord = []
    data_out_gab = []
    qtd_bp = 0
    cont_data = 0

    for x in range(1, size_par + len(data) + 1):
        if qtd_bp < size_par:
            if math.log2(x).is_integer():
                data_out_gab.append("P")
                qtd_bp += 1
            else:
                data_out_gab.append("D")
        else:
            data_out_gab.append("D")

        if data_out_gab[-1] == "D":
            data_ord.append(data[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    for bp in range(1, size_par + 1):
        cont_bo = 0
        for cont_loop, x in enumerate(data_ord):
            if x is not None:
                try:
                    aux = bin_pos[cont_loop][-bp]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
        parity.append(cont_bo % 2)

    cont_bp = 0
    for x in range(size_par + len(data)):
        if data_ord[x] is None:
            data_out.append(str(parity[cont_bp]))
            cont_bp += 1
        else:
            data_out.append(data_ord[x])

    return data_out


def receptor_converter(size_par: int, data: str) -> tuple[list[str], bool]:
    """
    Decode a Hamming-encoded message and check integrity.

    :param size_par: number of parity bits
    :param data: received message as string
    :return: tuple of (data bits, integrity check passed)

    >>> receptor_converter(4, "1111010010111111")
    (['1', '0', '1', '0', '1', '0', '1', '1', '1', '1', '1', '1'], True)
    """
    data_out_gab = []
    qtd_bp = 0
    parity_received = []
    data_output = []

    for i, item in enumerate(data, 1):
        if qtd_bp < size_par and math.log2(i).is_integer():
            data_out_gab.append("P")
            qtd_bp += 1
        else:
            data_out_gab.append("D")

        if data_out_gab[-1] == "D":
            data_output.append(item)
        else:
            parity_received.append(item)

    # Recalculate parity
    parity = []
    bin_pos = [bin(x)[2:] for x in range(1, size_par + len(data_output) + 1)]

    data_ord = []
    data_out_gab2 = []
    qtd_bp = 0
    cont_data = 0

    for x in range(1, size_par + len(data_output) + 1):
        if qtd_bp < size_par and math.log2(x).is_integer():
            data_out_gab2.append("P")
            qtd_bp += 1
        else:
            data_out_gab2.append("D")

        if data_out_gab2[-1] == "D":
            data_ord.append(data_output[cont_data])
            cont_data += 1
        else:
            data_ord.append(None)

    for bp in range(1, size_par + 1):
        cont_bo = 0
        for cont_loop, x in enumerate(data_ord):
            if x is not None:
                try:
                    aux = bin_pos[cont_loop][-bp]
                except IndexError:
                    aux = "0"
                if aux == "1" and x == "1":
                    cont_bo += 1
        parity.append(str(cont_bo % 2))

    ack = parity_received == parity
    return data_output, ack


if __name__ == "__main__":
    import doctest

    doctest.testmod()
