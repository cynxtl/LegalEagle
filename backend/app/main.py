"""
FastAPI application entry point.

Initializes real InLegalBERT embedder, FAISS retriever, and local LLM generator
on startup via lifespan context manager.
Enforces real model inference without silent fallbacks.
Supports SQLite database persistence for threads, messages, documents, and sources.
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from backend.app.core.config import (
    settings,
    validate_model_files,
    format_validation_report,
)
from backend.app.db.database import Base, engine
from backend.app.services.rag.embedder import InLegalBERTEmbeddings
from backend.app.services.rag.retriever import FAISSRetriever
from backend.app.services.llm.generator import LLMGenerator
from backend.app.services.rag.pipeline import RAGPipeline

from backend.app.routes import chat, upload, health, threads, documents, sources

# ── Logging ───────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("legaleagle")

# ── Global service instances ──────────────────────────────────────────
# Populated during lifespan startup, accessed by route handlers.

_embedder: Optional[InLegalBERTEmbeddings] = None
_retriever: Optional[FAISSRetriever] = None
_generator: Optional[LLMGenerator] = None
_pipeline: Optional[RAGPipeline] = None


def get_embedder() -> Optional[InLegalBERTEmbeddings]:
    return _embedder


def get_retriever() -> Optional[FAISSRetriever]:
    return _retriever


def get_generator() -> Optional[LLMGenerator]:
    return _generator


def get_pipeline() -> Optional[RAGPipeline]:
    return _pipeline


# ── Lifespan ──────────────────────────────────────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle.

    On startup:
      1. Initialize SQLite database tables
      2. Validate model files
      3. Load real InLegalBERT embedding model
      4. Load real FAISS vector index
      5. Load real local LLM generator
      6. Assemble RAG pipeline

    On shutdown:
      - Release model references
    """
    global _embedder, _retriever, _generator, _pipeline

    logger.info("=" * 60)
    logger.info("LegalEagle FastAPI Backend — Starting up")
    logger.info("=" * 60)
    logger.info("Project root : %s", settings.project_root)

    # ── Step 1: Initialize Database Tables ────────────────────────
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ SQLite database tables verified")
    except Exception as exc:
        logger.error("✗ Failed to initialize database tables: %s", exc)

    # ── Step 2: Validate model files ──────────────────────────────
    validation_errors = validate_model_files(settings)
    if validation_errors:
        report = format_validation_report(validation_errors)
        logger.error("\n%s", report)
    else:
        logger.info("✓ All required model files verified on disk")

    # ── Step 3: Load embedding model ──────────────────────────────
    try:
        _embedder = InLegalBERTEmbeddings(demo_mode=False)
        logger.info("✓ InLegalBERT embedder ready (768 dimensions)")
    except Exception as exc:
        logger.error("✗ InLegalBERT embedder failed: %s", exc)

    # ── Step 4: Load FAISS index ──────────────────────────────────
    if _embedder is not None:
        try:
            _retriever = FAISSRetriever(_embedder)
            loaded = _retriever.load_index()
            if loaded:
                doc_count = _retriever.vector_store.index.ntotal if _retriever.vector_store else 0
                logger.info("✓ FAISS vector index ready (%d vectors loaded)", doc_count)
            else:
                logger.warning("⚠ FAISS index not loaded (retrieval will be empty)")
        except Exception as exc:
            logger.error("✗ FAISS retriever failed: %s", exc)

    # ── Step 5: Load LLM ─────────────────────────────────────────
    try:
        _generator = LLMGenerator(demo_mode=False)
        logger.info("✓ LLM generator ready (CTransformers)")
    except Exception as exc:
        logger.error("✗ LLM generator failed: %s", exc)

    # ── Step 6: Create RAG pipeline ───────────────────────────────
    if _retriever is not None and _generator is not None:
        try:
            _pipeline = RAGPipeline(retriever=_retriever, generator=_generator)
            logger.info("✓ RAG pipeline assembled with real AI models")
        except Exception as exc:
            logger.error("✗ RAG pipeline failed: %s", exc)
    else:
        logger.warning("⚠ RAG pipeline not assembled — missing components")

    logger.info("=" * 60)
    logger.info("LegalEagle backend ready at http://%s:%d", settings.host, settings.port)
    logger.info("API docs at http://%s:%d/docs", settings.host, settings.port)
    logger.info("=" * 60)

    yield  # ← Application runs here

    # ── Shutdown ──────────────────────────────────────────────────
    logger.info("Shutting down LegalEagle backend…")
    _embedder = None
    _retriever = None
    _generator = None
    _pipeline = None


# ── FastAPI App ───────────────────────────────────────────────────────

app = FastAPI(
    title="LegalEagle API",
    description=(
        "AI-powered Indian legal research assistant with RAG-based "
        "retrieval and local LLM generation. Returns answers with "
        "verifiable source citations."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────

app.include_router(chat.router)
app.include_router(upload.router)
app.include_router(health.router)
app.include_router(threads.router)
app.include_router(documents.router)
app.include_router(sources.router)


@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


# ── CLI Entry Point ───────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info",
    )
