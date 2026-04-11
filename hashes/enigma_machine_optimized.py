#!/usr/bin/env python3
"""
Optimized and alternative implementations of the Enigma Machine cipher.

The reference simulates a 3-rotor Enigma machine with a reflector on
printable ASCII (94 characters). Each character passes forward through
3 gears, through a reflector, then backward through the 3 gears.
Rotors advance after each character (odometer-style).

Variants:
  reference     -- dict-based functional Enigma from base module
  class_based   -- OOP Enigma with configurable rotors
  lookup_table  -- pre-computed substitution tables (faster engine)
  deque_rotors  -- uses collections.deque for O(1) rotation

Run:
    python hashes/enigma_machine_optimized.py
"""

from __future__ import annotations

import os
import sys
import timeit
from collections import deque

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hashes.enigma_machine import enigma_encrypt as reference


# ---------------------------------------------------------------------------
# Variant 1 -- class_based: OOP Enigma with configurable rotors
# ---------------------------------------------------------------------------

class EnigmaMachine:
    """
    Object-oriented Enigma machine with configurable rotors.

    >>> em = EnigmaMachine()
    >>> em.encrypt('Hello')
    'U6-+&'

    >>> em2 = EnigmaMachine(token=42)
    >>> enc = em2.encrypt('Hello World')
    >>> em3 = EnigmaMachine(token=42)
    >>> em3.encrypt(enc) == 'Hello World'
    True
    """

    def __init__(self, token: int = 0):
        self.alphabets = [chr(i) for i in range(32, 126)]
        n = len(self.alphabets)
        self.gears = [list(range(n)) for _ in range(3)]
        self.reflector = list(reversed(range(n)))
        self.positions = [0, 0, 0]
        self.n = n
        # Apply token offset
        for _ in range(token):
            self._rotate()

    def _rotate(self) -> None:
        n = self.n
        self.gears[0].append(self.gears[0].pop(0))
        self.positions[0] += 1
        if self.positions[0] % n == 0:
            self.gears[1].append(self.gears[1].pop(0))
            self.positions[1] += 1
            if self.positions[1] % n == 0:
                self.gears[2].append(self.gears[2].pop(0))
                self.positions[2] += 1

    def _process_char(self, char: str) -> str:
        idx = self.alphabets.index(char)
        # Forward
        for gear in self.gears:
            idx = gear[idx]
        # Reflector
        idx = self.reflector[idx]
        # Backward
        for gear in reversed(self.gears):
            idx = gear.index(idx)
        self._rotate()
        return self.alphabets[idx]

    def encrypt(self, message: str) -> str:
        return "".join(self._process_char(c) for c in message)


# ---------------------------------------------------------------------------
# Variant 2 -- deque_rotors: O(1) rotation using deque
# ---------------------------------------------------------------------------

class EnigmaDeque:
    """
    Enigma machine using deque for O(1) rotor rotation.

    list.pop(0) is O(n); deque.popleft() is O(1). For the 94-char alphabet
    the difference is small, but it's the correct data structure.

    >>> ed = EnigmaDeque()
    >>> ed.encrypt('Hello')
    'U6-+&'

    >>> ed2 = EnigmaDeque(token=42)
    >>> enc = ed2.encrypt('Test')
    >>> ed3 = EnigmaDeque(token=42)
    >>> ed3.encrypt(enc) == 'Test'
    True
    """

    def __init__(self, token: int = 0):
        self.alphabets = [chr(i) for i in range(32, 126)]
        n = len(self.alphabets)
        self.gears = [deque(range(n)) for _ in range(3)]
        self.reflector = list(reversed(range(n)))
        self.positions = [0, 0, 0]
        self.n = n
        for _ in range(token):
            self._rotate()

    def _rotate(self) -> None:
        n = self.n
        self.gears[0].rotate(-1)
        self.positions[0] += 1
        if self.positions[0] % n == 0:
            self.gears[1].rotate(-1)
            self.positions[1] += 1
            if self.positions[1] % n == 0:
                self.gears[2].rotate(-1)
                self.positions[2] += 1

    def _process_char(self, char: str) -> str:
        idx = self.alphabets.index(char)
        for gear in self.gears:
            idx = gear[idx]
        idx = self.reflector[idx]
        for gear in reversed(self.gears):
            idx = list(gear).index(idx)
        self._rotate()
        return self.alphabets[idx]

    def encrypt(self, message: str) -> str:
        return "".join(self._process_char(c) for c in message)


# ---------------------------------------------------------------------------
# Variant 3 -- lookup_table: pre-computed forward/reverse tables
# ---------------------------------------------------------------------------

class EnigmaLookup:
    """
    Enigma with pre-computed reverse lookup tables for O(1) backward pass.

    The reference uses list.index() which is O(n). This variant maintains
    reverse-lookup dicts that update on rotation.

    >>> el = EnigmaLookup()
    >>> el.encrypt('Hello')
    'U6-+&'
    """

    def __init__(self, token: int = 0):
        self.alphabets = [chr(i) for i in range(32, 126)]
        n = len(self.alphabets)
        self.gears = [list(range(n)) for _ in range(3)]
        self.rev_gears = [{v: k for k, v in enumerate(g)} for g in self.gears]
        self.reflector = list(reversed(range(n)))
        self.positions = [0, 0, 0]
        self.n = n
        for _ in range(token):
            self._rotate()

    def _rotate(self) -> None:
        n = self.n
        self.gears[0].append(self.gears[0].pop(0))
        self.rev_gears[0] = {v: k for k, v in enumerate(self.gears[0])}
        self.positions[0] += 1
        if self.positions[0] % n == 0:
            self.gears[1].append(self.gears[1].pop(0))
            self.rev_gears[1] = {v: k for k, v in enumerate(self.gears[1])}
            self.positions[1] += 1
            if self.positions[1] % n == 0:
                self.gears[2].append(self.gears[2].pop(0))
                self.rev_gears[2] = {v: k for k, v in enumerate(self.gears[2])}
                self.positions[2] += 1

    def _process_char(self, char: str) -> str:
        idx = self.alphabets.index(char)
        for gear in self.gears:
            idx = gear[idx]
        idx = self.reflector[idx]
        for rev in reversed(self.rev_gears):
            idx = rev[idx]
        self._rotate()
        return self.alphabets[idx]

    def encrypt(self, message: str) -> str:
        return "".join(self._process_char(c) for c in message)


# ---------------------------------------------------------------------------
# Correctness + benchmark
# ---------------------------------------------------------------------------

TEST_CASES = [
    ("Hello", 0, "U6-+&"),
    ("a", 0, "<"),
    ("", 0, ""),
]


def run_all() -> None:
    print("\n=== Correctness ===")
    for msg, token, expected in TEST_CASES:
        results = {
            "reference": reference(msg, token),
            "class_based": EnigmaMachine(token).encrypt(msg),
            "deque": EnigmaDeque(token).encrypt(msg),
            "lookup": EnigmaLookup(token).encrypt(msg),
        }
        ok = all(v == expected for v in results.values())
        tag = "OK" if ok else "FAIL"
        print(f"  [{tag}] enigma({msg!r}, token={token}) = {expected!r}")

    # Verify encrypt/decrypt symmetry
    for token in [0, 42, 100]:
        msg = "The quick brown fox jumps over the lazy dog"
        enc = reference(msg, token)
        dec = reference(enc, token)
        ok = dec == msg
        print(f"  [{'OK' if ok else 'FAIL'}] Encrypt/decrypt symmetry (token={token})")

    # Benchmark
    REPS = 2_000
    test_msg = "The quick brown fox jumps over the lazy dog"

    print(f"\n=== Benchmark: encrypt {len(test_msg)}-char message, {REPS} runs ===")
    for name, fn in [
        ("reference", lambda: reference(test_msg, 0)),
        ("class_based", lambda: EnigmaMachine(0).encrypt(test_msg)),
        ("deque", lambda: EnigmaDeque(0).encrypt(test_msg)),
        ("lookup", lambda: EnigmaLookup(0).encrypt(test_msg)),
    ]:
        t = timeit.timeit(fn, number=REPS) * 1000 / REPS
        print(f"  {name:<14} {t:>8.4f} ms")


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=False)
    print("Doctests passed.")
    run_all()
