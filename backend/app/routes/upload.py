"""
Document upload API route.

POST /upload — accepts PDF/DOCX files, extracts text,
chunks it, and adds to the FAISS vector store.
"""

import logging
import os
import uuid

from fastapi import APIRouter, File, HTTPException, UploadFile, status

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
        "chunked, and added to the FAISS vector store for retrieval."
    ),
)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    """Process and index an uploaded document."""
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

        return UploadResponse(
            id=doc_id,
            name=filename,
            size=file_size,
            pages=pages,
            status="indexed",
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
