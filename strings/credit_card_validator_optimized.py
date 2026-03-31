"""
Optimized credit card validation.
Companion to credit_card_validator.py.

Key improvement:
  The original luhn_validation mutates the string on every iteration
  (cc_number = cc_number[:i] + str(digit) + cc_number[i+1:]), which is O(n²)
  in total string work — each slice copies up to n characters, done n/2 times.

  The optimised version works entirely with integers in a single reversed pass:
  O(n) time, O(1) extra space, no string allocation inside the loop.

  Also simplifies digit reduction: when doubled > 9, subtract 9 instead of
  (d % 10 + 1) — mathematically equivalent for the range 10–18.
"""

from credit_card_validator import validate_initial_digits


def luhn_validation_fast(credit_card_number: str) -> bool:
    """
    Luhn check using a single reversed pass and integer arithmetic.
    No string mutation — O(n) time, O(1) extra space.

    >>> luhn_validation_fast('4111111111111111')
    True
    >>> luhn_validation_fast('36111111111111')
    True
    >>> luhn_validation_fast('41111111111111')
    False
    >>> luhn_validation_fast('4532015112830366')
    True
    >>> luhn_validation_fast('1234567890123456')
    False
    """
    total = 0
    for i, ch in enumerate(reversed(credit_card_number)):
        n = int(ch)
        if i % 2 == 1:      # double every second digit from the right (0-indexed)
            n *= 2
            if n > 9:
                n -= 9      # equivalent to summing the two digits (e.g. 14 → 1+4=5 = 14-9)
        total += n
    return total % 10 == 0


def validate_credit_card_number_fast(credit_card_number: str) -> bool:
    """
    Validate a credit card number using the fast Luhn implementation.

    >>> validate_credit_card_number_fast('4111111111111111')
    4111111111111111 is a valid credit card number.
    True
    >>> validate_credit_card_number_fast('helloworld$')
    helloworld$ is an invalid credit card number because it has nonnumerical characters.
    False
    >>> validate_credit_card_number_fast('32323')
    32323 is an invalid credit card number because of its length.
    False
    >>> validate_credit_card_number_fast('36111111111111')
    36111111111111 is an invalid credit card number because of its first two digits.
    False
    >>> validate_credit_card_number_fast('41111111111111')
    41111111111111 is an invalid credit card number because it fails the Luhn check.
    False
    """
    error_message = f"{credit_card_number} is an invalid credit card number because"
    if not credit_card_number.isdigit():
        print(f"{error_message} it has nonnumerical characters.")
        return False

    if not 13 <= len(credit_card_number) <= 16:
        print(f"{error_message} of its length.")
        return False

    if not validate_initial_digits(credit_card_number):
        print(f"{error_message} of its first two digits.")
        return False

    if not luhn_validation_fast(credit_card_number):
        print(f"{error_message} it fails the Luhn check.")
        return False

    print(f"{credit_card_number} is a valid credit card number.")
    return True


def benchmark() -> None:
    from timeit import timeit

    n = 200_000
    card = "4111111111111111"

    cases = [
        (
            "luhn_validation(card)",
            f"from credit_card_validator import luhn_validation; card={card!r}",
            "original  (string mutation, O(n²) string work)",
        ),
        (
            "luhn_validation_fast(card)",
            f"from credit_card_validator_optimized import luhn_validation_fast; card={card!r}",
            "optimized (integer reversed pass, O(n))",
        ),
    ]

    print(f"Benchmarking {n:,} runs on a {len(card)}-digit card number:\n")
    for stmt, setup, label in cases:
        t = timeit(stmt, setup=setup, number=n)
        print(f"  {label:<48} {t:.4f}s")


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
