#!/usr/bin/env python3
"""
Quadratic Probing — open addressing collision resolution for hash tables.

Quadratic probing works by taking the original hash index and adding successive
values of an arbitrary quadratic polynomial until an open slot is found:
    Hash + 1², Hash + 2², Hash + 3² .... Hash + n²

Reference: https://en.wikipedia.org/wiki/Quadratic_probing
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


class QuadraticProbing(HashTable):
    """
    Hash Table with open addressing using Quadratic Probing.

    >>> qp = QuadraticProbing(7)
    >>> qp.insert_data(90)
    >>> qp.insert_data(340)
    >>> qp.insert_data(24)
    >>> qp.insert_data(45)
    >>> qp.insert_data(99)
    >>> qp.insert_data(73)
    >>> qp.insert_data(7)
    >>> qp.keys()
    {11: 45, 14: 99, 7: 24, 0: 340, 5: 73, 6: 90, 8: 7}

    >>> qp = QuadraticProbing(8)
    >>> qp.insert_data(0)
    >>> qp.insert_data(999)
    >>> qp.insert_data(111)
    >>> qp.keys()
    {0: 0, 7: 999, 3: 111}

    >>> qp = QuadraticProbing(2)
    >>> qp.insert_data(0)
    >>> qp.insert_data(999)
    >>> qp.insert_data(111)
    >>> qp.keys()
    {0: 0, 4: 999, 1: 111}

    >>> qp = QuadraticProbing(1)
    >>> qp.insert_data(0)
    >>> qp.insert_data(999)
    >>> qp.insert_data(111)
    >>> qp.keys()
    {4: 999, 1: 111}
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _collision_resolution(self, key, data=None):  # noqa: ARG002
        i = 1
        new_key = self.hash_function(key + i * i)

        while self.values[new_key] is not None and self.values[new_key] != key:
            i += 1
            new_key = (
                self.hash_function(key + i * i)
                if not self.balanced_factor() >= self.lim_charge
                else None
            )

            if new_key is None:
                break

        return new_key


if __name__ == "__main__":
    import doctest

    doctest.testmod()
