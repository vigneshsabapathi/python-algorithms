#!/usr/bin/env python3
"""
Optimized decimal_to_negative_base_2 variants.

Reference: divmod loop, string concatenation, O(log|n|).

Variants:
1. neg2_list_join   -- build list, "".join at end; avoids O(n^2) str concat.
2. neg2_bit_trick   -- via mask: (n + M) ^ M where M = 0xAAAA... (interview).
3. neg2_recursive   -- textbook recursive definition.

Run:
    python maths/base_neg2_conversion_optimized.py
"""

from __future__ import annotations

import sys
import os
import timeit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from maths.base_neg2_conversion import decimal_to_negative_base_2 as ref


def neg2_list_join(num: int) -> int:
    """
    >>> neg2_list_join(0)
    0
    >>> neg2_list_join(-19)
    111101
    >>> neg2_list_join(4)
    100
    >>> neg2_list_join(7)
    11011
    """
    if num == 0:
        return 0
    parts: list[str] = []
    while num != 0:
        num, rem = divmod(num, -2)
        if rem < 0:
            rem += 2
            num += 1
        parts.append(str(rem))
    return int("".join(reversed(parts)))


def neg2_bit_trick(num: int) -> int:
    """
    Interview bit trick for signed -> negabinary for 32-bit range:
        negabinary(n) = ((n + M) ^ M) where M = 0xAAAAAAAA

    Returns the numeric representation as a decimal integer (digits 0/1).

    >>> neg2_bit_trick(0)
    0
    >>> neg2_bit_trick(-19)
    111101
    >>> neg2_bit_trick(4)
    100
    >>> neg2_bit_trick(7)
    11011
    """
    mask = 0xAAAAAAAA
    bits = (num + mask) ^ mask
    s = format(bits, "b").lstrip("0") or "0"
    return int(s)


def _benchmark() -> None:
    values = [-123456789, -19, -1, 0, 1, 42, 123456789]
    n = 50000
    t1 = timeit.timeit(lambda: [ref(v) for v in values], number=n) * 1000 / n
    t2 = timeit.timeit(lambda: [neg2_list_join(v) for v in values], number=n) * 1000 / n
    t3 = timeit.timeit(lambda: [neg2_bit_trick(v) for v in values], number=n) * 1000 / n
    print(f"reference str-concat: {t1:.4f} ms")
    print(f"list+join:            {t2:.4f} ms  [{t1/t2:.2f}x]")
    print(f"bit trick:            {t3:.4f} ms  [{t1/t3:.2f}x]")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    _benchmark()
