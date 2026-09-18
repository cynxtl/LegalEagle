"""
Pydantic request / response schemas.

Aligned with the frontend TypeScript types in frontend/lib/legal-data.ts
so that the JSON contract matches exactly what the Next.js client expects.
"""

from __future__ import annotations

from typing import Optional, List
from pydantic import BaseModel, Field


# ── Chat Request Models ───────────────────────────────────────────────


class ChatHistoryEntry(BaseModel):
    """A single message in the conversation history sent by the frontend."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str = Field(..., description="Message text")


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
    thread_id: Optional[str] = Field(
        default=None,
        description="Optional thread ID. If omitted, a new thread is created.",
    )
    chat_history: Optional[list[ChatHistoryEntry]] = Field(
        default=None,
        description=(
            "Previous messages for conversational context. "
            "The frontend can pass these or they can be loaded from DB."
        ),
    )


# ── Source Models ─────────────────────────────────────────────────────


class SourceResponse(BaseModel):
    """A single retrieved source document."""

    id: str
    thread_id: Optional[str] = None
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
    score: Optional[float] = None
    is_starred: bool = False
    created_at: Optional[str] = None


# ── Chat Response Model ───────────────────────────────────────────────


class ChatResponse(BaseModel):
    """Response body for ``POST /chat``."""

    answer: str = Field(..., description="Generated legal response text.")
    sources: list[SourceResponse] = Field(
        default_factory=list,
        description="Retrieved source documents used to ground the answer.",
    )
    thread_id: Optional[str] = Field(
        default=None,
        description="Thread ID associated with this chat session.",
    )
    confidence: str = Field(
        default="medium",
        description="Answer confidence level: 'high', 'medium', or 'low'.",
    )


# ── Thread Models ─────────────────────────────────────────────────────


class ThreadCreate(BaseModel):
    """Payload to create a new thread."""
    title: Optional[str] = "New Consultation"
    category: Optional[str] = "General"


class MessageResponse(BaseModel):
    """A single message response."""
    id: str
    thread_id: str
    role: str
    content: str
    category: Optional[str] = None
    confidence: Optional[str] = "medium"
    sources: list[SourceResponse] = Field(default_factory=list)
    created_at: str


class ThreadResponse(BaseModel):
    """Thread summary for sidebar."""
    id: str
    title: str
    category: str
    created_at: str
    updated_at: str
    message_count: int = 0
    preview: Optional[str] = ""


class ThreadDetailResponse(ThreadResponse):
    """Thread detail including all messages."""
    messages: list[MessageResponse] = Field(default_factory=list)


# ── Document Models ───────────────────────────────────────────────────


class UploadResponse(BaseModel):
    """Response body for ``POST /upload``."""

    id: str
    name: str
    size: str
    pages: int
    status: str = Field(
        default="indexed",
        description="One of: indexed, processing, failed",
    )
    chunk_count: int = 0
    category: str = "Contract"
    uploaded_at: Optional[str] = None
    message: str = "Document uploaded and processed successfully."


class DocumentResponse(BaseModel):
    """Document record response."""

    id: str
    name: str
    size: str
    pages: int
    status: str
    chunk_count: int
    category: str
    uploaded_at: str


# ── System Models ─────────────────────────────────────────────────────


class HealthResponse(BaseModel):
    """Response body for ``GET /health``."""

    status: str = "ok"
    models_loaded: bool = False
    faiss_index_loaded: bool = False
    demo_mode: bool = False
    version: str = "2.0.0"
    missing_models: list[str] = Field(
        default_factory=list,
        description="List of model files that are missing.",
    )


class ErrorResponse(BaseModel):
    """Standard error envelope."""

    detail: str
    error_code: Optional[str] = None
