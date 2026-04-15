# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/range_sum_query.py


class RangeSumQuery:
    """
    Range Sum Query - Immutable (prefix sum approach).

    Precomputes prefix sums so that any range sum query is O(1).

    >>> rsq = RangeSumQuery([-2, 0, 3, -5, 2, -1])
    >>> rsq.sum_range(0, 2)
    1
    >>> rsq.sum_range(2, 5)
    -1
    >>> rsq.sum_range(0, 5)
    -3
    """

    def __init__(self, nums: list[int]) -> None:
        self.prefix = [0] * (len(nums) + 1)
        for i, num in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + num

    def sum_range(self, left: int, right: int) -> int:
        """
        Return sum of nums[left..right] inclusive.

        >>> rsq = RangeSumQuery([1, 2, 3, 4, 5])
        >>> rsq.sum_range(0, 4)
        15
        >>> rsq.sum_range(1, 3)
        9
        """
        return self.prefix[right + 1] - self.prefix[left]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    nums = [-2, 0, 3, -5, 2, -1]
    rsq = RangeSumQuery(nums)
    cases = [
        (0, 2, 1), (2, 5, -1), (0, 5, -3),
    ]
    for left, right, expected in cases:
        result = rsq.sum_range(left, right)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] sum_range({left}, {right}) = {result}  (expected {expected})")
