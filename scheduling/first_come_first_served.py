"""
First Come First Served (FCFS) CPU Scheduling Algorithm.

Processes are executed in the order they arrive. This is the simplest
scheduling algorithm — a non-preemptive FIFO queue.

Given a list of process arrival times and burst times, compute:
  - Completion Time (CT)
  - Turnaround Time (TAT = CT - AT)
  - Waiting Time (WT = TAT - BT)

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/first_come_first_served.py
"""

from __future__ import annotations


def first_come_first_served(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    Calculate CT, TAT, and WT for FCFS scheduling.

    Processes are sorted by arrival time; ties broken by original order.

    Args:
        arrival_times: list of arrival times for each process
        burst_times:   list of burst (execution) times for each process

    Returns:
        (completion_times, turnaround_times, waiting_times)

    >>> first_come_first_served([0, 1, 2, 3], [4, 3, 1, 2])
    ([4, 7, 8, 10], [4, 6, 6, 7], [0, 3, 5, 5])

    >>> first_come_first_served([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])

    >>> first_come_first_served([2, 0, 4], [3, 2, 1])
    ([5, 2, 6], [3, 2, 2], [0, 0, 1])

    >>> first_come_first_served([], [])
    ([], [], [])

    >>> first_come_first_served([0], [5])
    ([5], [5], [0])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    # Pair each process with its original index, sort by arrival time
    processes = sorted(range(n), key=lambda i: (arrival_times[i], i))

    completion_times = [0] * n
    turnaround_times = [0] * n
    waiting_times = [0] * n

    current_time = 0
    for idx in processes:
        at = arrival_times[idx]
        bt = burst_times[idx]
        # CPU may be idle if next process hasn't arrived yet
        if current_time < at:
            current_time = at
        current_time += bt
        completion_times[idx] = current_time
        turnaround_times[idx] = current_time - at
        waiting_times[idx] = turnaround_times[idx] - bt

    return (completion_times, turnaround_times, waiting_times)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    arrivals = [0, 1, 2, 3]
    bursts = [4, 3, 1, 2]
    ct, tat, wt = first_come_first_served(arrivals, bursts)
    print("FCFS Scheduling")
    print(f"  Arrival Times:    {arrivals}")
    print(f"  Burst Times:      {bursts}")
    print(f"  Completion Times: {ct}")
    print(f"  Turnaround Times: {tat}")
    print(f"  Waiting Times:    {wt}")
    print(f"  Avg Turnaround:   {sum(tat)/len(tat):.2f}")
    print(f"  Avg Waiting:      {sum(wt)/len(wt):.2f}")
