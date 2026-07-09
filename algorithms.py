from typing import List, Dict, Any

from process import Process


def _finalize_metrics(processes: List[Process], finish_time: float) -> None:
    for process in processes:
        if process.completion_time == 0.0:
            process.completion_time = finish_time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
        if process.response_time is None:
            process.response_time = 0.0


def _build_result(processes: List[Process], timeline: List[tuple], algorithm_name: str) -> Dict[str, Any]:
    total_time = max([p.completion_time for p in processes], default=0.0)
    _finalize_metrics(processes, total_time)

    avg_waiting = round(sum(p.waiting_time for p in processes) /
                        len(processes), 2) if processes else 0.0
    avg_turnaround = round(sum(
        p.turnaround_time for p in processes) / len(processes), 2) if processes else 0.0
    avg_response = round(sum(p.response_time or 0.0 for p in processes) /
                         len(processes), 2) if processes else 0.0
    cpu_utilization = round(
        (sum(p.burst_time for p in processes) / total_time) * 100, 2) if total_time else 0.0
    throughput = round(len(processes) / total_time, 2) if total_time else 0.0

    return {
        "algorithm": algorithm_name,
        "processes": [p.to_dict() for p in processes],
        "timeline": timeline,
        "avg_waiting_time": avg_waiting,
        "avg_turnaround_time": avg_turnaround,
        "avg_response_time": avg_response,
        "cpu_utilization": cpu_utilization,
        "throughput": throughput,
        "completion_time": round(total_time, 2),
    }


def fcfs(processes: List[Process]) -> Dict[str, Any]:
    """First Come First Serve: run processes in arrival order."""

    current_time = 0.0
    timeline: List[tuple] = []
    ordered = sorted(processes, key=lambda p: (p.arrival_time, p.pid))

    for process in ordered:
        if current_time < process.arrival_time:
            current_time = process.arrival_time

        start_time = current_time
        process.response_time = current_time - process.arrival_time
        current_time += process.burst_time
        process.completion_time = current_time
        timeline.append((process.pid, start_time, current_time))

    return _build_result(ordered, timeline, "FCFS")


def sjf_non_preemptive(processes: List[Process]) -> Dict[str, Any]:
    """Shortest Job First: pick the shortest burst among arrived processes."""

    current_time = 0.0
    timeline: List[tuple] = []
    remaining = list(processes)

    while remaining:
        available = [p for p in remaining if p.arrival_time <= current_time]
        if not available:
            next_arrival = min(p.arrival_time for p in remaining)
            current_time = next_arrival
            continue

        chosen = min(available, key=lambda p: (
            p.burst_time, p.arrival_time, p.pid))
        if current_time < chosen.arrival_time:
            current_time = chosen.arrival_time
        start_time = current_time
        chosen.response_time = current_time - chosen.arrival_time
        current_time += chosen.burst_time
        chosen.completion_time = current_time
        timeline.append((chosen.pid, start_time, current_time))
        remaining.remove(chosen)

    return _build_result(sorted(processes, key=lambda p: p.pid), timeline, "SJF (Non-Preemptive)")


def srtf(processes: List[Process]) -> Dict[str, Any]:
    """Shortest Remaining Time First: preemptive version of SJF."""

    current_time = 0.0
    timeline: List[tuple] = []
    remaining_processes = list(processes)

    while remaining_processes:
        available = [p for p in remaining_processes if p.arrival_time <=
                     current_time and p.remaining_time > 0]
        if not available:
            next_arrival = min(
                p.arrival_time for p in remaining_processes if p.remaining_time > 0)
            current_time = next_arrival
            continue

        chosen = min(available, key=lambda p: (
            p.remaining_time, p.arrival_time, p.pid))
        if chosen.response_time is None:
            chosen.response_time = current_time - chosen.arrival_time

        next_arrival_time = min(
            [p.arrival_time for p in remaining_processes if p.arrival_time >
                current_time and p.remaining_time > 0],
            default=float("inf"),
        )
        run_until = min(current_time + chosen.remaining_time,
                        next_arrival_time)
        start_time = current_time
        chosen.remaining_time -= run_until - current_time
        current_time = run_until
        timeline.append((chosen.pid, start_time, current_time))

        if chosen.remaining_time <= 0.0:
            chosen.completion_time = current_time
            remaining_processes.remove(chosen)

    return _build_result(sorted(processes, key=lambda p: p.pid), timeline, "SRTF")


def priority_scheduling(processes: List[Process]) -> Dict[str, Any]:
    """Priority scheduling: lower numeric priority value is higher importance."""

    current_time = 0.0
    timeline: List[tuple] = []
    ordered = sorted(processes, key=lambda p: (
        p.arrival_time, p.priority, p.pid))

    for process in ordered:
        if current_time < process.arrival_time:
            current_time = process.arrival_time
        start_time = current_time
        process.response_time = current_time - process.arrival_time
        current_time += process.burst_time
        process.completion_time = current_time
        timeline.append((process.pid, start_time, current_time))

    return _build_result(ordered, timeline, "Priority Scheduling")


def round_robin(processes: List[Process], quantum: float) -> Dict[str, Any]:
    """Round Robin: give each process a time slice of the given quantum."""

    from collections import deque

    current_time = 0.0
    timeline: List[tuple] = []
    queue = deque()
    remaining = list(processes)

    while remaining:
        arrived = [p for p in remaining if p.arrival_time <=
                   current_time and p.remaining_time > 0]
        for process in sorted(arrived, key=lambda p: (p.arrival_time, p.pid)):
            if process not in queue:
                queue.append(process)

        if not queue:
            next_arrival = min(
                p.arrival_time for p in remaining if p.remaining_time > 0)
            current_time = next_arrival
            continue

        current = queue.popleft()
        if current.response_time is None:
            current.response_time = current_time - current.arrival_time

        start_time = current_time
        run_time = min(quantum, current.remaining_time)
        current_time += run_time
        current.remaining_time -= run_time
        timeline.append((current.pid, start_time, current_time))

        if current.remaining_time <= 0.0:
            current.completion_time = current_time
            remaining.remove(current)
        else:
            queue.append(current)

    return _build_result(sorted(processes, key=lambda p: p.pid), timeline, "Round Robin")
