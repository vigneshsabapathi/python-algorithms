# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/subset_generation.py


def generate_subsets(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets (power set) of the given list.

    >>> generate_subsets([1, 2, 3])
    [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    >>> generate_subsets([])
    [[]]
    >>> generate_subsets([1])
    [[], [1]]
    """
    result = [[]]
    for num in nums:
        result += [subset + [num] for subset in result]
    return result


def generate_subsets_bitmask(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using bitmask enumeration.

    >>> sorted([sorted(s) for s in generate_subsets_bitmask([1, 2, 3])])
    [[], [1], [1, 2], [1, 2, 3], [1, 3], [2], [2, 3], [3]]
    >>> generate_subsets_bitmask([])
    [[]]
    """
    n = len(nums)
    result = []
    for mask in range(1 << n):
        subset = [nums[i] for i in range(n) if mask & (1 << i)]
        result.append(subset)
    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    nums = [1, 2, 3]
    print(f"\n  Subsets of {nums}:")
    for s in generate_subsets(nums):
        print(f"    {s}")
    print(f"\n  Total: {len(generate_subsets(nums))} subsets")
