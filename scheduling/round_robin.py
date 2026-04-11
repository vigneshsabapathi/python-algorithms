"""
Round Robin (RR) CPU Scheduling Algorithm.

A preemptive scheduling algorithm that assigns a fixed time quantum to each
process in circular order. If a process doesn't finish within its quantum,
it goes back to the end of the ready queue.

Key properties:
- Fair: every process gets equal CPU time in each cycle
- Preemptive: processes are interrupted after their quantum expires
- Time quantum selection is critical: too small = high overhead,
  too large = degenerates to FCFS

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/round_robin.py
"""

from __future__ import annotations

from collections import deque


def round_robin(
    arrival_times: list[int],
    burst_times: list[int],
    time_quantum: int,
) -> tuple[list[int], list[int], list[int]]:
    """
    Calculate CT, TAT, and WT for Round Robin scheduling.

    Args:
        arrival_times: list of arrival times for each process
        burst_times:   list of burst (execution) times for each process
        time_quantum:  fixed time slice for each process turn

    Returns:
        (completion_times, turnaround_times, waiting_times)

    >>> round_robin([0, 1, 2, 3], [5, 4, 2, 1], 2)
    ([12, 11, 6, 9], [12, 10, 4, 6], [7, 6, 2, 5])

    >>> round_robin([0, 0, 0], [4, 3, 2], 2)
    ([8, 9, 6], [8, 9, 6], [4, 6, 4])

    >>> round_robin([], [], 3)
    ([], [], [])

    >>> round_robin([0], [5], 2)
    ([5], [5], [0])

    >>> round_robin([0, 0], [3, 3], 3)
    ([3, 6], [3, 6], [0, 3])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    remaining = list(burst_times)
    ct = [0] * n
    ready_queue: deque[int] = deque()
    clock = 0
    done = 0

    # Track which processes are in the ready queue or completed
    in_queue = [False] * n
    completed = [False] * n

    # Sort process indices by arrival time for initial admission
    order = sorted(range(n), key=lambda i: (arrival_times[i], i))
    next_admit = 0

    def admit_processes(up_to: int) -> None:
        nonlocal next_admit
        while next_admit < n and arrival_times[order[next_admit]] <= up_to:
            idx = order[next_admit]
            if not in_queue[idx] and not completed[idx]:
                ready_queue.append(idx)
                in_queue[idx] = True
            next_admit += 1

    admit_processes(0)

    while done < n:
        if not ready_queue:
            # CPU idle -- jump to next arrival
            if next_admit < n:
                clock = arrival_times[order[next_admit]]
                admit_processes(clock)
                continue
            break

        idx = ready_queue.popleft()
        in_queue[idx] = False

        run_time = min(time_quantum, remaining[idx])
        clock += run_time
        remaining[idx] -= run_time

        # Admit any processes that arrived during this quantum
        admit_processes(clock)

        if remaining[idx] == 0:
            ct[idx] = clock
            completed[idx] = True
            done += 1
        else:
            # Put back at end of ready queue
            ready_queue.append(idx)
            in_queue[idx] = True

    tat = [ct[i] - arrival_times[i] for i in range(n)]
    wt = [tat[i] - burst_times[i] for i in range(n)]
    return (ct, tat, wt)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    arrivals = [0, 1, 2, 3]
    bursts = [5, 4, 2, 1]
    quantum = 2
    ct, tat, wt = round_robin(arrivals, bursts, quantum)
    print("Round Robin Scheduling")
    print(f"  Arrival Times:    {arrivals}")
    print(f"  Burst Times:      {bursts}")
    print(f"  Time Quantum:     {quantum}")
    print(f"  Completion Times: {ct}")
    print(f"  Turnaround Times: {tat}")
    print(f"  Waiting Times:    {wt}")
    print(f"  Avg Turnaround:   {sum(tat)/len(tat):.2f}")
    print(f"  Avg Waiting:      {sum(wt)/len(wt):.2f}")
