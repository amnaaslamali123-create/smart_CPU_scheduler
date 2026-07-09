from typing import Dict, List

import matplotlib.pyplot as plt

from process import Process


def draw_gantt_chart(result: Dict[str, object]) -> None:
    """Draw a simple Gantt Chart for one algorithm result."""

    timeline = result.get("timeline", [])
    if not timeline:
        return

    fig, ax = plt.subplots(figsize=(10, 3))
    y_positions = [0] * len(timeline)
    for idx, (pid, start, end) in enumerate(timeline):
        ax.barh(pid, end - start, left=start,
                color="tab:blue", edgecolor="black")
        ax.text(start + (end - start) / 2, pid, pid, ha="center", va="center")

    ax.set_title("Gantt Chart")
    ax.set_xlabel("Time")
    ax.set_ylabel("Process")
    ax.set_xticks([0, max([item[2] for item in timeline], default=0)])
    plt.tight_layout()
    plt.show()


def draw_comparison_graph(results: Dict[str, object]) -> None:
    """Create a bar chart comparing average waiting times across algorithms."""

    comparison = results.get("comparison", {})
    algorithms = list(comparison.keys())
    waiting_times = [comparison[name]["avg_waiting_time"]
                     for name in algorithms]

    plt.figure(figsize=(8, 4))
    plt.bar(algorithms, waiting_times, color="tab:orange")
    plt.title("Average Waiting Time Comparison")
    plt.ylabel("Average Waiting Time")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()
