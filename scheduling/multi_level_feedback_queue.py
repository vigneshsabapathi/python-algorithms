"""
Multi-Level Feedback Queue (MLFQ) CPU Scheduling Algorithm.

MLFQ uses multiple queues with different priority levels. Processes start
in the highest-priority queue and get demoted to lower-priority queues if
they use up their time quantum. Lower queues have larger time quanta.

Key rules:
1. New processes enter the highest-priority queue.
2. If a process uses its entire time quantum, it moves down one level.
3. If a process completes or blocks before the quantum expires, it stays.
4. Higher-priority queues are served first (preemptive over lower queues).

This implementation uses Round Robin within each queue level.

Reference: https://github.com/TheAlgorithms/Python/blob/master/scheduling/multi_level_feedback_queue.py
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass
class Process:
    """A process in the MLFQ system."""

    pid: str
    arrival_time: int
    burst_time: int
    remaining_time: int = field(init=False)
    completion_time: int = 0
    current_queue: int = 0

    def __post_init__(self) -> None:
        self.remaining_time = self.burst_time


def multi_level_feedback_queue(
    processes: list[tuple[str, int, int]],
    time_quanta: list[int] | None = None,
    num_queues: int = 3,
) -> list[dict[str, int | str]]:
    """
    Simulate MLFQ scheduling.

    Args:
        processes:   list of (pid, arrival_time, burst_time)
        time_quanta: time quantum for each queue level (default: [4, 8, 16])
        num_queues:  number of queue levels

    Returns:
        list of dicts with pid, arrival, burst, completion, turnaround, waiting

    >>> result = multi_level_feedback_queue([("P1", 0, 10), ("P2", 1, 5), ("P3", 2, 3)])
    >>> [(r["pid"], r["completion"], r["turnaround"], r["waiting"]) for r in result]
    [('P1', 17, 17, 7), ('P2', 18, 17, 12), ('P3', 11, 9, 6)]

    >>> result = multi_level_feedback_queue([("A", 0, 2)])
    >>> [(r["pid"], r["completion"]) for r in result]
    [('A', 2)]

    >>> multi_level_feedback_queue([])
    []

    >>> result = multi_level_feedback_queue([("P1", 0, 3), ("P2", 0, 3)], time_quanta=[2, 4])
    >>> [(r["pid"], r["completion"]) for r in result]
    [('P1', 5), ('P2', 6)]
    """
    if not processes:
        return []

    if time_quanta is None:
        time_quanta = [4, 8, 16]
    # Extend time quanta if fewer than num_queues
    while len(time_quanta) < num_queues:
        time_quanta.append(time_quanta[-1] * 2)

    # Create process objects
    procs = [Process(pid, at, bt) for pid, at, bt in processes]
    procs.sort(key=lambda p: (p.arrival_time, p.pid))

    queues: list[deque[Process]] = [deque() for _ in range(num_queues)]
    completed: list[Process] = []
    clock = 0
    proc_idx = 0  # next process to add

    def add_arriving_processes(up_to_time: int) -> None:
        nonlocal proc_idx
        while proc_idx < len(procs) and procs[proc_idx].arrival_time <= up_to_time:
            queues[0].append(procs[proc_idx])
            proc_idx += 1

    # Add processes arriving at time 0
    add_arriving_processes(0)

    while len(completed) < len(procs):
        # Find highest priority non-empty queue
        current_q = -1
        for q in range(num_queues):
            if queues[q]:
                current_q = q
                break

        if current_q == -1:
            # CPU idle -- jump to next arrival
            if proc_idx < len(procs):
                clock = procs[proc_idx].arrival_time
                add_arriving_processes(clock)
                continue
            else:
                break  # no more processes

        process = queues[current_q].popleft()
        quantum = time_quanta[current_q]
        run_time = min(quantum, process.remaining_time)

        # Execute for run_time units, checking for new arrivals each tick
        for t in range(run_time):
            clock += 1
            add_arriving_processes(clock)

        process.remaining_time -= run_time

        if process.remaining_time == 0:
            process.completion_time = clock
            completed.append(process)
        else:
            # Demote to next queue (or stay in lowest)
            next_q = min(current_q + 1, num_queues - 1)
            process.current_queue = next_q
            queues[next_q].append(process)

    # Build results in original input order
    proc_map = {p.pid: p for p in completed}
    results = []
    for pid, at, bt in processes:
        p = proc_map[pid]
        ct = p.completion_time
        tat = ct - at
        wt = tat - bt
        results.append({
            "pid": pid,
            "arrival": at,
            "burst": bt,
            "completion": ct,
            "turnaround": tat,
            "waiting": wt,
        })

    return results


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    processes = [("P1", 0, 10), ("P2", 1, 5), ("P3", 2, 3)]
    results = multi_level_feedback_queue(processes)
    print("MLFQ Scheduling")
    print(f"  Time Quanta: [4, 8, 16]")
    print(f"  {'PID':<6} {'AT':<6} {'BT':<6} {'CT':<6} {'TAT':<6} {'WT':<6}")
    for r in results:
        print(
            f"  {r['pid']:<6} {r['arrival']:<6} {r['burst']:<6} "
            f"{r['completion']:<6} {r['turnaround']:<6} {r['waiting']:<6}"
        )
    avg_tat = sum(r["turnaround"] for r in results) / len(results)
    avg_wt = sum(r["waiting"] for r in results) / len(results)
    print(f"  Avg TAT: {avg_tat:.2f}  Avg WT: {avg_wt:.2f}")
