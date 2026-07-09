from typing import Dict, List

from algorithms import fcfs, priority_scheduling, round_robin, sjf_non_preemptive, srtf
from process import Process, clone_processes


def run_selected_algorithm(processes: List[Process], algorithm: str, quantum: float = 2.0) -> Dict[str, object]:
    """Run one scheduling algorithm and return its results."""

    fresh_processes = clone_processes(processes)
    name = algorithm.lower()

    if name == "fcfs":
        return fcfs(fresh_processes)
    if name == "sjf" or name == "sjf (non-preemptive)":
        return sjf_non_preemptive(fresh_processes)
    if name == "srtf":
        return srtf(fresh_processes)
    if name == "priority" or name == "priority scheduling":
        return priority_scheduling(fresh_processes)
    if name == "round robin" or name == "rr":
        return round_robin(fresh_processes, quantum)
    if name == "all algorithms" or name == "compare all":
        return compare_algorithms(processes, quantum)
    return fcfs(fresh_processes)


def compare_algorithms(processes: List[Process], quantum: float = 2.0) -> Dict[str, object]:
    """Execute every algorithm and return a comparison dictionary."""

    results = {
        "FCFS": run_selected_algorithm(processes, "FCFS", quantum),
        "SJF (Non-Preemptive)": run_selected_algorithm(processes, "SJF", quantum),
        "SRTF": run_selected_algorithm(processes, "SRTF", quantum),
        "Priority Scheduling": run_selected_algorithm(processes, "Priority", quantum),
        "Round Robin": run_selected_algorithm(processes, "Round Robin", quantum),
    }
    return {"comparison": results}
