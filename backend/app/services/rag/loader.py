"""
Document ingestion and chunking.

Extracted from app.py read_pdf(), read_docx(), process_document(),
and create_vector_store() (lines 409-486).
Handles PDF and DOCX uploads, text extraction, and chunking.
"""

import logging
import os
import tempfile
from pathlib import Path

import PyPDF2
import docx
from langchain.text_splitter import RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)


def read_pdf(file_path: str) -> str:
    """Extract text from a PDF file.

    Args:
        file_path: Absolute path to the PDF file.

    Returns:
        Extracted text as a single string.
    """
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            pages_text = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pages_text.append(text)
            full_text = "\n".join(pages_text)
            logger.info(
                "Extracted %d characters from %d pages of %s",
                len(full_text),
                len(reader.pages),
                file_path,
            )
            return full_text
    except Exception as exc:
        logger.error("Failed to read PDF '%s': %s", file_path, exc)
        return ""


def read_docx(file_path: str) -> str:
    """Extract text from a DOCX file.

    Args:
        file_path: Absolute path to the DOCX file.

    Returns:
        Extracted text as a single string.
    """
    try:
        document = docx.Document(file_path)
        paragraphs = [para.text for para in document.paragraphs if para.text.strip()]
        full_text = "\n".join(paragraphs)
        logger.info(
            "Extracted %d characters from %d paragraphs of %s",
            len(full_text),
            len(paragraphs),
            file_path,
        )
        return full_text
    except Exception as exc:
        logger.error("Failed to read DOCX '%s': %s", file_path, exc)
        return ""


def extract_text(file_path: str, filename: str) -> str:
    """Dispatch text extraction based on file extension.

    Args:
        file_path: Absolute path to the saved file.
        filename: Original filename (used for extension detection).

    Returns:
        Extracted text, or empty string on failure.

    Raises:
        ValueError: If the file type is not supported.
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return read_docx(file_path)
    elif ext == ".txt":
        try:
            return Path(file_path).read_text(encoding="utf-8")
        except Exception as exc:
            logger.error("Failed to read TXT '%s': %s", file_path, exc)
            return ""
    else:
        raise ValueError(
            f"Unsupported file format: '{ext}'. "
            f"Accepted formats: .pdf, .docx, .doc, .txt"
        )


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 100,
) -> list[str]:
    """Split text into chunks using recursive character splitting.

    Args:
        text: Full document text.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        List of text chunks.
    """
    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = splitter.split_text(text)
    logger.info(
        "Split text (%d chars) into %d chunks (size=%d, overlap=%d)",
        len(text),
        len(chunks),
        chunk_size,
        chunk_overlap,
    )
    return chunks


def save_upload_to_temp(file_bytes: bytes, filename: str) -> str:
    """Save uploaded file bytes to a temporary directory.

    Args:
        file_bytes: Raw file content.
        filename: Original filename.

    Returns:
        Absolute path to the saved temporary file.
    """
    temp_dir = tempfile.mkdtemp(prefix="legaleagle_upload_")
    temp_path = os.path.join(temp_dir, filename)

    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    logger.info("Saved upload '%s' to %s (%d bytes)", filename, temp_path, len(file_bytes))
    return temp_path


def count_pages(file_path: str, filename: str) -> int:
    """Estimate page count for the uploaded document.

    Args:
        file_path: Path to the file.
        filename: Original filename.

    Returns:
        Page count (exact for PDF, estimated for others).
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        try:
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                return len(reader.pages)
        except Exception:
            return 0

    # For non-PDF, estimate: ~3000 chars per page
    try:
        size = os.path.getsize(file_path)
        return max(1, size // 3000)
    except Exception:
        return 1
