"""
Highest Response Ratio Next (HRRN) CPU Scheduling Algorithm.

Non-preemptive scheduling that selects the process with the highest
response ratio at each scheduling decision point.

Response Ratio = (Waiting Time + Burst Time) / Burst Time

This favors shorter jobs while also aging longer-waiting jobs, avoiding
starvation — a key improvement over Shortest Job First (SJF).

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/highest_response_ratio_next.py
"""

from __future__ import annotations


def highest_response_ratio_next(
    arrival_times: list[int], burst_times: list[int]
) -> tuple[list[int], list[int], list[int]]:
    """
    Calculate CT, TAT, and WT for HRRN scheduling.

    At each decision point (when CPU becomes free), pick the arrived process
    with the highest response ratio: (waiting_time + burst_time) / burst_time.

    Args:
        arrival_times: list of arrival times for each process
        burst_times:   list of burst (execution) times for each process

    Returns:
        (completion_times, turnaround_times, waiting_times)

    >>> highest_response_ratio_next([0, 2, 4, 6], [3, 5, 2, 4])
    ([3, 8, 10, 14], [3, 6, 6, 8], [0, 1, 4, 4])

    >>> highest_response_ratio_next([0, 0, 0], [5, 3, 8])
    ([5, 8, 16], [5, 8, 16], [0, 5, 8])

    >>> highest_response_ratio_next([], [])
    ([], [], [])

    >>> highest_response_ratio_next([0], [10])
    ([10], [10], [0])
    """
    n = len(arrival_times)
    if n == 0:
        return ([], [], [])

    completed = [False] * n
    ct = [0] * n
    tat = [0] * n
    wt = [0] * n
    current_time = 0
    done = 0

    while done < n:
        # Find all arrived, not-yet-completed processes
        ready = []
        for i in range(n):
            if not completed[i] and arrival_times[i] <= current_time:
                waiting = current_time - arrival_times[i]
                response_ratio = (waiting + burst_times[i]) / burst_times[i]
                ready.append((response_ratio, i))

        if not ready:
            # CPU idle — jump to next arrival
            next_arrival = min(
                arrival_times[i] for i in range(n) if not completed[i]
            )
            current_time = next_arrival
            continue

        # Pick highest response ratio (ties broken by earlier arrival / index)
        ready.sort(key=lambda x: (-x[0], arrival_times[x[1]], x[1]))
        _, chosen = ready[0]

        current_time += burst_times[chosen]
        ct[chosen] = current_time
        tat[chosen] = current_time - arrival_times[chosen]
        wt[chosen] = tat[chosen] - burst_times[chosen]
        completed[chosen] = True
        done += 1

    return (ct, tat, wt)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    arrivals = [0, 2, 4, 6]
    bursts = [3, 5, 2, 4]
    ct, tat, wt = highest_response_ratio_next(arrivals, bursts)
    print("HRRN Scheduling")
    print(f"  Arrival Times:    {arrivals}")
    print(f"  Burst Times:      {bursts}")
    print(f"  Completion Times: {ct}")
    print(f"  Turnaround Times: {tat}")
    print(f"  Waiting Times:    {wt}")
    print(f"  Avg Turnaround:   {sum(tat)/len(tat):.2f}")
    print(f"  Avg Waiting:      {sum(wt)/len(wt):.2f}")
