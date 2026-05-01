"""
Health check API route.

GET /health — reports model load status, FAISS index status,
demo mode flag, and lists any missing model files.
"""

import logging

from fastapi import APIRouter

from backend.app.core.config import settings, validate_model_files
from backend.app.models.schemas import HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Check backend health",
    description=(
        "Returns the status of the backend service including model load "
        "state, FAISS index availability, and any missing model files."
    ),
)
async def health_check() -> HealthResponse:
    """Report backend health and readiness."""
    from backend.app.main import get_embedder, get_retriever, get_generator

    embedder = get_embedder()
    retriever = get_retriever()
    generator = get_generator()

    models_loaded = (
        (embedder is not None and embedder.is_loaded)
        and (generator is not None and generator.is_loaded)
    )
    faiss_loaded = retriever is not None and retriever.is_loaded

    # Check for missing model files
    validation_errors = validate_model_files(settings)
    missing = [err.name for err in validation_errors]

    return HealthResponse(
        status="ok" if models_loaded and faiss_loaded else "degraded",
        models_loaded=models_loaded,
        faiss_index_loaded=faiss_loaded,
        demo_mode=settings.demo_mode,
        version="2.0.0",
        missing_models=missing,
    )
