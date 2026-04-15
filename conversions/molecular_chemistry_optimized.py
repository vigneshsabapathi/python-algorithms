"""
Molecular Chemistry - Optimized Variants with Benchmarks
"""

import timeit
import re

ATOMIC_MASS = {
    "H": 1.008, "He": 4.003, "C": 12.011, "N": 14.007, "O": 15.999,
    "Na": 22.990, "Cl": 35.453, "Fe": 56.845, "S": 32.065,
}


def mol_weight_regex(formula: str) -> float:
    """
    Regex tokenization.

    >>> mol_weight_regex("H2O")
    18.015
    """
    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    return round(sum(ATOMIC_MASS[e] * (int(c) if c else 1) for e, c in tokens if e), 3)


def mol_weight_manual_parse(formula: str) -> float:
    """
    Manual character-by-character parsing (no regex).

    >>> mol_weight_manual_parse("H2O")
    18.015
    """
    total = 0.0
    i = 0
    while i < len(formula):
        elem = formula[i]
        i += 1
        if i < len(formula) and formula[i].islower():
            elem += formula[i]
            i += 1
        count_str = ""
        while i < len(formula) and formula[i].isdigit():
            count_str += formula[i]
            i += 1
        count = int(count_str) if count_str else 1
        total += ATOMIC_MASS[elem] * count
    return round(total, 3)


def mol_weight_compiled_regex(formula: str, _pat=re.compile(r"([A-Z][a-z]?)(\d*)")) -> float:
    """
    Pre-compiled regex pattern.

    >>> mol_weight_compiled_regex("H2O")
    18.015
    """
    return round(sum(ATOMIC_MASS[e] * (int(c) if c else 1) for e, c in _pat.findall(formula) if e), 3)


def benchmark():
    test_input = "C6H12O6"
    number = 100_000
    print(f"Benchmark: molecular weight of '{test_input}' ({number:,} iterations)\n")
    results = []
    for label, func in [("Regex", mol_weight_regex),
                         ("Manual parse", mol_weight_manual_parse),
                         ("Compiled regex", mol_weight_compiled_regex)]:
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
