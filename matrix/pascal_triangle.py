"""

Task:
Generate Pascal's Triangle for a given number of rows.
Each element is the sum of the two elements directly above it:
  triangle[r][c] = triangle[r-1][c-1] + triangle[r-1][c]

Implementation notes: Two approaches provided:
1. Standard: build each row from the previous row
2. Optimized: exploit symmetry (each row is a palindrome)

Reference: https://en.wikipedia.org/wiki/Pascal%27s_triangle
Reference: https://github.com/TheAlgorithms/Python/blob/master/matrix/pascal_triangle.py
"""


def generate_pascal_triangle(num_rows: int) -> list[list[int]]:
    """
    Generate Pascal's triangle with the given number of rows.

    >>> generate_pascal_triangle(0)
    []
    >>> generate_pascal_triangle(1)
    [[1]]
    >>> generate_pascal_triangle(2)
    [[1], [1, 1]]
    >>> generate_pascal_triangle(3)
    [[1], [1, 1], [1, 2, 1]]
    >>> generate_pascal_triangle(5)
    [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    >>> generate_pascal_triangle(-5)
    Traceback (most recent call last):
        ...
    ValueError: The input value of 'num_rows' should be greater than or equal to 0
    >>> generate_pascal_triangle(7.89)
    Traceback (most recent call last):
        ...
    TypeError: The input value of 'num_rows' should be 'int'
    """
    if not isinstance(num_rows, int):
        raise TypeError("The input value of 'num_rows' should be 'int'")
    if num_rows == 0:
        return []
    elif num_rows < 0:
        raise ValueError(
            "The input value of 'num_rows' should be greater than or equal to 0"
        )

    triangle: list[list[int]] = []
    for current_row_idx in range(num_rows):
        current_row = [1] * (current_row_idx + 1)
        for col in range(1, current_row_idx):
            current_row[col] = triangle[current_row_idx - 1][col - 1] + triangle[current_row_idx - 1][col]
        triangle.append(current_row)
    return triangle


def generate_pascal_triangle_optimized(num_rows: int) -> list[list[int]]:
    """
    Generate Pascal's triangle exploiting row symmetry.
    Reduces operations by computing only the first half of each row.

    >>> generate_pascal_triangle_optimized(3)
    [[1], [1, 1], [1, 2, 1]]
    >>> generate_pascal_triangle_optimized(1)
    [[1]]
    >>> generate_pascal_triangle_optimized(0)
    []
    >>> generate_pascal_triangle_optimized(-5)
    Traceback (most recent call last):
        ...
    ValueError: The input value of 'num_rows' should be greater than or equal to 0
    >>> generate_pascal_triangle_optimized(7.89)
    Traceback (most recent call last):
        ...
    TypeError: The input value of 'num_rows' should be 'int'
    """
    if not isinstance(num_rows, int):
        raise TypeError("The input value of 'num_rows' should be 'int'")
    if num_rows == 0:
        return []
    elif num_rows < 0:
        raise ValueError(
            "The input value of 'num_rows' should be greater than or equal to 0"
        )

    result: list[list[int]] = [[1]]
    for row_index in range(1, num_rows):
        temp_row = [0] + result[-1] + [0]
        row_length = row_index + 1
        distinct_elements = sum(divmod(row_length, 2))
        row_first_half = [
            temp_row[i - 1] + temp_row[i] for i in range(1, distinct_elements + 1)
        ]
        row_second_half = row_first_half[: (row_index + 1) // 2]
        row_second_half.reverse()
        row = row_first_half + row_second_half
        result.append(row)

    return result


def print_pascal_triangle(num_rows: int) -> None:
    """
    Print Pascal's triangle formatted with centering.

    >>> print_pascal_triangle(5)
        1
       1 1
      1 2 1
     1 3 3 1
    1 4 6 4 1
    """
    triangle = generate_pascal_triangle(num_rows)
    for row_idx in range(num_rows):
        for _ in range(num_rows - row_idx - 1):
            print(end=" ")
        for col_idx in range(row_idx + 1):
            if col_idx != row_idx:
                print(triangle[row_idx][col_idx], end=" ")
            else:
                print(triangle[row_idx][col_idx], end="")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
