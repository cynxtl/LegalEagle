"""
Thread persistence API routes.

Provides endpoints for:
- GET /api/v1/threads (List all threads for sidebar)
- POST /api/v1/threads (Create new thread)
- GET /api/v1/threads/{id} (Get thread with full message history)
- DELETE /api/v1/threads/{id} (Delete thread)
"""

import json
import logging
from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import ThreadDB, MessageDB
from backend.app.models.schemas import (
    ThreadCreate,
    ThreadUpdate,
    ThreadResponse,
    ThreadDetailResponse,
    MessageResponse,
    SourceResponse,
    ErrorResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/threads", tags=["threads"])


@router.get(
    "",
    response_model=List[ThreadResponse],
    summary="List all chat threads",
    description="Returns all conversation threads ordered by most recently updated.",
)
def list_threads(db: Session = Depends(get_db)):
    threads = db.query(ThreadDB).order_by(ThreadDB.updated_at.desc()).all()
    results = []
    for t in threads:
        msg_count = len(t.messages)
        last_msg = t.messages[-1].content if t.messages else "New consultation..."
        preview = last_msg[:80] + "..." if len(last_msg) > 80 else last_msg
        results.append(
            ThreadResponse(
                id=t.id,
                title=t.title,
                category=t.category,
                created_at=t.created_at.isoformat(),
                updated_at=t.updated_at.isoformat(),
                message_count=msg_count,
                preview=preview,
            )
        )
    return results


@router.post(
    "",
    response_model=ThreadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new chat thread",
)
def create_thread(payload: ThreadCreate, db: Session = Depends(get_db)):
    thread = ThreadDB(
        title=payload.title or "New Consultation",
        category=payload.category or "General",
    )
    db.add(thread)
    db.commit()
    db.refresh(thread)
    return ThreadResponse(
        id=thread.id,
        title=thread.title,
        category=thread.category,
        created_at=thread.created_at.isoformat(),
        updated_at=thread.updated_at.isoformat(),
        message_count=0,
        preview="",
    )


@router.get(
    "/{thread_id}",
    response_model=ThreadDetailResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Get thread by ID with all messages",
)
def get_thread(thread_id: str, db: Session = Depends(get_db)):
    thread = db.query(ThreadDB).filter(ThreadDB.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail=f"Thread '{thread_id}' not found")

    messages_res = []
    for m in thread.messages:
        sources_list = []
        if m.sources_json:
            try:
                raw_sources = json.loads(m.sources_json)
                sources_list = [SourceResponse(**s) for s in raw_sources]
            except Exception:
                pass
        messages_res.append(
            MessageResponse(
                id=m.id,
                thread_id=m.thread_id,
                role=m.role,
                content=m.content,
                category=m.category,
                confidence=m.confidence,
                sources=sources_list,
                created_at=m.created_at.isoformat(),
            )
        )

    last_msg = thread.messages[-1].content if thread.messages else ""
    preview = last_msg[:80] + "..." if len(last_msg) > 80 else last_msg

    return ThreadDetailResponse(
        id=thread.id,
        title=thread.title,
        category=thread.category,
        created_at=thread.created_at.isoformat(),
        updated_at=thread.updated_at.isoformat(),
        message_count=len(thread.messages),
        preview=preview,
        messages=messages_res,
    )


@router.delete(
    "/{thread_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    summary="Delete a chat thread",
)
def delete_thread(thread_id: str, db: Session = Depends(get_db)):
    thread = db.query(ThreadDB).filter(ThreadDB.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail=f"Thread '{thread_id}' not found")
    db.delete(thread)
    db.commit()
    return None


@router.patch(
    "/{thread_id}",
    response_model=ThreadResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Rename or update a chat thread",
)
def update_thread(thread_id: str, payload: ThreadUpdate, db: Session = Depends(get_db)):
    thread = db.query(ThreadDB).filter(ThreadDB.id == thread_id).first()
    if not thread:
        raise HTTPException(status_code=404, detail=f"Thread '{thread_id}' not found")
    
    if payload.title is not None and payload.title.strip():
        thread.title = payload.title.strip()
    if payload.category is not None and payload.category.strip():
        thread.category = payload.category.strip()
    
    thread.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(thread)

    msg_count = len(thread.messages)
    last_msg = thread.messages[-1].content if thread.messages else "New consultation..."
    preview = last_msg[:80] + "..." if len(last_msg) > 80 else last_msg

    return ThreadResponse(
        id=thread.id,
        title=thread.title,
        category=thread.category,
        created_at=thread.created_at.isoformat(),
        updated_at=thread.updated_at.isoformat(),
        message_count=msg_count,
        preview=preview,
    )
