from typing import Dict, List

from algorithms import fcfs, priority_scheduling, round_robin, sjf_non_preemptive, srtf
from process import Process, clone_processes


def recommend_best_algorithm(processes: List[Process], quantum: float = 2.0) -> Dict[str, object]:
    """Recommend a scheduling algorithm using a beginner-friendly heuristic."""

    candidates: List[str] = []
    if len(processes) >= 6 and quantum > 0:
        candidates.append("Round Robin")
    if any(process.priority != 0 for process in processes):
        candidates.append("Priority Scheduling")
    if len(processes) >= 4 and any(process.arrival_time != 0 for process in processes):
        candidates.append("SRTF")
    if len(processes) <= 4 and all(process.arrival_time == 0 for process in processes):
        candidates.append("SJF (Non-Preemptive)")
    if not candidates:
        candidates = ["FCFS"]

    results: Dict[str, Dict[str, object]] = {}
    for name in candidates:
        fresh = clone_processes(processes)
        if name == "FCFS":
            results[name] = fcfs(fresh)
        elif name == "SJF (Non-Preemptive)":
            results[name] = sjf_non_preemptive(fresh)
        elif name == "SRTF":
            results[name] = srtf(fresh)
        elif name == "Priority Scheduling":
            results[name] = priority_scheduling(fresh)
        elif name == "Round Robin":
            results[name] = round_robin(fresh, quantum)

    ranked = sorted(
        results.items(),
        key=lambda item: (
            item[1]["avg_waiting_time"],
            item[1]["avg_turnaround_time"],
            item[1]["avg_response_time"],
        ),
    )
    best_name, best_result = ranked[0]

    reason = (
        f"The system recommends {best_name} because it produced the lowest average waiting time "
        f"({best_result['avg_waiting_time']}) among the best-fitting algorithms for your workload."
    )

    return {
        "recommended_algorithm": best_name,
        "result": best_result,
        "results": results,
        "reason": reason,
    }
