"""
RAG pipeline orchestrator.

Coordinates: query → retrieve → generate → format response.
Derived from the chat handler logic in app.py (lines 836-854).
"""

import logging
import uuid
from typing import Optional

from backend.app.core.config import settings
from backend.app.models.schemas import (
    ChatResponse,
    SourceResponse,
)
from backend.app.services.rag.retriever import FAISSRetriever
from backend.app.services.llm.generator import LLMGenerator

logger = logging.getLogger(__name__)


class RAGPipeline:
    """End-to-end RAG pipeline for Indian legal Q&A.

    Orchestrates retrieval, context assembly, generation, and
    response formatting in a single ``process_query()`` call.
    """

    def __init__(self, retriever: FAISSRetriever, generator: LLMGenerator):
        self.retriever = retriever
        self.generator = generator

    def process_query(
        self,
        message: str,
        chat_history: Optional[list[dict]] = None,
        category: Optional[str] = None,
    ) -> ChatResponse:
        """Process a user query through the full RAG pipeline.

        Args:
            message: The user's legal question.
            chat_history: Previous conversation messages (role + content dicts).
            category: Optional legal category filter.

        Returns:
            ChatResponse with answer, sources, and confidence.
        """
        logger.info("Processing query: %s", message[:100])

        # Step 1: Retrieve relevant documents
        retrieved = self.retriever.retrieve(message)
        logger.info("Retrieved %d documents", len(retrieved))

        # Step 2: Build context from retrieved chunks
        context = self._build_context(retrieved)

        # Step 3: Format chat history
        formatted_history = self._format_chat_history(chat_history)

        # Step 4: Generate answer
        answer = self.generator.generate(
            context=context,
            question=message,
            chat_history=formatted_history,
        )
        logger.info("Generated answer (%d chars)", len(answer))

        # Step 5: Build source responses
        sources = self._build_sources(retrieved)

        # Step 6: Determine confidence
        confidence = self._compute_confidence(retrieved, answer)

        return ChatResponse(
            answer=answer,
            sources=sources,
            confidence=confidence,
        )

    def _build_context(self, retrieved: list[dict]) -> str:
        """Assemble retrieved documents into a context string."""
        if not retrieved:
            return "No relevant documents found in the knowledge base."

        context_parts = []
        for doc in retrieved:
            context_parts.append(doc["content"])
        return "\n\n".join(context_parts)

    def _format_chat_history(
        self, chat_history: Optional[list[dict]]
    ) -> str:
        """Format chat history for the LLM prompt.

        Uses only the last 3 exchanges (6 messages) to limit context size.
        Truncates individual messages to 200 characters.
        """
        if not chat_history:
            return "No previous conversation."

        # Limit to last 6 messages (3 exchanges)
        limited = chat_history[-6:] if len(chat_history) > 6 else chat_history

        parts = []
        for entry in limited:
            role = entry.get("role", "user")
            content = entry.get("content", "")

            # Truncate long messages
            if len(content) > 200:
                content = content[:197] + "..."

            label = "Human" if role == "user" else "Assistant"
            parts.append(f"{label}: {content}")

        return "\n".join(parts)

    def _build_sources(self, retrieved: list[dict]) -> list[SourceResponse]:
        """Convert retrieved documents into SourceResponse objects.

        Uses fallback metadata since FAISS only stores raw text chunks.
        """
        sources = []
        for i, doc in enumerate(retrieved):
            content = doc["content"]

            # Try to extract any metadata hints from the content
            title, doc_type = self._infer_metadata(content)

            sources.append(
                SourceResponse(
                    id=f"src-{uuid.uuid4().hex[:8]}",
                    title=title,
                    citation=None,
                    jurisdiction=None,
                    year=None,
                    excerpt=content[:500] if len(content) > 500 else content,
                    url=None,
                    type=doc_type,
                )
            )

        return sources

    def _infer_metadata(self, content: str) -> tuple[str, str]:
        """Best-effort metadata extraction from raw text.

        Returns (title, type) tuple.
        """
        content_lower = content.lower()

        # Q&A pairs
        if content.startswith("Q:") and "A:" in content:
            q_end = content.find("\n")
            title = content[2:q_end].strip() if q_end > 0 else content[2:80].strip()
            return f"Q&A: {title[:80]}", "commentary"

        # Section references
        if "section" in content_lower and ("ipc" in content_lower or "crpc" in content_lower):
            return "Indian Penal Code Reference", "statute"

        # Article references
        if "article" in content_lower and "constitution" in content_lower:
            return "Constitutional Provision", "statute"

        # Case-like content
        if " v. " in content or " vs " in content_lower:
            return "Case Reference", "case"

        return "Retrieved Document", "retrieved_chunk"

    def _compute_confidence(
        self, retrieved: list[dict], answer: str
    ) -> str:
        """Heuristic confidence scoring based on retrieval quality.

        Uses FAISS similarity scores (lower = more similar for L2 distance).
        """
        if not retrieved:
            return "low"

        scores = [doc["score"] for doc in retrieved]
        avg_score = sum(scores) / len(scores)

        # FAISS L2 distance: lower is better
        # These thresholds are empirical and may need tuning
        if avg_score < 50:
            return "high"
        elif avg_score < 150:
            return "medium"
        else:
            return "low"
