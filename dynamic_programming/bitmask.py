"""
Task Assignment Using Bitmask DP

Given N tasks and M people, where each person can only do certain tasks,
find the total number of ways to distribute tasks such that:
  - Each person does exactly one task
  - Each task is done by at most one person
  - All people get assigned a task

Uses bitmask DP where the mask represents which people have been assigned.

>>> task_performed = [[1, 3, 4], [1, 2, 5], [3, 4]]
>>> AssignmentUsingBitmask(task_performed, 5).count_no_of_ways(task_performed)
10
"""

from __future__ import annotations

from collections import defaultdict


class AssignmentUsingBitmask:
    """
    Solves the task assignment problem using bitmask dynamic programming.

    >>> solver = AssignmentUsingBitmask([[1, 3, 4], [1, 2, 5], [3, 4]], 5)
    >>> solver.count_no_of_ways([[1, 3, 4], [1, 2, 5], [3, 4]])
    10
    >>> solver2 = AssignmentUsingBitmask([[1, 2], [1, 2]], 2)
    >>> solver2.count_no_of_ways([[1, 2], [1, 2]])
    2
    """

    def __init__(self, task_performed: list[list[int]], total: int) -> None:
        self.total_tasks = total
        self.dp = [
            [-1 for _ in range(total + 1)]
            for _ in range(2 ** len(task_performed))
        ]
        self.task: dict[int, list[int]] = defaultdict(list)
        self.final_mask = (1 << len(task_performed)) - 1

    def count_ways_until(self, mask: int, task_no: int) -> int:
        if mask == self.final_mask:
            return 1
        if task_no > self.total_tasks:
            return 0
        if self.dp[mask][task_no] != -1:
            return self.dp[mask][task_no]

        # Ways when we skip this task
        total_ways_until = self.count_ways_until(mask, task_no + 1)

        # Try assigning this task to each eligible person
        if task_no in self.task:
            for p in self.task[task_no]:
                if mask & (1 << p):
                    continue
                total_ways_until += self.count_ways_until(
                    mask | (1 << p), task_no + 1
                )

        self.dp[mask][task_no] = total_ways_until
        return self.dp[mask][task_no]

    def count_no_of_ways(self, task_performed: list[list[int]]) -> int:
        # Build task -> person mapping
        for i in range(len(task_performed)):
            for j in task_performed[i]:
                self.task[j].append(i)
        return self.count_ways_until(0, 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    print("Doctests passed.")

    total_tasks = 5
    task_performed = [[1, 3, 4], [1, 2, 5], [3, 4]]
    result = AssignmentUsingBitmask(task_performed, total_tasks).count_no_of_ways(
        task_performed
    )
    print(f"  Tasks can be distributed in {result} ways")
    print("  Expected: 10")
    print("  Distributions: (1,2,3), (1,2,4), (1,5,3), (1,5,4), (3,1,4),")
    print("                 (3,2,4), (3,5,4), (4,1,3), (4,2,3), (4,5,3)")
