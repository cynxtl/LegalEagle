"""
Document persistence API routes.

Provides endpoints for:
- GET /api/v1/documents (List all indexed documents)
- DELETE /api/v1/documents/{id} (Delete document from database)
"""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import DocumentDB
from backend.app.models.schemas import DocumentResponse, ErrorResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.get(
    "",
    response_model=List[DocumentResponse],
    summary="List all uploaded documents",
    description="Returns all uploaded and indexed legal documents stored in the database.",
)
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(DocumentDB).order_by(DocumentDB.uploaded_at.desc()).all()
    return [
        DocumentResponse(
            id=d.id,
            name=d.name,
            size=d.size,
            pages=d.pages,
            status=d.status,
            chunk_count=d.chunk_count,
            category=d.category,
            uploaded_at=d.uploaded_at.strftime("%b %d, %Y %I:%M %p"),
        )
        for d in docs
    ]


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
    summary="Delete a document",
)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(DocumentDB).filter(DocumentDB.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Document '{document_id}' not found")
    db.delete(doc)
    db.commit()
    logger.info("Deleted document %s from database", document_id)
    return None
