"""
LLM generation service using Mistral-7B via CTransformers.

Extracted from app.py:
  - Model initialization (lines 188-199)
  - QA_PROMPT template (lines 627-642)
  - Response generation with retry logic (lines 728-791)

Supports demo mode returning canned responses when the GGUF
weight file is not available.
"""

import logging

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Prompt Template ──────────────────────────────────────────────────
# Preserved from app.py — Mistral [INST] format for Indian law Q&A

QA_PROMPT = """\
<s>[INST]
You are an expert assistant specializing in Indian law. Provide highly accurate, \
contextually appropriate, and well-structured answers strictly based on Indian legal \
statutes, regulations, and precedents. If you do not know the answer, say \
"I don't know." Do not hallucinate or make up information.

CONTEXT: {context}
CHAT HISTORY: {chat_history}
QUESTION: {question}

ANSWER:
- Detail the first key aspect of the law, ensuring it reflects general application.
- Provide a concise explanation of how the law is typically interpreted or applied.
- Correct a common misconception or clarify a frequently misunderstood aspect.
- Detail any exceptions to the general rule, if applicable.
- Include any additional relevant information that directly relates to the user's query.
</s>[INST]
"""

# ── Demo mode fallback response ──────────────────────────────────────

DEMO_RESPONSE = (
    "**[Demo Mode]** The LLM model files are not loaded. "
    "This is a placeholder response.\n\n"
    "In a production setup, this would contain a detailed legal analysis "
    "based on the retrieved context from the FAISS knowledge base, "
    "citing relevant Indian legal statutes and precedents.\n\n"
    "To enable real responses, download the Mistral-7B GGUF model file "
    "and set `LEGALEAGLE_DEMO_MODE=false`."
)


class LLMGenerator:
    """Generates legal answers using a local Mistral-7B model (CTransformers).

    In demo mode, returns a canned response without requiring model weights.
    """

    def __init__(self, model_path: str | None = None, demo_mode: bool = False):
        self.llm = None
        self.demo_mode = demo_mode
        self._loaded = False

        if demo_mode:
            logger.warning("Demo mode active — LLM will return placeholder responses")
            self._loaded = True
            return

        resolved_path = model_path or str(
            settings.resolved_model_paths["mistral_gguf_path"]
        )

        try:
            from langchain_community.llms import CTransformers

            logger.info("Loading Mistral-7B from %s …", resolved_path)
            self.llm = CTransformers(
                model=resolved_path,
                model_type="mistral",
                config={
                    "max_new_tokens": settings.llm_max_new_tokens,
                    "temperature": settings.llm_temperature,
                    "context_length": settings.llm_context_length,
                    "gpu_layers": settings.llm_gpu_layers,
                },
            )
            self._loaded = True
            logger.info("Mistral-7B loaded successfully")
        except Exception as exc:
            logger.error("Failed to load Mistral-7B from '%s': %s", resolved_path, exc)
            raise RuntimeError(
                f"Mistral-7B failed to load from '{resolved_path}'. "
                f"Ensure the GGUF file is present.\n"
                f"Download: huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF "
                f"mistral-7b-instruct-v0.2.Q4_K_M.gguf "
                f"--local-dir models/Mistral-7B-Instruct-v0.2-GGUF\n"
                f"Error: {exc}"
            ) from exc

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def generate(
        self,
        context: str,
        question: str,
        chat_history: str = "No previous conversation.",
    ) -> str:
        """Generate a legal answer using the prompt template.

        Args:
            context: Retrieved document context.
            question: The user's question.
            chat_history: Formatted previous conversation.

        Returns:
            Generated answer text.
        """
        if self.demo_mode:
            return self._demo_response(question, context)

        if self.llm is None:
            raise RuntimeError("LLM is not loaded — cannot generate")

        prompt = QA_PROMPT.format(
            context=context,
            question=question,
            chat_history=chat_history,
        )

        # Retry logic: up to 3 attempts, truncating prompt on failure
        response = ""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.llm.invoke(prompt)

                # Ensure response ends cleanly
                if response and not response.rstrip().endswith((".", "!", "?", ":", ";")):
                    response = response.rstrip() + "..."

                if response.strip():
                    return response.strip()

            except Exception as exc:
                logger.warning(
                    "Generation attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries,
                    exc,
                )
                # Truncate prompt for retry
                if len(prompt) > 300:
                    prompt = prompt[:300]

        if not response.strip():
            return (
                "I was unable to generate a response for this query. "
                "Please try rephrasing your question or asking something more specific."
            )

        return response.strip()

    def _demo_response(self, question: str, context: str) -> str:
        """Generate a demo response that acknowledges the query."""
        has_context = context and "No relevant documents" not in context

        base = DEMO_RESPONSE
        if has_context:
            base += (
                f"\n\n**Retrieved context preview** (first 200 chars):\n"
                f"> {context[:200]}..."
            )
        return base
