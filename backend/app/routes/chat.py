"""
Chat API route.

POST /chat — accepts a legal query, runs the RAG pipeline,
and returns a structured response with answer, sources, and confidence.
"""

import logging

from fastapi import APIRouter, HTTPException, status

from backend.app.models.schemas import ChatRequest, ChatResponse, ErrorResponse

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
        "confidence score."
    ),
)
async def chat(request: ChatRequest) -> ChatResponse:
    """Process a legal question through the RAG pipeline."""
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

    # Convert chat_history from Pydantic models to dicts
    history = None
    if request.chat_history:
        history = [
            {"role": entry.role, "content": entry.content}
            for entry in request.chat_history
        ]

    try:
        response = pipeline.process_query(
            message=request.message,
            chat_history=history,
            category=request.category,
        )
        return response

    except Exception as exc:
        logger.error("Chat processing failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process query: {str(exc)}",
        )
