"""
Sources & Citations API routes.

Provides endpoints for:
- GET /api/v1/sources (List all saved/retrieved citations)
- POST /api/v1/sources/{id}/star (Toggle star on citation)
- DELETE /api/v1/sources/{id} (Delete citation)
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import SourceDB
from backend.app.models.schemas import SourceResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sources", tags=["sources"])


@router.get(
    "",
    response_model=List[SourceResponse],
    summary="List all retrieved sources",
    description="Returns all sources grounded in past consultations.",
)
def list_sources(
    doc_type: Optional[str] = Query(None, description="Filter by type: case, statute, regulation, commentary"),
    starred_only: bool = Query(False, description="Filter only starred sources"),
    db: Session = Depends(get_db),
):
    query = db.query(SourceDB)
    if doc_type:
        query = query.filter(SourceDB.doc_type == doc_type)
    if starred_only:
        query = query.filter(SourceDB.is_starred == True)

    sources = query.order_by(SourceDB.created_at.desc()).all()
    return [
        SourceResponse(
            id=s.id,
            thread_id=s.thread_id,
            title=s.title,
            citation=s.citation,
            jurisdiction=s.jurisdiction,
            year=s.year,
            excerpt=s.excerpt,
            url=s.url,
            type=s.doc_type,
            score=s.score,
            is_starred=s.is_starred,
            created_at=s.created_at.isoformat() if s.created_at else None,
        )
        for s in sources
    ]


@router.post(
    "/{source_id}/star",
    response_model=SourceResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Toggle star on a citation",
)
def toggle_star_source(source_id: str, db: Session = Depends(get_db)):
    source = db.query(SourceDB).filter(SourceDB.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{source_id}' not found")
    source.is_starred = not source.is_starred
    db.commit()
    db.refresh(source)
    return SourceResponse(
        id=source.id,
        thread_id=source.thread_id,
        title=source.title,
        citation=source.citation,
        jurisdiction=source.jurisdiction,
        year=source.year,
        excerpt=source.excerpt,
        url=source.url,
        type=source.doc_type,
        score=source.score,
        is_starred=source.is_starred,
        created_at=source.created_at.isoformat() if source.created_at else None,
    )


@router.delete(
    "/{source_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    summary="Delete a source from library",
)
def delete_source(source_id: str, db: Session = Depends(get_db)):
    source = db.query(SourceDB).filter(SourceDB.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail=f"Source '{source_id}' not found")
    db.delete(source)
    db.commit()
    return None
