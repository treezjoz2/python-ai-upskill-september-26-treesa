"""Settings shared by the journal CLI and the journal API."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
CSV_FILE = DATA_DIR / "journal.csv"
CSV_COLUMNS = ["id", "message", "mood", "timestamp"]

DEFAULT_NAME = "TJ"
MAX_ENTRY_LENGTH = 500

MOOD_FACES = {
    "happy": ":)",
    "sad": ":(",
    "neutral": ":|",
}

SENTIMENT_FACES = {
    "positive": ":)",
    "negative": ":(",
    "neutral": ":|",
}

FACE_SENTIMENTS = {face: sentiment for sentiment, face in SENTIMENT_FACES.items()}

ALLOWED_ORIGINS = ["*"]
