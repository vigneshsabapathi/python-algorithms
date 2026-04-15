"""
FizzBuzz — Classic programming interview question.

Rules:
  - Print "Fizz" for multiples of 3
  - Print "Buzz" for multiples of 5
  - Print "FizzBuzz" for multiples of both 3 and 5 (i.e., 15)
  - Otherwise print the number itself

>>> fizz_buzz(1, 7)
'1 2 Fizz 4 Buzz Fizz 7 '
>>> fizz_buzz(1, 15)
'1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz '
>>> fizz_buzz(1, 0)
Traceback (most recent call last):
    ...
ValueError: Iterations must be done more than 0 times to play FizzBuzz
"""


def fizz_buzz(number: int, iterations: int) -> str:
    """
    Play FizzBuzz from `number` to `iterations`.

    >>> fizz_buzz(1, 7)
    '1 2 Fizz 4 Buzz Fizz 7 '
    >>> fizz_buzz(1, 0)
    Traceback (most recent call last):
      ...
    ValueError: Iterations must be done more than 0 times to play FizzBuzz
    >>> fizz_buzz(-5, 5)
    Traceback (most recent call last):
        ...
    ValueError: starting number must be and integer and be more than 0
    >>> fizz_buzz(1.5, 5)
    Traceback (most recent call last):
        ...
    ValueError: starting number must be and integer and be more than 0
    >>> fizz_buzz(1, 5.5)
    Traceback (most recent call last):
        ...
    ValueError: iterations must be defined as integers
    """
    if not isinstance(iterations, int):
        raise ValueError("iterations must be defined as integers")
    if not isinstance(number, int) or not number >= 1:
        raise ValueError(
            "starting number must be and integer and be more than 0"
        )
    if not iterations >= 1:
        raise ValueError("Iterations must be done more than 0 times to play FizzBuzz")

    out = ""
    while number <= iterations:
        if number % 3 == 0:
            out += "Fizz"
        if number % 5 == 0:
            out += "Buzz"
        if 0 not in (number % 3, number % 5):
            out += str(number)
        number += 1
        out += " "
    return out


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    print(f"  fizz_buzz(1, 20) = {fizz_buzz(1, 20)!r}")
