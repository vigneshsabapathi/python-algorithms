"""
Optimized camelCase → snake_case conversion.
Companion to camel_case_to_snake_case.py.

Two approaches:
  1. Original: manual character loop with index arithmetic
  2. Regex:    zero-width lookahead/lookbehind to locate all boundaries in one pass

Bugs in the original:
  - index=0 reads input_str[-1] (the LAST character) as the "previous" character.
    Works by accident: any spurious leading '_' is stripped at the end.
  - Empty string crashes: `snake_str[0]` raises IndexError when input_str == "".

The regex approach fixes both and is simpler.
"""

import re

# Pre-compiled at module level — paid once, reused on every call.
#
# Zero-width assertions: no characters are consumed, only boundaries are found.
#   (?=[A-Z])              — before EVERY uppercase letter (matches original behaviour:
#                            each uppercase gets its own segment, so XMLParser → x_m_l_parser)
#   (?<=[a-zA-Z])(?=\d)    — letter immediately before a digit
#   (?<=\d)(?=[a-zA-Z])    — digit immediately before a letter
#
# All three cases get an '_' inserted; any leading '_' is stripped at the end.
_BOUNDARIES = re.compile(
    r"(?=[A-Z])"               # before every uppercase (camelCase, PascalCase, acronyms)
    r"|(?<=[a-zA-Z])(?=\d)"    # letter → digit
    r"|(?<=\d)(?=[a-zA-Z])"    # digit → letter
)
_NON_ALNUM = re.compile(r"[^a-z0-9]+")  # collapses runs of non-alnum into one _


def camel_to_snake_case_regex(input_str: str) -> str:
    """
    Convert camelCase/PascalCase to snake_case using pre-compiled regex.
    Fixes the original's empty-string crash and index-0 look-behind bug.

    >>> camel_to_snake_case_regex("someRandomString")
    'some_random_string'
    >>> camel_to_snake_case_regex("SomeRandomStr#ng")
    'some_random_str_ng'
    >>> camel_to_snake_case_regex("123someRandom123String123")
    '123_some_random_123_string_123'
    >>> camel_to_snake_case_regex("123SomeRandom123String123")
    '123_some_random_123_string_123'
    >>> camel_to_snake_case_regex("")
    ''
    >>> camel_to_snake_case_regex("alreadysnake")
    'alreadysnake'
    >>> camel_to_snake_case_regex("XMLParser")
    'x_m_l_parser'
    >>> camel_to_snake_case_regex(123)
    Traceback (most recent call last):
        ...
    ValueError: Expected string as input, found <class 'int'>
    """
    if not isinstance(input_str, str):
        raise ValueError(f"Expected string as input, found {type(input_str)}")
    if not input_str:
        return ""

    # Step 1: insert '_' at every camel/digit/letter boundary (zero-width, no copy)
    s = _BOUNDARIES.sub("_", input_str)
    # Step 2: lowercase everything
    s = s.lower()
    # Step 3: collapse runs of non-alphanumeric chars (e.g. '#', '--') into one '_'
    s = _NON_ALNUM.sub("_", s)
    # Step 4: strip any leading/trailing underscore
    return s.strip("_")


def benchmark() -> None:
    from timeit import timeit
    from camel_case_to_snake_case import camel_to_snake_case

    n = 500_000
    cases = [
        ("short",  "someRandomString"),
        ("medium", "123someRandom123String123"),
        ("long",   "someRandomCamelCaseString" * 5),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, msg in cases:
        t_orig = timeit(
            "camel_to_snake_case(s)",
            setup=f"from camel_case_to_snake_case import camel_to_snake_case; s={msg!r}",
            number=n,
        )
        t_re = timeit(
            "camel_to_snake_case_regex(s)",
            setup=f"from camel_case_to_snake_case_optimized import camel_to_snake_case_regex; s={msg!r}",
            number=n,
        )

        print(f"  {label} ({len(msg)} chars):")
        print(f"    original  (manual loop + index arithmetic) {t_orig:.4f}s")
        print(f"    regex     (lookahead/lookbehind, 3 passes)  {t_re:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
