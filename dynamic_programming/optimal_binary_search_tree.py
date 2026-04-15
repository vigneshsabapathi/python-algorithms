# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/optimal_binary_search_tree.py


def optimal_bst(keys: list[int], freq: list[int]) -> int:
    """
    Find the cost of an optimal binary search tree given keys and frequencies.

    The cost of searching is sum of (depth+1)*frequency for each key.
    Optimal BST minimizes total search cost.

    >>> optimal_bst([10, 12, 20], [34, 8, 50])
    142
    >>> optimal_bst([10, 12], [34, 50])
    118
    >>> optimal_bst([10], [34])
    34
    >>> optimal_bst([10, 20, 30, 40], [4, 2, 6, 3])
    26
    """
    n = len(keys)
    # cost[i][j] = optimal cost of BST for keys[i..j]
    cost = [[0] * n for _ in range(n)]

    # Single keys
    for i in range(n):
        cost[i][i] = freq[i]

    # Chain length from 2 to n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = float("inf")
            freq_sum = sum(freq[i:j + 1])
            for r in range(i, j + 1):
                left = cost[i][r - 1] if r > i else 0
                right = cost[r + 1][j] if r < j else 0
                c = left + right + freq_sum
                if c < cost[i][j]:
                    cost[i][j] = c

    return cost[0][n - 1]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        ([10, 12, 20], [34, 8, 50], 142),
        ([10, 12], [34, 50], 118),
        ([10], [34], 34),
        ([10, 20, 30, 40], [4, 2, 6, 3], 26),
    ]
    for keys, freq, expected in cases:
        result = optimal_bst(keys, freq)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] optimal_bst({keys}, {freq}) = {result}  (expected {expected})")
