"""
LLM generation service using local quantized model via CTransformers.

Extracted from app.py:
  - Model initialization
  - QA_PROMPT template
  - Response generation with retry logic
"""

import logging

from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Prompt Template ──────────────────────────────────────────────────
# Mistral [INST] format for Indian law Q&A

QA_PROMPT = """[INST] You are an expert assistant specializing in Indian law. Provide highly accurate, contextually appropriate, and well-structured answers strictly based on Indian legal statutes, regulations, and precedents. If you do not know the answer, say "I don't know." Do not hallucinate or make up information.

CONTEXT:
{context}

CHAT HISTORY:
{chat_history}

QUESTION:
{question}

Provide a clear and structured answer detailing key aspects of the applicable Indian law, statutory provisions, and judicial interpretations. [/INST]
"""


class LLMGenerator:
    """Generates legal answers using a local quantized model via CTransformers."""

    def __init__(self, model_path: str | None = None, demo_mode: bool = False):
        self.llm = None
        self.demo_mode = False  # Demo mode disabled: real models enforced
        self._loaded = False

        resolved_path = model_path or str(
            settings.resolved_model_paths["mistral_gguf_path"]
        )

        try:
            from langchain_community.llms import CTransformers

            logger.info("Loading LLM from %s …", resolved_path)
            try:
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
            except Exception as e:
                logger.warning("Loading with model_type='mistral' failed (%s), trying 'llama'...", e)
                self.llm = CTransformers(
                    model=resolved_path,
                    model_type="llama",
                    config={
                        "max_new_tokens": settings.llm_max_new_tokens,
                        "temperature": settings.llm_temperature,
                        "context_length": settings.llm_context_length,
                        "gpu_layers": settings.llm_gpu_layers,
                    },
                )

            self._loaded = True
            logger.info("LLM loaded successfully")
        except Exception as exc:
            logger.error("Failed to load LLM from '%s': %s", resolved_path, exc)
            raise RuntimeError(
                f"LLM failed to load from '{resolved_path}'. "
                f"Ensure the GGUF file is present.\n"
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
        if self.llm is None or not self._loaded:
            raise RuntimeError("LLM is not loaded — cannot generate answers. Please check model weights.")

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
            raise RuntimeError("LLM failed to generate a response after retries.")

        return response.strip()
