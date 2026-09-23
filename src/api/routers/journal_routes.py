"""Journal endpoints: read entries from the CSV, append new ones to it."""

from fastapi import APIRouter, HTTPException, Query, status

from src.api.models.journal_model import (
    EntryCreate,
    EntryCreated,
    EntryResponse,
    JournalCleared,
    Sentiment,
)
from src.api.utils.file_handler import (
    build_entry,
    clear_entries,
    load_entries,
    next_entry_id,
    save_entry_to_csv,
)
from src.core.config import FACE_SENTIMENTS, SENTIMENT_FACES

router = APIRouter(prefix="/journal", tags=["journal"])


def to_response(row: dict) -> dict:
    """Turn a raw CSV row into the shape the API returns."""
    return {
        "id": int(row["id"]),
        "message": row["message"],
        "mood": row["mood"],
        "sentiment": FACE_SENTIMENTS.get(row["mood"], "neutral"),
        "timestamp": row["timestamp"],
    }


@router.get("", response_model=list[EntryResponse], summary="List journal entries")
def get_entries(
    sentiment_filter: Sentiment | None = Query(
        default=None,
        description="Return only entries with this sentiment.",
    ),
) -> list[dict]:
    """Return every saved entry, oldest first, optionally narrowed to one sentiment."""
    entries = [to_response(row) for row in load_entries()]

    if sentiment_filter is None:
        return entries
    return [entry for entry in entries if entry["sentiment"] == sentiment_filter]


@router.post(
    "",
    response_model=EntryCreated,
    status_code=status.HTTP_201_CREATED,
    summary="Write a journal entry",
)
def create_entry(payload: EntryCreate) -> dict:
    """Validate the incoming entry and append it to the CSV."""
    entry = build_entry(
        entry_id=next_entry_id(load_entries()),
        message=payload.entry,
        mood=SENTIMENT_FACES[payload.sentiment],
    )

    try:
        save_entry_to_csv(entry)
    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not write to the journal file: {error}",
        ) from error

    return {"message": f"Saved entry #{entry['id']}", "entry": to_response(entry)}


@router.delete("", response_model=JournalCleared, summary="Delete every entry")
def delete_entries() -> dict:
    """Empty the journal. Numbering starts from 1 again afterwards."""
    try:
        removed = clear_entries()
    except OSError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not clear the journal file: {error}",
        ) from error

    return {"message": f"Cleared {removed} entries", "removed": removed}
