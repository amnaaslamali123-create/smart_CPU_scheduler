import json
from pathlib import Path
from typing import Any, Dict, List

from process import Process


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLE_DATA_FILE = DATA_DIR / "sample_processes.json"


def load_sample_data() -> List[Process]:
    """Load the built-in sample processes from a JSON file."""

    if not SAMPLE_DATA_FILE.exists():
        return []

    with SAMPLE_DATA_FILE.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    return [Process.from_dict(item) for item in data]


def save_results_json(path: str, data: Dict[str, Any]) -> None:
    """Save scheduling results to a JSON file."""

    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def export_to_pdf(path: str, content: str) -> None:
    """Create a simple PDF file from text content."""

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
