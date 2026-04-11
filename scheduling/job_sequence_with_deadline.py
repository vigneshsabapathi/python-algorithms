"""
Job Sequence with Deadline (Greedy approach).

Given a set of jobs where each job has a deadline and profit, schedule jobs
on a single machine to maximize total profit. Each job takes one unit of time,
and only one job can be scheduled at a time. A job must finish before its deadline.

Greedy strategy: Sort jobs by profit (descending), assign each to the latest
available slot before its deadline.

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/job_sequence_with_deadline.py
"""

from __future__ import annotations


def job_sequence_with_deadline(
    jobs: list[tuple[str, int, int]],
) -> tuple[list[str], int]:
    """
    Schedule jobs to maximize profit using a greedy approach.

    Each job is a tuple: (job_id, deadline, profit).
    Jobs take 1 unit of time each. A job must complete by its deadline.

    Args:
        jobs: list of (job_id, deadline, profit) tuples

    Returns:
        (scheduled_job_ids, total_profit)

    >>> job_sequence_with_deadline([("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)])
    (['J2', 'J1', 'J3'], 180)

    >>> job_sequence_with_deadline([("A", 1, 50), ("B", 1, 40)])
    (['A'], 50)

    >>> job_sequence_with_deadline([])
    ([], 0)

    >>> job_sequence_with_deadline([("X", 3, 10)])
    (['X'], 10)
    """
    if not jobs:
        return ([], 0)

    # Sort by profit descending
    sorted_jobs = sorted(jobs, key=lambda j: j[2], reverse=True)

    # Find max deadline to determine slot count
    max_deadline = max(j[1] for j in sorted_jobs)

    # Slots: index 0 unused, slots 1..max_deadline
    slots = [None] * (max_deadline + 1)
    total_profit = 0
    scheduled = []

    for job_id, deadline, profit in sorted_jobs:
        # Try to place in latest available slot <= deadline
        for slot in range(min(deadline, max_deadline), 0, -1):
            if slots[slot] is None:
                slots[slot] = job_id
                total_profit += profit
                break

    # Collect scheduled jobs in time order
    scheduled = [slots[i] for i in range(1, max_deadline + 1) if slots[i] is not None]

    return (scheduled, total_profit)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    jobs = [("J1", 2, 60), ("J2", 1, 100), ("J3", 3, 20), ("J4", 2, 40)]
    result, profit = job_sequence_with_deadline(jobs)
    print("Job Sequence with Deadline")
    print(f"  Jobs:      {jobs}")
    print(f"  Scheduled: {result}")
    print(f"  Profit:    {profit}")
