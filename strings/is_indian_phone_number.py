import re


def is_indian_phone_number(phone: str) -> bool:
    """
    Determine whether the string is a valid Indian mobile phone number or not.

    Indian mobile numbers are 10 digits and begin with 6, 7, 8, or 9.
    Accepted prefixes: +91, 91, 0, or none.
    An optional single space or hyphen is allowed between the prefix and the number.

    References:
        https://en.wikipedia.org/wiki/Telephone_numbers_in_India

    >>> is_indian_phone_number("9876543210")
    True
    >>> is_indian_phone_number("+919876543210")
    True
    >>> is_indian_phone_number("919876543210")
    True
    >>> is_indian_phone_number("09876543210")
    True
    >>> is_indian_phone_number("+91 9876543210")
    True
    >>> is_indian_phone_number("+91-9876543210")
    True
    >>> is_indian_phone_number("91-6000000000")
    True
    >>> is_indian_phone_number("1234567890")
    False
    >>> is_indian_phone_number("+919876543")
    False
    >>> is_indian_phone_number("+9198765432100")
    False
    >>> is_indian_phone_number("0098765432100")
    False
    >>> is_indian_phone_number("")
    False
    """
    # Pattern breakdown:
    #   ^                       start of string
    #   (?:\+91|91|0)?          optional country code prefix (+91, 91, or 0)
    #   [-\s]?                  optional separator: hyphen or space
    #   [6-9]                   first digit must be 6, 7, 8, or 9 (mobile range)
    #   \d{9}                   followed by exactly 9 more digits
    #   $                       end of string
    pattern = re.compile(r"^(?:\+91|91|0)?[-\s]?[6-9]\d{9}$")
    return bool(re.search(pattern, phone))


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    test_cases = [
        ("9876543210", True),
        ("+919876543210", True),
        ("919876543210", True),
        ("09876543210", True),
        ("+91 9876543210", True),
        ("+91-9876543210", True),
        ("91-6000000000", True),
        ("7000000000", True),
        ("8000000000", True),
        ("6000000000", True),
        ("1234567890", False),   # starts with 1, not a mobile number
        ("+919876543", False),   # too short
        ("+9198765432100", False),  # too long
        ("", False),
    ]

    for phone, expected in test_cases:
        result = is_indian_phone_number(phone)
        status = "OK" if result == expected else "FAIL"
        print(f"[{status}] is_indian_phone_number({phone!r}) = {result}")
