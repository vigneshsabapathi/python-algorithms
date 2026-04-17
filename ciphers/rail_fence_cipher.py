"""
Rail Fence Cipher (Zigzag Transposition)

Plaintext is written in a zigzag pattern across 'key' rails, then read
off row by row to produce the ciphertext.

https://en.wikipedia.org/wiki/Rail_fence_cipher
"""


def encrypt(input_string: str, key: int) -> str:
    """
    Encrypt a string using the rail fence cipher.

    >>> encrypt("Hello World", 4)
    'HWe olordll'
    >>> encrypt("This is a message", 0)
    Traceback (most recent call last):
        ...
    ValueError: Height of grid can't be 0 or negative
    >>> encrypt("Short", 1)
    'Short'
    """
    if key <= 0:
        raise ValueError("Height of grid can't be 0 or negative")
    if key == 1 or len(input_string) <= key:
        return input_string

    temp_grid: list[list[str]] = [[] for _ in range(key)]
    lowest = key - 1

    for position, character in enumerate(input_string):
        num = position % (lowest * 2)
        num = min(num, lowest * 2 - num)
        temp_grid[num].append(character)

    return "".join("".join(row) for row in temp_grid)


def decrypt(input_string: str, key: int) -> str:
    """
    Decrypt a rail-fence-encrypted string.

    >>> decrypt("HWe olordll", 4)
    'Hello World'
    >>> decrypt("This is a message", -10)
    Traceback (most recent call last):
        ...
    ValueError: Height of grid can't be 0 or negative
    >>> decrypt("My key is very big", 100)
    'My key is very big'
    """
    if key <= 0:
        raise ValueError("Height of grid can't be 0 or negative")
    if key == 1:
        return input_string

    lowest = key - 1
    temp_grid: list[list[str]] = [[] for _ in range(key)]

    for position in range(len(input_string)):
        num = position % (lowest * 2)
        num = min(num, lowest * 2 - num)
        temp_grid[num].append("*")

    grid: list[list[str]] = []
    counter = 0
    for row in temp_grid:
        splice = input_string[counter : counter + len(row)]
        grid.append(list(splice))
        counter += len(row)

    output_string = ""
    for position in range(len(input_string)):
        num = position % (lowest * 2)
        num = min(num, lowest * 2 - num)
        output_string += grid[num][0]
        grid[num].pop(0)

    return output_string


def bruteforce(input_string: str) -> dict[int, str]:
    """
    Try all key values to decrypt an unknown rail-fence ciphertext.

    >>> bruteforce("HWe olordll")[4]
    'Hello World'
    """
    return {key: decrypt(input_string, key) for key in range(1, len(input_string))}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print(encrypt("Hello World", 4))
    print(decrypt("HWe olordll", 4))
