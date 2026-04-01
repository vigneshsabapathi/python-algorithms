"""
Optimized capitalize implementations.
Companion to capitalize.py.

Four approaches compared:
  1. Original: sentence[0].upper() + sentence[1:]        — string concat
  2. f-string: f"{sentence[0].upper()}{sentence[1:]}"    — format string
  3. join:     "".join([sentence[0].upper(), sentence[1:]]) — list join
  4. builtin:  sentence.capitalize()                     — WARNING: different semantics

Key gotcha: str.capitalize() lowercases EVERY character after the first.
  "hELLO wORLD".capitalize()  ->  "Hello world"   (lowercases rest)
  capitalize("hELLO wORLD")   ->  "HELLO wORLD"   (preserves rest)

Use str.capitalize() only when you explicitly want the rest lowercased.
"""


def capitalize_fstring(sentence: str) -> str:
    """
    Capitalize using an f-string instead of + concatenation.
    Identical semantics to the original — preserves the rest of the string.

    >>> capitalize_fstring("hello world")
    'Hello world'
    >>> capitalize_fstring("hELLO wORLD")
    'HELLO wORLD'
    >>> capitalize_fstring("123 hello")
    '123 hello'
    >>> capitalize_fstring("")
    ''
    """
    if not sentence:
        return ""
    return f"{sentence[0].upper()}{sentence[1:]}"


def capitalize_join(sentence: str) -> str:
    """
    Capitalize using "".join on a two-element list.
    Same semantics, different string-building strategy.

    >>> capitalize_join("hello world")
    'Hello world'
    >>> capitalize_join("hELLO wORLD")
    'HELLO wORLD'
    >>> capitalize_join("")
    ''
    """
    if not sentence:
        return ""
    return "".join([sentence[0].upper(), sentence[1:]])


def capitalize_builtin(sentence: str) -> str:
    """
    Python's str.capitalize() — fast but LOWERCASES everything after the first char.
    Only use when that behaviour is intentional.

    >>> capitalize_builtin("hello world")
    'Hello world'
    >>> capitalize_builtin("hELLO wORLD")
    'Hello world'
    >>> capitalize_builtin("")
    ''
    """
    return sentence.capitalize()


def benchmark() -> None:
    from timeit import timeit
    from capitalize import capitalize

    n = 1_000_000
    cases = [
        ("short",  "hello"),
        ("medium", "hello world, this is a test sentence"),
        ("mixed",  "hELLO wORLD, THIS IS MIXED CASE"),
    ]

    print(f"Benchmarking {n:,} runs:\n")
    for label, msg in cases:
        t_orig = timeit(
            "capitalize(s)",
            setup=f"from capitalize import capitalize; s={msg!r}",
            number=n,
        )
        t_fs = timeit(
            "capitalize_fstring(s)",
            setup=f"from capitalize_optimized import capitalize_fstring; s={msg!r}",
            number=n,
        )
        t_jn = timeit(
            "capitalize_join(s)",
            setup=f"from capitalize_optimized import capitalize_join; s={msg!r}",
            number=n,
        )
        t_bi = timeit(
            "capitalize_builtin(s)",
            setup=f"from capitalize_optimized import capitalize_builtin; s={msg!r}",
            number=n,
        )

        print(f"  {label} ({len(msg)} chars):")
        print(f"    original  ([0].upper() + [1:])           {t_orig:.4f}s")
        print(f"    f-string  (f'{{[0].upper()}}{{[1:]}}')   {t_fs:.4f}s")
        print(f"    join      (''.join([upper, rest]))        {t_jn:.4f}s")
        print(f"    builtin   (str.capitalize — diff semantics) {t_bi:.4f}s")
        print()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print()
    benchmark()
