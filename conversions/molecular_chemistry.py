"""
Molecular Chemistry Conversion

Convert molecular formulas to molar mass and related calculations.

Reference: https://github.com/TheAlgorithms/Python/blob/master/conversions/molecular_chemistry.py
"""

ATOMIC_MASS: dict[str, float] = {
    "H": 1.008, "He": 4.003, "Li": 6.941, "Be": 9.012, "B": 10.81,
    "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.086, "P": 30.974,
    "S": 32.065, "Cl": 35.453, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
    "Fe": 56.845, "Cu": 63.546, "Zn": 65.380, "Br": 79.904, "Ag": 107.868,
    "I": 126.904, "Au": 196.967, "Pb": 207.200,
}


def molecular_weight(formula: str) -> float:
    """
    Calculate the molecular weight of a chemical formula.

    Supports simple formulas like H2O, NaCl, C6H12O6.
    Does not support parenthetical grouping.

    >>> molecular_weight("H2O")
    18.015
    >>> molecular_weight("NaCl")
    58.443
    >>> molecular_weight("CO2")
    44.009
    >>> molecular_weight("C6H12O6")
    180.156
    >>> molecular_weight("")
    Traceback (most recent call last):
        ...
    ValueError: Empty formula
    """
    if not formula:
        raise ValueError("Empty formula")

    import re

    tokens = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    total = 0.0
    for element, count_str in tokens:
        if not element:
            continue
        if element not in ATOMIC_MASS:
            raise ValueError(f"Unknown element: {element}")
        count = int(count_str) if count_str else 1
        total += ATOMIC_MASS[element] * count

    return round(total, 3)


def moles_to_grams(moles: float, formula: str) -> float:
    """
    Convert moles of a substance to grams.

    >>> moles_to_grams(1, "H2O")
    18.015
    >>> moles_to_grams(2, "NaCl")
    116.886
    >>> moles_to_grams(0, "CO2")
    0.0
    """
    return round(moles * molecular_weight(formula), 3)


def grams_to_moles(grams: float, formula: str) -> float:
    """
    Convert grams of a substance to moles.

    >>> grams_to_moles(18.015, "H2O")
    1.0
    >>> grams_to_moles(44.009, "CO2")
    1.0
    >>> grams_to_moles(0, "NaCl")
    0.0
    """
    return round(grams / molecular_weight(formula), 3)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    formulas = ["H2O", "NaCl", "CO2", "C6H12O6", "Fe2O3"]
    for f in formulas:
        mw = molecular_weight(f)
        print(f"  {f}: molecular weight = {mw} g/mol")

    print(f"\n  2 moles of H2O = {moles_to_grams(2, 'H2O')} g")
    print(f"  100g of NaCl = {grams_to_moles(100, 'NaCl')} mol")
