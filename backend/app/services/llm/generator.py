"""
LLM generation service using local quantized model via CTransformers.
Hardened for strict Indian legal grounding and anti-hallucination.
"""

import logging
import re
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

# ── Grounded Prompt Template ──────────────────────────────────────────
# Mistral [INST] format with strict anti-hallucination guardrails

QA_PROMPT = """[INST] You are an authoritative Indian Legal Research AI Assistant. Answer the question STRICTLY AND ONLY using the provided legal context below.

MANDATORY RULES:
1. Grounding: Rely ONLY on the facts, sections, definitions, and punishments explicitly stated in the CONTEXT. Never invent or assume provisions, subsections, or case laws not present in the context.
2. If the context does not contain the answer or does not contain the specific statutory section asked about, you MUST output EXACTLY:
Relevant information not found in the indexed corpus.
Do not attempt to answer or extrapolate beyond the provided text.
3. Structure your response cleanly using these exact headings:
### Legal Analysis
[Direct explanation strictly based on the context]

### Statutory Provisions
[Statutory sections, act names, and penalties explicitly stated in context]

### Sources & Citations
[Exact citations of acts and sections cited from context]

CONTEXT:
{context}
{chat_history_block}
QUESTION:
{question}
[/INST]
"""


class LLMGenerator:
    """Generates legal answers using a local quantized model via CTransformers."""

    def __init__(self, model_path: str | None = None, demo_mode: bool = False):
        self.llm = None
        self.demo_mode = False
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

    @staticmethod
    def _sanitize_output(text: str) -> str:
        """Strip prompt echoes, instruction tags, and formatting artifacts."""
        clean = text.strip()

        # Strip reflected [INST]...[/INST] blocks
        if "[/INST]" in clean:
            clean = clean.split("[/INST]")[-1].strip()
        if "[INST]" in clean:
            clean = clean.split("[INST]")[-1].strip()

        # Strip system preamble reflections
        prefixes_to_strip = [
            "You are an expert assistant specializing in Indian law.",
            "You are an authoritative Indian Legal Research AI Assistant.",
            "Provide a clear and structured answer",
            "ANSWER:",
            "Here is the answer:",
        ]
        for p in prefixes_to_strip:
            if clean.startswith(p):
                clean = clean[len(p):].lstrip(": \n")

        # Standardize fallback responses
        lower = clean.lower()
        if (
            "relevant information not found" in lower
            or "i don't know" in lower
            or "not found in the indexed corpus" in lower
            or "context does not contain" in lower
        ):
            return "Relevant information not found in the indexed corpus."

        return clean.strip()

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

        # Only inject chat history if there is actual prior conversation
        if chat_history and chat_history.strip() and chat_history != "No previous conversation.":
            chat_history_block = f"\nCHAT HISTORY:\n{chat_history}\n"
        else:
            chat_history_block = ""

        prompt = QA_PROMPT.format(
            context=context,
            question=question,
            chat_history_block=chat_history_block,
        )

        response = ""
        max_retries = 3

        for attempt in range(max_retries):
            try:
                raw_response = self.llm.invoke(prompt)
                sanitized = self._sanitize_output(raw_response)

                if sanitized:
                    # Ensure clean termination
                    if not sanitized.endswith((".", "!", "?", ":", ";", '"', "'")):
                        sanitized = sanitized.rstrip() + "..."
                    return sanitized

            except Exception as exc:
                logger.warning(
                    "Generation attempt %d/%d failed: %s",
                    attempt + 1,
                    max_retries,
                    exc,
                )
                if len(prompt) > 300:
                    prompt = prompt[:300]

        if not response.strip():
            return "Relevant information not found in the indexed corpus."

        return response.strip()
