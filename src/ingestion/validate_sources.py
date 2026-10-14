"""Check that the required source files and columns exist before anything runs."""
import csv
from pathlib import Path

from src.config import REQUIRED_FILES


class SourceDataError(RuntimeError):
    pass


def validate_sources(data_dir: Path) -> None:
    data_dir = Path(data_dir)
    problems = []
    for name, cols in REQUIRED_FILES.items():
        f = data_dir / name
        if not f.exists():
            problems.append(f"missing file: {f}")
            continue
        with f.open(newline="", encoding="utf-8-sig") as fh:
            header = next(csv.reader(fh), [])
        missing = [c for c in cols if c not in header]
        if missing:
            problems.append(f"{name}: missing columns {missing}")
    if problems:
        raise SourceDataError(
            "Source data not usable. See data/raw/README.md for download steps.\n  " + "\n  ".join(problems))
