"""
Validate IPv4 address: four dotted decimals 0-255 with no leading zeros (strict).

>>> is_ip_v4_address_valid("192.168.0.1")
True
>>> is_ip_v4_address_valid("256.1.1.1")
False
>>> is_ip_v4_address_valid("1.2.3")
False
>>> is_ip_v4_address_valid("01.2.3.4")
False
>>> is_ip_v4_address_valid("0.0.0.0")
True
"""


def is_ip_v4_address_valid(ip: str) -> bool:
    """Strict IPv4 validation (no leading zeros).

    >>> is_ip_v4_address_valid("255.255.255.255")
    True
    >>> is_ip_v4_address_valid("192.168.1.256")
    False
    """
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        if not p or not p.isdigit():
            return False
        if len(p) > 1 and p[0] == "0":
            return False  # no leading zeros
        if int(p) > 255:
            return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(is_ip_v4_address_valid("192.168.0.1"))
