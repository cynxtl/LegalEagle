"""
Pydantic request / response schemas.

Aligned with the frontend TypeScript types in frontend/lib/legal-data.ts
so that the JSON contract matches exactly what the Next.js client expects.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


# ── Request Models ────────────────────────────────────────────────────


class ChatRequest(BaseModel):
    """Body for ``POST /chat``."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The user's legal query.",
    )
    category: Optional[str] = Field(
        default=None,
        description="Optional legal category filter (e.g. 'Criminal Law', 'Property').",
    )
    chat_history: Optional[list[ChatHistoryEntry]] = Field(
        default=None,
        description=(
            "Previous messages for conversational context. "
            "The frontend is responsible for sending these."
        ),
    )


class ChatHistoryEntry(BaseModel):
    """A single message in the conversation history sent by the frontend."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text")


# Rebuild ChatRequest so it can reference ChatHistoryEntry
ChatRequest.model_rebuild()


# ── Response Models ───────────────────────────────────────────────────


class SourceResponse(BaseModel):
    """A single retrieved source document.

    Matches the frontend ``Source`` TypeScript type.
    Fields that cannot be determined from raw FAISS chunks are nullable
    so the frontend can render gracefully.
    """

    id: str
    title: str = "Retrieved Document"
    citation: Optional[str] = None
    jurisdiction: Optional[str] = None
    year: Optional[int] = None
    excerpt: str = ""
    url: Optional[str] = None
    type: str = Field(
        default="retrieved_chunk",
        description="One of: case, statute, regulation, commentary, retrieved_chunk",
    )


class ChatResponse(BaseModel):
    """Response body for ``POST /chat``."""

    answer: str = Field(..., description="Generated legal response text.")
    sources: list[SourceResponse] = Field(
        default_factory=list,
        description="Retrieved source documents used to ground the answer.",
    )
    confidence: str = Field(
        default="medium",
        description="Answer confidence level: 'high', 'medium', or 'low'.",
    )


class UploadResponse(BaseModel):
    """Response body for ``POST /upload``."""

    id: str
    name: str
    size: str
    pages: int
    status: str = Field(
        default="processing",
        description="One of: indexed, processing, failed",
    )
    message: str = "Document uploaded and processing started."


class HealthResponse(BaseModel):
    """Response body for ``GET /health``."""

    status: str = "ok"
    models_loaded: bool = False
    faiss_index_loaded: bool = False
    demo_mode: bool = False
    version: str = "2.0.0"
    missing_models: list[str] = Field(
        default_factory=list,
        description="List of model files that are missing (empty when everything is present).",
    )


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    detail: str
    error_code: Optional[str] = None
