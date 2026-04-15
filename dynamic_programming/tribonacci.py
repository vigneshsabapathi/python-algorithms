# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/tribonacci.py


def tribonacci(n: int) -> int:
    """
    Return the n-th Tribonacci number.

    T(0) = 0, T(1) = 0, T(2) = 1
    T(n) = T(n-1) + T(n-2) + T(n-3)

    >>> [tribonacci(i) for i in range(10)]
    [0, 0, 1, 1, 2, 4, 7, 13, 24, 44]
    >>> tribonacci(25)
    755476
    >>> tribonacci(0)
    0
    >>> tribonacci(2)
    1
    """
    if n < 2:
        return 0
    if n == 2:
        return 1

    a, b, c = 0, 0, 1
    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c

    return c


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    for i in range(15):
        print(f"  T({i:>2}) = {tribonacci(i)}")
