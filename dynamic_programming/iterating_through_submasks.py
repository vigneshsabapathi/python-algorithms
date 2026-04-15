"""
Iterating Through Submasks of a Bitmask.

Given a bitmask m, efficiently iterate through all of its submasks.
A mask s is a submask of m if only bits that were set in m are set in s.

The key trick: starting from mask itself, repeatedly compute (submask - 1) & mask
to get the next submask in descending order.

>>> list_of_submasks(15)
[15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
>>> list_of_submasks(13)
[13, 12, 9, 8, 5, 4, 1]
>>> list_of_submasks(7)
[7, 6, 5, 4, 3, 2, 1]
>>> list_of_submasks(1)
[1]
>>> list_of_submasks(-7)  # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
AssertionError: mask needs to be positive integer, your input -7
>>> list_of_submasks(0)  # doctest: +ELLIPSIS
Traceback (most recent call last):
    ...
AssertionError: mask needs to be positive integer, your input 0
"""

from __future__ import annotations


def list_of_submasks(mask: int) -> list[int]:
    """
    Return all submasks of the given bitmask in descending order.

    >>> list_of_submasks(15)
    [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    >>> list_of_submasks(13)
    [13, 12, 9, 8, 5, 4, 1]
    >>> list_of_submasks(-7)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    AssertionError: mask needs to be positive integer, your input -7
    """
    assert isinstance(mask, int) and mask > 0, (
        f"mask needs to be positive integer, your input {mask}"
    )

    all_submasks = []
    submask = mask
    while submask:
        all_submasks.append(submask)
        submask = (submask - 1) & mask
    return all_submasks


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    for m in [7, 13, 15, 255]:
        subs = list_of_submasks(m)
        print(f"  submasks({m}) = {subs[:10]}{'...' if len(subs) > 10 else ''} ({len(subs)} total)")
