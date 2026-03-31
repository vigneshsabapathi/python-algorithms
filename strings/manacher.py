def palindromic_string(input_string: str) -> str:
    """
    >>> palindromic_string('abbbaba')
    'abbba'
    >>> palindromic_string('ababa')
    'ababa'

    Manacher's algorithm which finds Longest palindromic Substring in linear time.

    1. first this convert input_string("xyx") into new_string("x|y|x") where odd
        positions are actual input characters.
    2. for each character in new_string it find corresponding length and
        store the length and left,right to store previously calculated info.
        (please look the explanation for details)

    3. return corresponding output_string by removing all "|"
    """
    max_length = 0

    # Insert '|' between every character so both odd and even length palindromes
    # become odd-length in the transformed string
    # e.g. "aba" -> "a|b|a",  "abba" -> "a|b|b|a"
    new_input_string = ""
    output_string = ""

    for i in input_string[: len(input_string) - 1]:
        new_input_string += i + "|"
    new_input_string += input_string[-1]

    # left, right: boundaries of the currently furthest-reaching palindrome
    left, right = 0, 0

    # length[i] = length of palindromic substring centered at position i in new_string
    length = [1 for i in range(len(new_input_string))]

    start = 0
    for j in range(len(new_input_string)):
        # Key reuse step: if j is inside the known right boundary, mirror from left side
        # Otherwise start fresh (k=1) and expand from scratch
        k = 1 if j > right else min(length[left + right - j] // 2, right - j + 1)

        # Expand around center j as far as characters match
        while (
            j - k >= 0
            and j + k < len(new_input_string)
            and new_input_string[k + j] == new_input_string[j - k]
        ):
            k += 1

        # Store the full palindrome length centered at j
        length[j] = 2 * k - 1

        # If this palindrome extends past the current right boundary, update it
        if j + k - 1 > right:
            left = j - k + 1
            right = j + k - 1

        # Track the longest palindrome found so far
        if max_length < length[j]:
            max_length = length[j]
            start = j

    # Extract the palindrome from the transformed string, dropping all '|' separators
    s = new_input_string[start - max_length // 2 : start + max_length // 2 + 1]
    for i in s:
        if i != "|":
            output_string += i

    return output_string


if __name__ == "__main__":
    import doctest

    doctest.testmod()

"""
...a0...a1...a2.....a3......a4...a5...a6....

consider the string for which we are calculating the longest palindromic substring is
shown above where ... are some characters in between and right now we are calculating
the length of palindromic substring with center at a5 with following conditions :
i) we have stored the length of palindromic substring which has center at a3
    (starts at left ends at right) and it is the furthest ending till now,
    and it has ending after a6
ii) a2 and a4 are equally distant from a3 so char(a2) == char(a4)
iii) a0 and a6 are equally distant from a3 so char(a0) == char(a6)
iv) a1 is corresponding equal character of a5 in palindrome with center a3 (remember
    that in below derivation of a4==a6)

now for a5 we will calculate the length of palindromic substring with center as a5 but
can we use previously calculated information in some way?
Yes, look the above string we know that a5 is inside the palindrome with center a3 and
previously we have calculated that
a0==a2 (palindrome of center a1)
a2==a4 (palindrome of center a3)
a0==a6 (palindrome of center a3)
so a4==a6

so we can say that palindrome at center a5 is at least as long as palindrome at center
a1 but this only holds if a0 and a6 are inside the limits of palindrome centered at a3
so finally ..

len_of_palindrome__at(a5) = min(len_of_palindrome_at(a1), right-a5)
where a3 lies from left to right and we have to keep updating that

and if the a5 lies outside of left,right boundary we calculate length of palindrome with
bruteforce and update left,right.

it gives the linear time complexity just like z-function
"""
