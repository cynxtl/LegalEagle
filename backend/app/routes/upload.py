"""
Document upload API route with SQLite persistence.

POST /upload — accepts PDF/DOCX files, extracts text,
chunks it, adds to the FAISS vector store, and saves document record to SQLite.
"""

import logging
import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.db.models import DocumentDB
from backend.app.models.schemas import UploadResponse, ErrorResponse
from backend.app.services.rag.loader import (
    save_upload_to_temp,
    extract_text,
    chunk_text,
    count_pages,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["upload"])

# Supported MIME types
SUPPORTED_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB


@router.post(
    "/upload",
    response_model=UploadResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid file"},
        503: {"model": ErrorResponse, "description": "Backend models not ready"},
    },
    summary="Upload a legal document",
    description=(
        "Upload a PDF, DOCX, or TXT file. The document is processed, "
        "chunked, added to the FAISS vector store for retrieval, and persisted in SQLite."
    ),
)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadResponse:
    """Process and index an uploaded document, saving metadata to DB."""
    from backend.app.main import get_retriever

    retriever = get_retriever()
    if retriever is None or not retriever.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Vector store is not initialized. Check /health for status.",
        )

    # Validate file type
    if file.content_type and file.content_type not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type: {file.content_type}. "
                f"Accepted: PDF, DOCX, TXT."
            ),
        )

    # Validate filename extension as fallback
    filename = file.filename or "document"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in (".pdf", ".docx", ".doc", ".txt"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension: '{ext}'. Accepted: .pdf, .docx, .doc, .txt",
        )

    # Read file content
    try:
        content = await file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded file: {exc}",
        )

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size ({len(content) / 1024 / 1024:.1f} MB) exceeds 25 MB limit.",
        )

    # Save to temp and process
    try:
        temp_path = save_upload_to_temp(content, filename)
        document_text = extract_text(temp_path, filename)

        if not document_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract any text from the uploaded document.",
            )

        # Chunk and add to vector store
        chunks = chunk_text(document_text)
        if not chunks:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document produced no usable text chunks.",
            )

        success = retriever.add_documents(chunks)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to add document chunks to the vector store.",
            )

        # Get page count
        pages = count_pages(temp_path, filename)

        # Clean up temp file
        try:
            os.remove(temp_path)
            os.rmdir(os.path.dirname(temp_path))
        except OSError:
            pass

        doc_id = f"doc-{uuid.uuid4().hex[:12]}"
        file_size = f"{len(content) / 1024 / 1024:.1f} MB" if len(content) > 1024 * 1024 else f"{len(content) / 1024:.0f} KB"

        # Determine category based on filename/content
        category = "General"
        fn_lower = filename.lower()
        if "lease" in fn_lower or "rent" in fn_lower or "property" in fn_lower:
            category = "Property"
        elif "contract" in fn_lower or "agreement" in fn_lower or "deed" in fn_lower:
            category = "Contract"
        elif "fir" in fn_lower or "police" in fn_lower or "ipc" in fn_lower or "criminal" in fn_lower:
            category = "Criminal Law"
        elif "employ" in fn_lower or "labor" in fn_lower:
            category = "Employment"

        # Persist Document to SQLite
        doc_db = DocumentDB(
            id=doc_id,
            name=filename,
            size=file_size,
            pages=pages,
            status="indexed",
            chunk_count=len(chunks),
            category=category,
            uploaded_at=datetime.utcnow(),
        )
        db.add(doc_db)
        db.commit()
        db.refresh(doc_db)

        return UploadResponse(
            id=doc_id,
            name=filename,
            size=file_size,
            pages=pages,
            status="indexed",
            chunk_count=len(chunks),
            category=category,
            uploaded_at=doc_db.uploaded_at.strftime("%b %d, %Y %I:%M %p"),
            message=f"Document '{filename}' processed: {len(chunks)} chunks indexed.",
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Upload processing failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document processing failed: {str(exc)}",
        )
