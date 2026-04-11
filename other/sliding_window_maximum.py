"""
Sliding Window Maximum — Find maximum in each sliding window of size k.

Uses a monotonic deque to maintain candidates for the maximum in O(n) time.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/sliding_window_maximum.py
"""

from __future__ import annotations

from collections import deque


def sliding_window_maximum(nums: list[int], k: int) -> list[int]:
    """
    Return the maximum value in each sliding window of size k.

    >>> sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)
    [3, 3, 5, 5, 6, 7]
    >>> sliding_window_maximum([1], 1)
    [1]
    >>> sliding_window_maximum([1, -1], 1)
    [1, -1]
    >>> sliding_window_maximum([9, 11], 2)
    [11]
    >>> sliding_window_maximum([], 1)
    []
    >>> sliding_window_maximum([4, 3, 2, 1], 2)
    [4, 3, 2]
    """
    if not nums or k <= 0:
        return []

    result: list[int] = []
    dq: deque[int] = deque()  # stores indices

    for i, num in enumerate(nums):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove elements smaller than current (maintain decreasing order)
        while dq and nums[dq[-1]] <= num:
            dq.pop()

        dq.append(i)

        # Window is fully formed
        if i >= k - 1:
            result.append(nums[dq[0]])

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
