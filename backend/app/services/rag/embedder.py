"""
InLegalBERT embedding model wrapper.

Extracted from app.py CustomEmbeddings class (lines 119-178).
Implements the LangChain Embeddings interface for FAISS compatibility.
Supports demo mode with random embeddings when model files are missing.
"""

import logging
from typing import List, Union

import numpy as np
import torch
from langchain.embeddings.base import Embeddings

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class InLegalBERTEmbeddings(Embeddings):
    """LangChain-compatible embeddings using InLegalBERT.

    Loads the model from a local directory. Falls back to random
    768-dim embeddings when ``demo_mode`` is active and weights are missing.
    """

    EMBEDDING_DIM = 768

    def __init__(self, model_dir: str | None = None, demo_mode: bool = False):
        self.model = None
        self.tokenizer = None
        self.demo_mode = demo_mode
        self._loaded = False

        model_path = model_dir or str(
            settings.resolved_model_paths["inlegalbert_dir"]
        )

        if demo_mode:
            logger.warning(
                "Demo mode active — InLegalBERT will return random embeddings"
            )
            self._loaded = True
            return

        try:
            from transformers import AutoTokenizer, AutoModel

            logger.info("Loading InLegalBERT from %s …", model_path)
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModel.from_pretrained(model_path)
            self.model.eval()

            if torch.cuda.is_available():
                self.model = self.model.cuda()
                logger.info("InLegalBERT moved to CUDA")

            self._loaded = True
            logger.info("InLegalBERT loaded successfully")
        except Exception as exc:
            logger.error(
                "Failed to load InLegalBERT from '%s': %s", model_path, exc
            )
            raise RuntimeError(
                f"InLegalBERT failed to load from '{model_path}'. "
                f"Ensure all required files are present "
                f"(config.json, pytorch_model.bin, tokenizer_config.json, "
                f"special_tokens_map.json, vocab.txt).\n"
                f"Error: {exc}"
            ) from exc

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    # ── Core embedding logic (mean pooling) ─────────────────────────

    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Compute embeddings via mean pooling of last hidden states."""
        if self.demo_mode:
            rng = np.random.default_rng(42)
            return [
                rng.standard_normal(self.EMBEDDING_DIM).tolist()
                for _ in texts
            ]

        if self.model is None or self.tokenizer is None:
            raise RuntimeError("InLegalBERT model is not loaded")

        embeddings: List[List[float]] = []
        max_len = settings.embedding_max_length

        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    padding=True,
                    truncation=True,
                    max_length=max_len,
                )
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}

                outputs = self.model(**inputs)
                last_hidden = outputs.last_hidden_state
                attention_mask = inputs["attention_mask"]

                # Mean pooling
                mask_expanded = (
                    attention_mask.unsqueeze(-1)
                    .expand(last_hidden.size())
                    .float()
                )
                sum_embeddings = torch.sum(last_hidden * mask_expanded, dim=1)
                sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
                embedding = sum_embeddings / sum_mask

                embeddings.append(embedding[0].cpu().numpy().tolist())

        return embeddings

    # ── LangChain Embeddings interface ──────────────────────────────

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of document texts."""
        try:
            return self._get_embeddings(texts)
        except Exception as exc:
            logger.error("embed_documents failed: %s", exc)
            return [[0.0] * self.EMBEDDING_DIM] * len(texts)

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string."""
        try:
            return self._get_embeddings([text])[0]
        except Exception as exc:
            logger.error("embed_query failed: %s", exc)
            return [0.0] * self.EMBEDDING_DIM

    def __call__(
        self, texts: Union[str, List[str]]
    ) -> Union[List[float], List[List[float]]]:
        if isinstance(texts, str):
            return self.embed_query(texts)
        return self.embed_documents(texts)
