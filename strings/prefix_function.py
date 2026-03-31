"""
https://cp-algorithms.com/string/prefix-function.html

Prefix function Knuth-Morris-Pratt algorithm

Different algorithm than Knuth-Morris-Pratt pattern finding

E.x. Finding longest prefix which is also suffix

Time Complexity: O(n) - where n is the length of the string
"""


def prefix_function(input_string: str) -> list:
    """
    For the given string this function computes value for each index(i),
    which represents the longest coincidence of prefix and suffix
    for given substring (input_str[0...i])

    For the value of the first element the algorithm always returns 0

    >>> prefix_function("aabcdaabc")
    [0, 1, 0, 0, 0, 1, 2, 3, 4]
    >>> prefix_function("asdasdad")
    [0, 0, 0, 1, 2, 3, 4, 0]
    """

    # result[i] = length of longest proper prefix of input_string[:i+1]
    # that is also a suffix
    prefix_result = [0] * len(input_string)

    for i in range(1, len(input_string)):
        # Start from the previous index's value (DP reuse — avoids recomputing)
        j = prefix_result[i - 1]

        # Fall back until we find a matching character or reach the start
        while j > 0 and input_string[i] != input_string[j]:
            j = prefix_result[j - 1]

        # Extend the matching prefix by one if current chars match
        if input_string[i] == input_string[j]:
            j += 1

        prefix_result[i] = j

    return prefix_result


def longest_prefix(input_str: str) -> int:
    """
    Prefix-function use case
    Finding longest prefix which is suffix as well

    >>> longest_prefix("aabcdaabc")
    4
    >>> longest_prefix("asdasdad")
    4
    >>> longest_prefix("abcab")
    2
    """
    # The maximum value in the prefix array is the length of the longest
    # prefix that is also a suffix for the entire string
    return max(prefix_function(input_str))


if __name__ == "__main__":
    import doctest

    doctest.testmod()
