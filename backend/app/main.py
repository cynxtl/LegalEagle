"""
FastAPI application entry point.

Initializes models on startup via lifespan context manager.
Validates model files at startup with clear error messages.
Supports demo mode for development without model weights.
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
from backend.app.services.rag.embedder import InLegalBERTEmbeddings
from backend.app.services.rag.retriever import FAISSRetriever
from backend.app.services.rag.pipeline import RAGPipeline
from backend.app.services.llm.generator import LLMGenerator

from backend.app.routes import chat, upload, health

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
      1. Validate model files
      2. Load embedding model (or activate demo mode)
      3. Load FAISS index
      4. Load LLM
      5. Create RAG pipeline

    On shutdown:
      - Release model references
    """
    global _embedder, _retriever, _generator, _pipeline

    logger.info("=" * 60)
    logger.info("LegalEagle FastAPI Backend — Starting up")
    logger.info("=" * 60)
    logger.info("Project root : %s", settings.project_root)
    logger.info("Demo mode    : %s", settings.demo_mode)

    # ── Step 1: Validate model files ──────────────────────────────
    validation_errors = validate_model_files(settings)
    if validation_errors:
        report = format_validation_report(validation_errors)
        logger.warning("\n%s", report)

        if not settings.demo_mode:
            logger.warning(
                "Models are missing. Starting in degraded mode. "
                "Set LEGALEAGLE_DEMO_MODE=true for mock responses."
            )

    use_demo = settings.demo_mode or bool(validation_errors)

    # ── Step 2: Load embedding model ──────────────────────────────
    try:
        _embedder = InLegalBERTEmbeddings(demo_mode=use_demo)
        logger.info("✓ Embedder ready (demo=%s)", use_demo)
    except Exception as exc:
        logger.error("✗ Embedder failed: %s", exc)
        if not use_demo:
            logger.info("Falling back to demo mode for embedder")
            _embedder = InLegalBERTEmbeddings(demo_mode=True)

    # ── Step 3: Load FAISS index ──────────────────────────────────
    if _embedder is not None:
        try:
            _retriever = FAISSRetriever(_embedder)
            loaded = _retriever.load_index()
            if loaded:
                logger.info("✓ FAISS index ready")
            else:
                logger.warning("⚠ FAISS index not loaded (retrieval will be empty)")
        except Exception as exc:
            logger.error("✗ FAISS retriever failed: %s", exc)

    # ── Step 4: Load LLM ─────────────────────────────────────────
    try:
        _generator = LLMGenerator(demo_mode=use_demo)
        logger.info("✓ LLM generator ready (demo=%s)", use_demo)
    except Exception as exc:
        logger.error("✗ LLM generator failed: %s", exc)
        if not use_demo:
            logger.info("Falling back to demo mode for LLM")
            _generator = LLMGenerator(demo_mode=True)

    # ── Step 5: Create RAG pipeline ───────────────────────────────
    if _retriever is not None and _generator is not None:
        _pipeline = RAGPipeline(retriever=_retriever, generator=_generator)
        logger.info("✓ RAG pipeline assembled")
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
        "retrieval and Mistral-7B generation. Returns answers with "
        "verifiable source citations."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow all origins for local development
# TODO: Restrict to known frontend domains in production
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
