# Secret Journal

A journal you can write to from the terminal or over HTTP. Built across the
Python & AI upskilling series.

- **Day 1** — a CLI that stores entries in a CSV file.
- **Day 2** — the same logic served through a FastAPI app, with a small HTML page in front of it.

---

## Setup

```bash
git clone <repo-url>
cd python-ai-upskill-september-26-treesa

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

## Running it

**API**

```bash
uvicorn src.api.main:app --reload
```

- API root: <http://localhost:8000/>
- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

**Frontend**

Open `frontend.html` in a browser while the server is running. It writes through
`POST /journal` and lists entries through `GET /journal`.

**CLI**

```bash
python -m src.cli.journal_cli
```

Run it as a module, not as `python src/cli/journal_cli.py` — the `src.` imports
need the project root on the path.

---

## API reference

### `GET /`

Health check.

```json
{ "message": "Journal API is running 🚀" }
```

### `GET /journal`

Returns every saved entry, oldest first.

| Query parameter | Type | Required | Notes |
| --- | --- | --- | --- |
| `sentiment_filter` | `positive` \| `negative` \| `neutral` | no | Returns only entries with this sentiment. Anything else is a 422. |

```bash
curl "http://localhost:8000/journal?sentiment_filter=positive"
```

```json
[
  {
    "id": 2,
    "message": "Today I learned FastAPI. It feels great!",
    "mood": ":)",
    "sentiment": "positive",
    "timestamp": "2026-09-23 13:49"
  }
]
```

### `POST /journal`

Appends an entry to `data/journal.csv` and returns it with the id it was given.

**Request**

```json
{
  "entry": "Today I learned FastAPI. It feels great!",
  "sentiment": "positive"
}
```

`entry` is required; 1–500 characters, and an entry of only whitespace is
rejected. `sentiment` is optional and defaults to `neutral`.

**Response — 201 Created**

```json
{
  "message": "Saved entry #2",
  "entry": {
    "id": 2,
    "message": "Today I learned FastAPI. It feels great!",
    "mood": ":)",
    "sentiment": "positive",
    "timestamp": "2026-09-23 13:49"
  }
}
```

**Response — 422 Unprocessable Entity**

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "entry"],
      "msg": "String should have at least 1 character"
    }
  ]
}
```

### `DELETE /journal`

Empties the journal. Numbering restarts from 1 afterwards. Not part of the Day 2
brief — added so the page has a working "Clear all" button.

```bash
curl -X DELETE http://localhost:8000/journal
```

```json
{ "message": "Cleared 3 entries", "removed": 3 }
```

---

## Project structure

```
src/
├── cli/
│   └── journal_cli.py        menu-driven terminal journal (Day 1)
├── api/
│   ├── main.py               FastAPI app, CORS, router wiring
│   ├── routers/
│   │   └── journal_routes.py GET and POST /journal
│   ├── models/
│   │   └── journal_model.py  Pydantic request/response models
│   └── utils/
│       └── file_handler.py   CSV read/append, shared by CLI and API
└── core/
    └── config.py             paths, mood/sentiment maps, limits

data/journal.csv              the entries themselves
frontend.html                 minimal browser client
```

The CLI and the API both go through `file_handler.py`, so they read and write
the same file and neither owns the storage rules.

### Moods and sentiments

The CSV keeps the Day 1 ASCII face. The API speaks in sentiments and translates
at the edge:

| Sentiment | CLI mood | Stored as |
| --- | --- | --- |
| positive | happy | `:)` |
| negative | sad | `:(` |
| neutral | neutral | `:\|` |

---

## Code style

```bash
black src/
isort src/
flake8
```

`pyproject.toml` holds the black and isort settings (isort uses the black
profile, so the two do not fight); `.flake8` matches black's 88-character line
length.

---

## Day 2 learnings

- **A route is a normal function with a decorator.** `@router.get("")` and a type-hinted
  signature is the whole contract — FastAPI reads the hints and generates both the
  validation and the `/docs` page from them.
- **Pydantic validates before the handler runs.** `Field(min_length=1, max_length=500)`
  and a `@field_validator` replace the `while True` re-prompt loops the CLI needed, and a
  bad body never reaches the function body.
- **`Literal` is free validation.** Typing the filter as
  `Literal["positive", "negative", "neutral"]` means an unknown value is a 422 with a
  useful message, without a single `if`.
- **`response_model` is a filter, not just documentation.** It drops anything the model
  does not declare, which is what stops internal fields leaking later.
- **CORS is a browser rule, not a server one.** `curl` never needed it; the browser did.
  A page opened from disk sends `Origin: null`, and `allow_credentials=True` cannot be
  combined with `allow_origins=["*"]`.
- **Routers keep `main.py` small.** `APIRouter(prefix="/journal")` means the path lives in
  one place, and `main.py` only wires things together.
- **Separating storage from the interface paid off immediately.** Day 1's functions moved
  into `file_handler.py` untouched, and the API was able to reuse them as-is.
- **The browser caches GET requests.** A working endpoint can still look broken from a
  page: repeated `fetch` calls to the same URL can be answered from cache, so the list
  goes stale after a write. `fetch(url, { cache: "no-store" })` fixes it.
