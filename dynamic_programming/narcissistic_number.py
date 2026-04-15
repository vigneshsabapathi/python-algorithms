# https://github.com/TheAlgorithms/Python/blob/master/dynamic_programming/narcissistic_number.py


def is_narcissistic(n: int) -> bool:
    """
    Check if a number is narcissistic (Armstrong number).

    A number is narcissistic if it equals the sum of its digits
    each raised to the power of the number of digits.

    >>> is_narcissistic(153)
    True
    >>> is_narcissistic(370)
    True
    >>> is_narcissistic(9474)
    True
    >>> is_narcissistic(9475)
    False
    >>> is_narcissistic(1)
    True
    >>> is_narcissistic(0)
    True
    >>> is_narcissistic(10)
    False
    """
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    return sum(int(d) ** power for d in digits) == n


def narcissistic_numbers(limit: int) -> list[int]:
    """
    Return all narcissistic numbers up to limit.

    >>> narcissistic_numbers(1000)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
    """
    return [n for n in range(limit) if is_narcissistic(n)]


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")

    cases = [
        (153, True), (370, True), (9474, True),
        (9475, False), (1, True), (0, True), (10, False),
    ]
    for n, expected in cases:
        result = is_narcissistic(n)
        status = "OK" if result == expected else "FAIL"
        print(f"  [{status}] is_narcissistic({n}) = {result}  (expected {expected})")

    print(f"\n  Narcissistic numbers < 10000: {narcissistic_numbers(10000)}")
