"""
Activity Selection Problem — Greedy algorithm to select maximum non-overlapping activities.

Given a set of activities with start and finish times, select the maximum number
of activities that can be performed by a single person, assuming they can only
work on one activity at a time.

Reference: https://github.com/TheAlgorithms/Python/blob/master/other/activity_selection.py
"""

from __future__ import annotations


def activity_selection(
    activities: list[tuple[int, int]],
) -> list[tuple[int, int]]:
    """
    Select the maximum number of non-overlapping activities.

    Each activity is a (start, finish) tuple.  The greedy strategy sorts by
    finish time and picks the next compatible activity.

    >>> activity_selection([(1, 2), (3, 4), (0, 6), (5, 7), (8, 9), (5, 9)])
    [(1, 2), (3, 4), (5, 7), (8, 9)]
    >>> activity_selection([(0, 6), (1, 2), (3, 5), (4, 7)])
    [(1, 2), (3, 5)]
    >>> activity_selection([])
    []
    >>> activity_selection([(1, 3)])
    [(1, 3)]
    >>> activity_selection([(1, 2), (2, 3)])
    [(1, 2), (2, 3)]
    """
    if not activities:
        return []

    # Sort by finish time
    sorted_activities = sorted(activities, key=lambda x: x[1])
    selected = [sorted_activities[0]]

    for i in range(1, len(sorted_activities)):
        # If start time >= last selected finish time, it's compatible
        if sorted_activities[i][0] >= selected[-1][1]:
            selected.append(sorted_activities[i])

    return selected


if __name__ == "__main__":
    import doctest

    doctest.testmod()
