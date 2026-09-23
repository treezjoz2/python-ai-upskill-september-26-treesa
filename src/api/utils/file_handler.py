"""CSV storage for journal entries, shared by the CLI and the API."""

import csv
from datetime import datetime

from src.core.config import CSV_COLUMNS, CSV_FILE


def load_entries() -> list[dict]:
    """Read every saved entry from the CSV, or [] if there is no file yet."""
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def save_entry_to_csv(entry: dict) -> None:
    """Append one entry, writing the header row if the file is new."""
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_is_new = not CSV_FILE.exists()

    # newline="" stops the csv module adding a blank line between rows.
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        if file_is_new:
            writer.writeheader()
        writer.writerow(entry)


def clear_entries() -> int:
    """Delete every entry, keeping the header row. Returns how many were removed."""
    removed = len(load_entries())

    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        csv.DictWriter(file, fieldnames=CSV_COLUMNS).writeheader()

    return removed


def next_entry_id(entries: list[dict]) -> int:
    """Pick the next id, so numbering keeps counting across restarts."""
    if not entries:
        return 1
    return max(int(entry["id"]) for entry in entries) + 1


def build_entry(entry_id: int, message: str, mood: str) -> dict:
    """Assemble one entry row. Stores nothing on its own."""
    return {
        "id": entry_id,
        "message": message,
        "mood": mood,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
