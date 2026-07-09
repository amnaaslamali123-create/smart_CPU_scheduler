from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Process:
    """Represents one CPU process with scheduling-related information."""

    pid: str
    arrival_time: float
    burst_time: float
    priority: int
    waiting_time: float = 0.0
    turnaround_time: float = 0.0
    completion_time: float = 0.0
    response_time: Optional[float] = None
    remaining_time: float = field(init=False)

    def __post_init__(self) -> None:
        self.remaining_time = self.burst_time

    def to_dict(self) -> Dict[str, object]:
        return {
            "pid": self.pid,
            "arrival_time": self.arrival_time,
            "burst_time": self.burst_time,
            "priority": self.priority,
            "waiting_time": self.waiting_time,
            "turnaround_time": self.turnaround_time,
            "completion_time": self.completion_time,
            "response_time": self.response_time,
        }

    @classmethod
    def from_dict(cls, item: Dict[str, object]) -> "Process":
        return cls(
            pid=str(item["pid"]),
            arrival_time=float(item["arrival_time"]),
            burst_time=float(item["burst_time"]),
            priority=int(item["priority"]),
        )


def clone_processes(processes: List[Process]) -> List[Process]:
    """Create a fresh copy of the process list so each algorithm can work safely."""

    return [Process.from_dict(process.to_dict()) for process in processes]
