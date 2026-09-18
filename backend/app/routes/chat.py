"""
Chat API route with SQLite persistence.

POST /chat — accepts a legal query, runs the RAG pipeline,
saves user & assistant messages to SQLite, records sources,
and returns structured response with answer, sources, thread_id, and confidence.
"""

import json
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import ThreadDB, MessageDB, SourceDB
from backend.app.models.schemas import ChatRequest, ChatResponse, SourceResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    responses={
        503: {"model": ErrorResponse, "description": "Backend models not ready"},
    },
    summary="Ask a legal question",
    description=(
        "Send a legal query and receive an AI-generated answer grounded in "
        "retrieved Indian legal documents, with source citations and a "
        "confidence score. Persists conversation to SQLite."
    ),
)
async def chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """Process a legal question through the RAG pipeline and persist to DB."""
    from backend.app.main import get_pipeline

    pipeline = get_pipeline()
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "The RAG pipeline is not initialized. "
                "Check /health for model and index status."
            ),
        )

    # 1. Manage Thread: find existing or create new
    thread = None
    if request.thread_id:
        thread = db.query(ThreadDB).filter(ThreadDB.id == request.thread_id).first()

    if thread is None:
        thread_title = request.message[:50].strip()
        if len(request.message) > 50:
            thread_title += "..."
        thread = ThreadDB(
            id=request.thread_id or f"t-{uuid.uuid4().hex[:8]}",
            title=thread_title,
            category=request.category or "General",
        )
        db.add(thread)
        db.commit()
        db.refresh(thread)
    else:
        # Update thread timestamp
        thread.updated_at = datetime.utcnow()
        if request.category:
            thread.category = request.category
        db.commit()

    # 2. Persist User Message
    user_msg = MessageDB(
        id=f"msg-{uuid.uuid4().hex[:10]}",
        thread_id=thread.id,
        role="user",
        content=request.message,
        category=request.category,
        confidence=None,
        sources_json="[]",
    )
    db.add(user_msg)
    db.commit()

    # 3. Assemble chat history from request or DB
    history = None
    if request.chat_history:
        history = [
            {"role": entry.role, "content": entry.content}
            for entry in request.chat_history
        ]
    else:
        # Load previous messages from thread
        past_msgs = (
            db.query(MessageDB)
            .filter(MessageDB.thread_id == thread.id, MessageDB.id != user_msg.id)
            .order_by(MessageDB.created_at.asc())
            .all()
        )
        if past_msgs:
            history = [{"role": m.role, "content": m.content} for m in past_msgs[-6:]]

    # 4. Run RAG Pipeline
    try:
        response = pipeline.process_query(
            message=request.message,
            chat_history=history,
            category=request.category,
        )

        sources_dict_list = [s.model_dump() for s in response.sources]

        # 5. Persist Assistant Message
        assistant_msg = MessageDB(
            id=f"msg-{uuid.uuid4().hex[:10]}",
            thread_id=thread.id,
            role="assistant",
            content=response.answer,
            category=request.category,
            confidence=response.confidence,
            sources_json=json.dumps(sources_dict_list),
        )
        db.add(assistant_msg)

        # 6. Persist retrieved sources into SourceDB
        for src in response.sources:
            existing = db.query(SourceDB).filter(SourceDB.excerpt == src.excerpt).first()
            if not existing:
                src_db = SourceDB(
                    id=src.id or f"src-{uuid.uuid4().hex[:8]}",
                    thread_id=thread.id,
                    title=src.title,
                    citation=src.citation,
                    jurisdiction=src.jurisdiction,
                    year=src.year,
                    excerpt=src.excerpt,
                    url=src.url,
                    doc_type=src.type,
                    score=None,
                    is_starred=False,
                )
                db.add(src_db)

        db.commit()

        return ChatResponse(
            answer=response.answer,
            sources=response.sources,
            thread_id=thread.id,
            confidence=response.confidence,
        )

    except Exception as exc:
        logger.error("Chat processing failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(exc)}",
        )
