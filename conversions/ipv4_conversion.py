"""
IPv4 Conversion

Convert between IPv4 address formats: dotted-decimal, integer, binary.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/ipv4_conversion.py
"""


def ipv4_to_int(ip: str) -> int:
    """
    Convert a dotted-decimal IPv4 address to a 32-bit integer.

    >>> ipv4_to_int("0.0.0.0")
    0
    >>> ipv4_to_int("192.168.1.1")
    3232235777
    >>> ipv4_to_int("255.255.255.255")
    4294967295
    >>> ipv4_to_int("10.0.0.1")
    167772161
    >>> ipv4_to_int("256.0.0.1")
    Traceback (most recent call last):
        ...
    ValueError: Invalid IPv4 octet: 256
    """
    octets = ip.strip().split(".")
    if len(octets) != 4:
        raise ValueError(f"Invalid IPv4 address: {ip}")

    result = 0
    for octet_str in octets:
        octet = int(octet_str)
        if not 0 <= octet <= 255:
            raise ValueError(f"Invalid IPv4 octet: {octet}")
        result = (result << 8) | octet
    return result


def int_to_ipv4(number: int) -> str:
    """
    Convert a 32-bit integer to dotted-decimal IPv4 address.

    >>> int_to_ipv4(0)
    '0.0.0.0'
    >>> int_to_ipv4(3232235777)
    '192.168.1.1'
    >>> int_to_ipv4(4294967295)
    '255.255.255.255'
    >>> int_to_ipv4(-1)
    Traceback (most recent call last):
        ...
    ValueError: Number must be between 0 and 4294967295
    """
    if not 0 <= number <= 0xFFFFFFFF:
        raise ValueError("Number must be between 0 and 4294967295")

    octets = []
    for _ in range(4):
        octets.append(str(number & 0xFF))
        number >>= 8
    return ".".join(reversed(octets))


def ipv4_to_binary(ip: str) -> str:
    """
    Convert a dotted-decimal IPv4 to binary string representation.

    >>> ipv4_to_binary("192.168.1.1")
    '11000000.10101000.00000001.00000001'
    >>> ipv4_to_binary("0.0.0.0")
    '00000000.00000000.00000000.00000000'
    """
    octets = ip.strip().split(".")
    return ".".join(f"{int(o):08b}" for o in octets)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_ips = ["0.0.0.0", "192.168.1.1", "10.0.0.1", "255.255.255.255"]
    for ip in test_ips:
        num = ipv4_to_int(ip)
        back = int_to_ipv4(num)
        binary = ipv4_to_binary(ip)
        print(f"  {ip} -> {num} -> {back} | binary: {binary}")
