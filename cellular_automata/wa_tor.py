"""
Wa-Tor predator-prey simulation (1984)
https://en.wikipedia.org/wiki/Wa-Tor

A 2D toroidal grid where fish (prey) and sharks (predators) interact:

Prey rules:
1. Move randomly to an adjacent unoccupied square.
2. After surviving a set number of chronons, reproduce into the vacated square.

Predator rules:
1. Move to an adjacent square occupied by prey (eating it), or to an empty square.
2. Lose 1 energy per chronon. Die at 0 energy.
3. Gain energy when eating prey.
4. Reproduce like prey after surviving enough chronons.

>>> e = Entity(True, coords=(0, 0))
>>> e.prey
True
>>> e.alive
True
"""

from __future__ import annotations

from random import randint, shuffle
from typing import Literal

# Configuration constants
PREY_REPRODUCTION_TIME = 5
PREDATOR_INITIAL_ENERGY = 15
PREDATOR_FOOD_VALUE = 5
PREDATOR_REPRODUCTION_TIME = 20
MAX_ENTITIES = 500
DELETE_UNBALANCED = 50


class Entity:
    """
    Represents a prey or predator entity on the Wa-Tor planet.

    >>> e = Entity(True, coords=(2, 3))
    >>> e.prey
    True
    >>> e.coords
    (2, 3)
    >>> e.alive
    True
    >>> e.energy_value is None
    True

    >>> p = Entity(False, coords=(1, 1))
    >>> p.prey
    False
    >>> p.energy_value == PREDATOR_INITIAL_ENERGY
    True
    """

    def __init__(self, prey: bool, coords: tuple[int, int]) -> None:
        self.prey = prey
        self.coords = coords
        self.remaining_reproduction_time = (
            PREY_REPRODUCTION_TIME if prey else PREDATOR_REPRODUCTION_TIME
        )
        self.energy_value = None if prey else PREDATOR_INITIAL_ENERGY
        self.alive = True

    def reset_reproduction_time(self) -> None:
        """
        >>> e = Entity(True, coords=(0, 0))
        >>> e.reset_reproduction_time()
        >>> e.remaining_reproduction_time == PREY_REPRODUCTION_TIME
        True
        """
        self.remaining_reproduction_time = (
            PREY_REPRODUCTION_TIME if self.prey else PREDATOR_REPRODUCTION_TIME
        )

    def __repr__(self) -> str:
        """
        >>> Entity(prey=True, coords=(1, 1))
        Entity(prey=True, coords=(1, 1), repro=5)
        """
        repr_ = (
            f"Entity(prey={self.prey}, coords={self.coords}, "
            f"repro={self.remaining_reproduction_time}"
        )
        if self.energy_value is not None:
            repr_ += f", energy={self.energy_value}"
        return f"{repr_})"


class WaTor:
    """
    Represents the Wa-Tor planet simulation.

    >>> wt = WaTor(10, 10, prey_count=5, predator_count=3)
    >>> wt.width
    10
    >>> wt.height
    10
    >>> len(wt.get_entities())
    8
    """

    def __init__(
        self, width: int, height: int,
        prey_count: int = 30, predator_count: int = 50
    ) -> None:
        self.width = width
        self.height = height
        self.planet: list[list[Entity | None]] = [
            [None] * width for _ in range(height)
        ]

        for _ in range(prey_count):
            self._add_entity(prey=True)
        for _ in range(predator_count):
            self._add_entity(prey=False)

    def _add_entity(self, prey: bool) -> None:
        """Place an entity at a random empty cell."""
        while True:
            row = randint(0, self.height - 1)
            col = randint(0, self.width - 1)
            if self.planet[row][col] is None:
                self.planet[row][col] = Entity(prey=prey, coords=(row, col))
                return

    def get_entities(self) -> list[Entity]:
        """
        Return all living entities on the planet.

        >>> wt = WaTor(5, 5, prey_count=2, predator_count=1)
        >>> len(wt.get_entities())
        3
        """
        return [e for row in self.planet for e in row if e is not None]

    def _get_adjacent(
        self, row: int, col: int
    ) -> list[tuple[int, int]]:
        """Get adjacent cell coordinates (N, S, E, W)."""
        return [
            (r, c)
            for r, c in [
                (row - 1, col), (row + 1, col),
                (row, col - 1), (row, col + 1),
            ]
            if 0 <= r < self.height and 0 <= c < self.width
        ]

    def _get_surrounding_prey(self, entity: Entity) -> list[Entity]:
        """
        Return prey entities adjacent to a predator.

        >>> wt = WaTor(3, 3, prey_count=0, predator_count=0)
        >>> wt.planet[0][1] = Entity(True, (0, 1))
        >>> wt.planet[1][1] = Entity(False, (1, 1))
        >>> wt.planet[2][1] = Entity(True, (2, 1))
        >>> len(wt._get_surrounding_prey(wt.planet[1][1]))
        2
        """
        row, col = entity.coords
        prey_list = []
        for r, c in self._get_adjacent(row, col):
            ent = self.planet[r][c]
            if ent is not None and ent.prey:
                prey_list.append(ent)
        return prey_list

    def _move_and_reproduce(
        self, entity: Entity,
        direction_orders: list[Literal["N", "E", "S", "W"]]
    ) -> None:
        """Move entity to empty adjacent cell and optionally reproduce."""
        row, col = entity.coords
        adjacent_map = {
            "N": (row - 1, col),
            "S": (row + 1, col),
            "W": (row, col - 1),
            "E": (row, col + 1),
        }

        old_coords = entity.coords
        for d in direction_orders:
            r, c = adjacent_map[d]
            if 0 <= r < self.height and 0 <= c < self.width and self.planet[r][c] is None:
                self.planet[r][c] = entity
                self.planet[row][col] = None
                entity.coords = (r, c)
                break

        # Reproduce if moved and timer expired
        if old_coords != entity.coords and entity.remaining_reproduction_time <= 0:
            if len(self.get_entities()) < MAX_ENTITIES:
                self.planet[row][col] = Entity(prey=entity.prey, coords=old_coords)
                entity.reset_reproduction_time()
        else:
            entity.remaining_reproduction_time -= 1

    def _balance(self) -> None:
        """Remove excess entities if population nears max."""
        entities = self.get_entities()
        if len(entities) >= MAX_ENTITIES - MAX_ENTITIES // 10:
            shuffle(entities)
            prey = [e for e in entities if e.prey]
            predators = [e for e in entities if not e.prey]
            excess = prey[:DELETE_UNBALANCED] if len(prey) > len(predators) \
                else predators[:DELETE_UNBALANCED]
            for e in excess:
                self.planet[e.coords[0]][e.coords[1]] = None

    def step(self) -> dict[str, int]:
        """
        Advance the simulation by one chronon.
        Returns population counts.

        >>> wt = WaTor(5, 5, prey_count=3, predator_count=2)
        >>> result = wt.step()
        >>> 'prey' in result and 'predators' in result
        True
        """
        all_entities = self.get_entities()
        shuffle(all_entities)

        for entity in all_entities:
            if not entity.alive:
                continue

            directions: list[Literal["N", "E", "S", "W"]] = ["N", "E", "S", "W"]
            shuffle(directions)

            if entity.prey:
                self._move_and_reproduce(entity, directions)
            else:
                assert entity.energy_value is not None
                # Die if no energy
                if entity.energy_value == 0:
                    self.planet[entity.coords[0]][entity.coords[1]] = None
                    entity.alive = False
                    continue

                # Try to eat prey
                surrounding_prey = self._get_surrounding_prey(entity)
                if surrounding_prey:
                    shuffle(surrounding_prey)
                    prey_target = surrounding_prey[0]
                    prey_target.alive = False

                    row, col = entity.coords
                    pr, pc = prey_target.coords
                    self.planet[pr][pc] = entity
                    self.planet[row][col] = None
                    entity.coords = (pr, pc)
                    entity.energy_value += PREDATOR_FOOD_VALUE
                else:
                    self._move_and_reproduce(entity, directions)

                entity.energy_value -= 1

        self._balance()

        entities = self.get_entities()
        prey_count = sum(1 for e in entities if e.prey)
        return {"prey": prey_count, "predators": len(entities) - prey_count}

    def run(self, iterations: int) -> list[dict[str, int]]:
        """
        Run the simulation for multiple chronons.

        >>> wt = WaTor(10, 10, prey_count=5, predator_count=3)
        >>> history = wt.run(5)
        >>> len(history)
        5
        """
        history = []
        for _ in range(iterations):
            history.append(self.step())
        return history

    def planet_to_string(self) -> str:
        """
        Convert the planet to a printable string.
        '#' = prey, 'x' = predator, '.' = empty.

        >>> wt = WaTor(3, 1, prey_count=0, predator_count=0)
        >>> wt.planet[0][1] = Entity(True, (0, 1))
        >>> wt.planet_to_string()
        '.#.'
        """
        lines = []
        for row in self.planet:
            line = ""
            for cell in row:
                if cell is None:
                    line += "."
                elif cell.prey:
                    line += "#"
                else:
                    line += "x"
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    print("Wa-Tor Predator-Prey Simulation")
    print("=" * 40)
    wt = WaTor(15, 15, prey_count=20, predator_count=10)
    print(f"Initial state:")
    print(wt.planet_to_string())

    for i in range(1, 6):
        counts = wt.step()
        print(f"\nChronon {i}: prey={counts['prey']}, predators={counts['predators']}")
        print(wt.planet_to_string())
