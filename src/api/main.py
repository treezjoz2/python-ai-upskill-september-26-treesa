"""FastAPI application for the Secret Journal.

Run it with:  uvicorn src.api.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import journal_routes
from src.core.config import ALLOWED_ORIGINS

app = FastAPI(
    title="TJ's Journal API",
    description="Day 2 of the upskilling series: the journal CLI, served over HTTP.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(journal_routes.router)


@app.get("/", summary="Health check")
def read_root() -> dict:
    """Confirm the API is up."""
    return {"message": "Journal API is running 🚀"}
