# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/max_product_subarray.py


def max_product_subarray(nums: list[int]) -> int:
    """
    Find the contiguous subarray with the largest product.

    A negative times a negative can produce the largest product,
    so we track both the running max and running min.

    >>> max_product_subarray([2, 3, -2, 4])
    6
    >>> max_product_subarray([-2, 0, -1])
    0
    >>> max_product_subarray([-2, 3, -4])
    24
    >>> max_product_subarray([0, 2])
    2
    >>> max_product_subarray([-2])
    -2
    >>> max_product_subarray([2, -5, -2, -4, 3])
    24
    >>> max_product_subarray([])
    0
    """
    if not nums:
        return 0

    max_prod = nums[0]
    cur_max = nums[0]
    cur_min = nums[0]

    for i in range(1, len(nums)):
        num = nums[i]
        if num < 0:
            cur_max, cur_min = cur_min, cur_max
        cur_max = max(num, cur_max * num)
        cur_min = min(num, cur_min * num)
        max_prod = max(max_prod, cur_max)

    return max_prod


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([2, 3, -2, 4], 6),
        ([-2, 0, -1], 0),
        ([-2, 3, -4], 24),
        ([0, 2], 2),
        ([-2], -2),
        ([2, -5, -2, -4, 3], 24),
        ([], 0),
    ]
    for nums, expected in cases:
        result = max_product_subarray(nums)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] max_product_subarray({nums}) = {result}  (expected {expected})")
