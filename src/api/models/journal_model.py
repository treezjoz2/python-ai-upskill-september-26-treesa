"""Pydantic models describing what the journal API accepts and returns."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

from src.core.config import MAX_ENTRY_LENGTH

Sentiment = Literal["positive", "negative", "neutral"]


class EntryCreate(BaseModel):
    """Body of POST /journal."""

    entry: str = Field(
        min_length=1,
        max_length=MAX_ENTRY_LENGTH,
        description="The journal message, 1-500 characters.",
    )
    sentiment: Sentiment = Field(
        default="neutral",
        description="How the entry felt. Stored as the Day 1 mood face.",
    )

    @field_validator("entry")
    @classmethod
    def reject_whitespace_only(cls, value: str) -> str:
        """Treat an entry of only spaces as empty, and trim what we store."""
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Entry cannot be empty")
        return trimmed


class EntryResponse(BaseModel):
    """One stored entry, as the API hands it back."""

    id: int
    message: str
    mood: str
    sentiment: Sentiment
    timestamp: str


class EntryCreated(BaseModel):
    """Answer to a successful POST /journal."""

    message: str
    entry: EntryResponse


class JournalCleared(BaseModel):
    """Answer to a successful DELETE /journal."""

    message: str
    removed: int
