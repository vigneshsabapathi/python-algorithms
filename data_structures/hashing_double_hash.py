#!/usr/bin/env python3
"""
Double hashing is a collision resolving technique in Open Addressed Hash tables.
Double hashing uses the idea of applying a second hash function to key when a collision
occurs. The advantage of Double hashing is that it is one of the best forms of probing,
producing a uniform distribution of records throughout a hash table. This technique
does not yield any clusters. It is one of effective method for resolving collisions.

Double hashing can be done using: (hash1(key) + i * hash2(key)) % TABLE_SIZE
Where hash1() and hash2() are hash functions and TABLE_SIZE is size of hash table.

Reference: https://en.wikipedia.org/wiki/Double_hashing
"""

import math
from abc import abstractmethod


def _is_prime(number: int) -> bool:
    if not isinstance(number, int) or number < 0:
        return False
    if 1 < number < 4:
        return True
    if number < 2 or not number % 2:
        return False
    return not any(not number % i for i in range(3, int(math.sqrt(number) + 1), 2))


def _next_prime(value, factor=1, **kwargs):
    value = factor * value
    first_value_val = value
    while not _is_prime(value):
        value += 1 if not ("desc" in kwargs and kwargs["desc"] is True) else -1
    if value == first_value_val:
        return _next_prime(value + 1, **kwargs)
    return value


class HashTable:
    def __init__(
        self,
        size_table: int,
        charge_factor: int | None = None,
        lim_charge: float | None = None,
    ) -> None:
        self.size_table = size_table
        self.values = [None] * self.size_table
        self.lim_charge = 0.75 if lim_charge is None else lim_charge
        self.charge_factor = 1 if charge_factor is None else charge_factor
        self.__aux_list: list = []
        self._keys: dict = {}

    def keys(self):
        return self._keys

    def balanced_factor(self):
        return sum(1 for slot in self.values if slot is not None) / (
            self.size_table * self.charge_factor
        )

    def hash_function(self, key):
        return key % self.size_table

    def _step_by_step(self, step_ord):
        print(f"step {step_ord}")
        print(list(range(len(self.values))))
        print(self.values)

    def bulk_insert(self, values):
        i = 1
        self.__aux_list = values
        for value in values:
            self.insert_data(value)
            self._step_by_step(i)
            i += 1

    def _set_value(self, key, data):
        self.values[key] = data
        self._keys[key] = data

    @abstractmethod
    def _collision_resolution(self, key, data=None):
        new_key = self.hash_function(key + 1)
        while self.values[new_key] is not None and self.values[new_key] != key:
            if self.values.count(None) > 0:
                new_key = self.hash_function(new_key + 1)
            else:
                new_key = None
                break
        return new_key

    def rehashing(self):
        survivor_values = [value for value in self.values if value is not None]
        self.size_table = _next_prime(self.size_table, factor=2)
        self._keys.clear()
        self.values = [None] * self.size_table
        for value in survivor_values:
            self.insert_data(value)

    def insert_data(self, data):
        key = self.hash_function(data)
        if self.values[key] is None:
            self._set_value(key, data)
        elif self.values[key] == data:
            pass
        else:
            collision_resolution = self._collision_resolution(key, data)
            if collision_resolution is not None:
                self._set_value(collision_resolution, data)
            else:
                self.rehashing()
                self.insert_data(data)


class DoubleHash(HashTable):
    """
    Hash Table with open addressing and Double Hash collision resolution.

    >>> dh = DoubleHash(3)
    >>> dh.insert_data(10)
    >>> dh.insert_data(20)
    >>> dh.insert_data(30)
    >>> dh.keys()
    {1: 10, 2: 20, 0: 30}

    >>> dh = DoubleHash(2)
    >>> dh.insert_data(10)
    >>> dh.insert_data(20)
    >>> dh.insert_data(30)
    >>> dh.keys()
    {10: 10, 9: 20, 8: 30}

    >>> dh = DoubleHash(4)
    >>> dh.insert_data(10)
    >>> dh.insert_data(20)
    >>> dh.insert_data(30)
    >>> dh.keys()
    {9: 20, 10: 10, 8: 30}
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash_function_2(self, value, data):
        next_prime_gt = (
            _next_prime(value % self.size_table)
            if not _is_prime(value % self.size_table)
            else value % self.size_table
        )
        return next_prime_gt - (data % next_prime_gt)

    def __hash_double_function(self, key, data, increment):
        return (increment * self.__hash_function_2(key, data)) % self.size_table

    def _collision_resolution(self, key, data=None):
        i = 1
        new_key = self.hash_function(data)

        while self.values[new_key] is not None and self.values[new_key] != key:
            new_key = (
                self.__hash_double_function(key, data, i)
                if self.balanced_factor() >= self.lim_charge
                else None
            )
            if new_key is None:
                break
            else:
                i += 1

        return new_key


if __name__ == "__main__":
    import doctest

    doctest.testmod()
