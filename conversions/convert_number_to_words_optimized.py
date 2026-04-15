"""
Convert Number to Words - Optimized Variants with Benchmarks
"""

import timeit

ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
        "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
        "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
THOUSANDS = ["", "Thousand", "Million", "Billion", "Trillion"]


def num_to_words_iterative(number: int) -> str:
    """
    Iterative grouping approach.

    >>> num_to_words_iterative(12345)
    'Twelve Thousand Three Hundred Forty Five'
    """
    if number == 0:
        return "Zero"
    if number < 0:
        return "Negative " + num_to_words_iterative(-number)

    def three(n):
        if n == 0: return ""
        if n < 20: return ONES[n]
        if n < 100: return (TENS[n // 10] + " " + ONES[n % 10]).strip()
        return (ONES[n // 100] + " Hundred " + three(n % 100)).strip()

    parts = []
    gi = 0
    while number > 0:
        group = number % 1000
        if group:
            w = three(group)
            if THOUSANDS[gi]:
                w += " " + THOUSANDS[gi]
            parts.append(w)
        number //= 1000
        gi += 1
    return " ".join(reversed(parts))


def num_to_words_recursive(number: int) -> str:
    """
    Fully recursive approach.

    >>> num_to_words_recursive(12345)
    'Twelve Thousand Three Hundred Forty Five'
    """
    if number == 0:
        return "Zero"
    if number < 0:
        return "Negative " + num_to_words_recursive(-number)

    def convert(n):
        if n == 0: return ""
        if n < 20: return ONES[n]
        if n < 100: return (TENS[n // 10] + " " + convert(n % 10)).strip()
        if n < 1000: return (ONES[n // 100] + " Hundred " + convert(n % 100)).strip()
        for i, t in enumerate(THOUSANDS):
            if n < 1000 ** (i + 1):
                q, r = divmod(n, 1000 ** i)
                return (convert(q) + " " + t + " " + convert(r)).strip()
        return str(n)

    return convert(number)


def num_to_words_divmod(number: int) -> str:
    """
    Divmod-based without recursion.

    >>> num_to_words_divmod(12345)
    'Twelve Thousand Three Hundred Forty Five'
    """
    if number == 0:
        return "Zero"
    if number < 0:
        return "Negative " + num_to_words_divmod(-number)

    def three(n):
        if n == 0: return ""
        if n < 20: return ONES[n]
        if n < 100:
            t, o = divmod(n, 10)
            return (TENS[t] + " " + ONES[o]).strip()
        h, r = divmod(n, 100)
        return (ONES[h] + " Hundred " + three(r)).strip()

    parts = []
    for i, label in enumerate(THOUSANDS):
        number, group = divmod(number, 1000) if i < len(THOUSANDS) - 1 else (0, number)
        if group:
            w = three(group)
            if label:
                w += " " + label
            parts.append(w)
        if number == 0:
            break
    return " ".join(reversed(parts))


def benchmark():
    test_input = 1234567890
    number = 100_000
    print(f"Benchmark: converting {test_input} ({number:,} iterations)\n")
    results = []
    for label, func in [("Iterative", num_to_words_iterative),
                         ("Recursive", num_to_words_recursive),
                         ("Divmod", num_to_words_divmod)]:
        t = timeit.timeit(lambda: func(test_input), number=number)
        ms = t / number * 1000
        results.append((label, ms))
        print(f"  {label:<20} {ms:.4f} ms/call")
    fastest = min(results, key=lambda x: x[1])
    print(f"\n  Fastest: {fastest[0]} at {fastest[1]:.4f} ms/call")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    benchmark()
