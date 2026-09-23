"""
Secret Journal : A terminal journal that stores entries in a CSV file.

Day 1 of the Python upskilling series: variables, input, f-strings, dicts, loops, functions, type hints and file handling.

Run it with:  python journal.py
"""

import csv
import os
from datetime import datetime

CSV_FILE = "journal.csv"
CSV_COLUMNS = ["id", "message", "mood", "timestamp"]

MOOD_FACES = {
    "happy": ":)",
    "sad": ":(",
    "neutral": ":|",
}

DEFAULT_NAME = "TJ"

def get_user_name() -> str:
    """Ask who is journaling, falling back to the owner of this journal."""
    name = input("Enter your name: ").strip()
    if not name:
        return DEFAULT_NAME
    return name


def ask_for_message() -> str:
    """Keep asking until the user types a message that is not empty."""
    while True:
        message = input("Write your journal message: ").strip()
        if message:
            return message
        print("An entry cannot be empty — write at least one word.")


def ask_for_mood() -> str:
    """Keep asking until the mood is one we know, then return its ASCII face."""
    while True:
        mood = input("How do you feel today? (happy/sad/neutral): ").strip().lower()
        if mood in MOOD_FACES:
            return MOOD_FACES[mood]
        print(f"'{mood}' is not a mood I know. Choose happy, sad or neutral.")


def create_entry(entry_id: int) -> dict:
    """Create a new journal entry with user input and validation."""
    message = ask_for_message()
    mood = ask_for_mood()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    return {
        "id": entry_id,
        "message": message,
        "mood": mood,
        "timestamp": timestamp,
    }


def save_entry_to_csv(entry: dict) -> None:
    """Append one entry to the CSV, writing the header row if the file is new."""
    file_is_new = not os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        if file_is_new:
            writer.writeheader()
        writer.writerow(entry)


def load_entries() -> list:
    """Read every saved entry back from the CSV, or [] if there is no file yet."""
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def next_entry_id(entries: list) -> int:
    """Pick the next id, so numbering keeps counting across restarts."""
    if not entries:
        return 1
    return max(int(entry["id"]) for entry in entries) + 1


def display_entries(entries: list) -> None:
    """Print the saved entries, one per line, oldest first."""
    if not entries:
        print("\nNothing here yet — option 1 starts your first entry.\n")
        return

    print("\n------ Journal Entries ------")
    for entry in entries:
        date = entry["timestamp"].split()[0]  # show the date, drop the time
        print(f"{entry['id']} | {entry['mood']} | {entry['message']} | {date}")
    print("-----------------------------\n")


def show_menu() -> None:
    """Print the menu options."""
    print("What would you like to do?")
    print("  1. Write a new journal entry")
    print("  2. View saved entries")
    print("  3. Exit")


def handle_new_entry() -> None:
    """Build one entry and append it to the CSV."""
    entries = load_entries()
    entry = create_entry(next_entry_id(entries))
    save_entry_to_csv(entry)
    print(f"\nSaved entry #{entry['id']} to {CSV_FILE}.\n")


def main() -> None:
    """Greet the user, then run the menu until they choose to exit."""
    print("Welcome to the Secret Journal!")
    name = get_user_name()
    print(f"\nHello {name} 👋 Let's start journaling!\n")

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            handle_new_entry()
        elif choice == "2":
            display_entries(load_entries())
        elif choice == "3":
            print(f"\nThat's a wrap, {name}. Your entries are safe in {CSV_FILE}.")
            return
        else:
            print("\nPlease choose 1, 2 or 3.\n")


if __name__ == "__main__":
    main()
