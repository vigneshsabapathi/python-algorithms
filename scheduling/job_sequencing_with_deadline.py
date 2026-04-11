"""
Job Sequencing with Deadline.

A variant of the job scheduling problem where jobs are represented as
dataclass objects with id, deadline, and profit. Uses a greedy algorithm
to maximize profit by scheduling jobs within their deadlines.

This implementation uses a different data representation than
job_sequence_with_deadline.py -- it uses a class-based approach with
named fields, which is closer to how real scheduling systems model tasks.

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/job_sequencing_with_deadline.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Job:
    """Represents a job with an ID, deadline, and profit."""

    job_id: str
    deadline: int
    profit: int

    def __repr__(self) -> str:
        return f"Job({self.job_id}, d={self.deadline}, p={self.profit})"


def job_sequencing_with_deadline(jobs: list[Job]) -> tuple[list[str], int]:
    """
    Schedule jobs to maximize total profit using greedy approach.

    Each job takes 1 unit of time and must complete by its deadline.
    Greedy: sort by profit desc, assign to latest available slot <= deadline.

    Args:
        jobs: list of Job objects

    Returns:
        (list of scheduled job IDs in time order, total profit)

    >>> jobs = [Job("J1", 4, 20), Job("J2", 1, 10), Job("J3", 1, 40), Job("J4", 1, 30)]
    >>> job_sequencing_with_deadline(jobs)
    (['J3', 'J1'], 60)

    >>> jobs = [Job("A", 2, 100), Job("B", 1, 19), Job("C", 2, 27), Job("D", 1, 25), Job("E", 3, 15)]
    >>> job_sequencing_with_deadline(jobs)
    (['C', 'A', 'E'], 142)

    >>> job_sequencing_with_deadline([])
    ([], 0)

    >>> job_sequencing_with_deadline([Job("X", 1, 50)])
    (['X'], 50)
    """
    if not jobs:
        return ([], 0)

    # Sort by profit descending
    sorted_jobs = sorted(jobs, key=lambda j: j.profit, reverse=True)

    max_deadline = max(j.deadline for j in sorted_jobs)

    # Time slots: 1-indexed, slot[i] = job_id or None
    slots: list[str | None] = [None] * (max_deadline + 1)
    total_profit = 0

    for job in sorted_jobs:
        # Try latest available slot before deadline
        for slot in range(min(job.deadline, max_deadline), 0, -1):
            if slots[slot] is None:
                slots[slot] = job.job_id
                total_profit += job.profit
                break

    # Collect in time order
    scheduled = [s for s in slots[1:] if s is not None]
    return (scheduled, total_profit)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    jobs = [
        Job("J1", 4, 20),
        Job("J2", 1, 10),
        Job("J3", 1, 40),
        Job("J4", 1, 30),
    ]
    result, profit = job_sequencing_with_deadline(jobs)
    print("Job Sequencing with Deadline")
    print(f"  Jobs:      {jobs}")
    print(f"  Scheduled: {result}")
    print(f"  Profit:    {profit}")
