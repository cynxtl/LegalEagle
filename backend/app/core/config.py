"""
Application configuration using pydantic-settings.

All paths are relative to the project root (parent of backend/).
Validates model file existence at startup with clear error messages.
"""

import os
import logging
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import Field

logger = logging.getLogger(__name__)

# Project root is two levels up from this file: backend/app/core/config.py → project root
_THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _THIS_DIR.parent.parent.parent  # → LegalEagle/


class ModelPaths(BaseSettings):
    """Paths to local model files, resolved relative to PROJECT_ROOT."""

    inlegalbert_dir: str = Field(
        default="models/InLegalBERT",
        description="Directory containing InLegalBERT tokenizer and model files",
    )
    mistral_gguf_path: str = Field(
        default="models/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf",
        description="Path to the Mistral-7B GGUF weight file",
    )

    def resolve(self, root: Path) -> dict:
        """Return absolute paths resolved against project root."""
        return {
            "inlegalbert_dir": root / self.inlegalbert_dir,
            "mistral_gguf_path": root / self.mistral_gguf_path,
        }


class Settings(BaseSettings):
    """Central application settings.

    Values can be overridden via environment variables prefixed with
    ``LEGALEAGLE_`` (e.g. ``LEGALEAGLE_HOST=0.0.0.0``).
    """

    model_config = {"env_prefix": "LEGALEAGLE_"}

    # ── Server ────────────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list[str] = ["*"]

    # ── Paths ─────────────────────────────────────────────────────────
    project_root: Path = PROJECT_ROOT
    faiss_index_dir: str = "LegalKB_FAISS/ipc_embed_db"
    mini_dataset_dir: str = "mini_dataset"

    # ── Models ────────────────────────────────────────────────────────
    model_paths: ModelPaths = ModelPaths()

    # ── LLM parameters ────────────────────────────────────────────────
    llm_max_new_tokens: int = 512
    llm_temperature: float = 0.7
    llm_context_length: int = 2048
    llm_gpu_layers: int = 0

    # ── Embedding parameters ──────────────────────────────────────────
    embedding_max_length: int = 512
    embedding_batch_size: int = 10

    # ── Retrieval parameters ──────────────────────────────────────────
    retrieval_top_k: int = 3

    # ── Feature flags ─────────────────────────────────────────────────
    demo_mode: bool = Field(
        default=False,
        description=(
            "When True, the backend uses mock/lightweight models if the real "
            "model files are not found. Useful for development and demos."
        ),
    )

    # TODO: Production auth — add API key / JWT settings here
    # auth_enabled: bool = False
    # api_key: Optional[str] = None

    # ── Computed helpers ──────────────────────────────────────────────

    @property
    def faiss_index_path(self) -> Path:
        return self.project_root / self.faiss_index_dir

    @property
    def dataset_path(self) -> Path:
        return self.project_root / self.mini_dataset_dir

    @property
    def resolved_model_paths(self) -> dict:
        return self.model_paths.resolve(self.project_root)


# ── Startup validation ────────────────────────────────────────────────

class ModelValidationError:
    """Container for a single missing-model diagnostic."""

    def __init__(self, name: str, expected_path: Path, hint: str):
        self.name = name
        self.expected_path = expected_path
        self.hint = hint

    def __str__(self) -> str:
        return (
            f"  ✗ {self.name}\n"
            f"    Expected at : {self.expected_path}\n"
            f"    Fix         : {self.hint}"
        )


def validate_model_files(settings: Settings) -> list[ModelValidationError]:
    """Check that required model artefacts exist on disk.

    Returns a list of ``ModelValidationError`` objects — empty means
    everything is fine.
    """
    errors: list[ModelValidationError] = []
    resolved = settings.resolved_model_paths

    # InLegalBERT — we need at minimum config.json + vocab.txt + a weight file
    bert_dir: Path = resolved["inlegalbert_dir"]
    if not bert_dir.is_dir():
        errors.append(
            ModelValidationError(
                "InLegalBERT directory",
                bert_dir,
                "Download from HuggingFace: "
                "huggingface-cli download law-ai/InLegalBERT --local-dir models/InLegalBERT",
            )
        )
    else:
        # Check for weight file (could be pytorch_model.bin or model.safetensors)
        has_weights = any(
            (bert_dir / f).exists()
            for f in [
                "pytorch_model.bin",
                "model.safetensors",
                "tf_model.h5",
            ]
        )
        if not has_weights:
            errors.append(
                ModelValidationError(
                    "InLegalBERT model weights",
                    bert_dir / "pytorch_model.bin",
                    "Run: huggingface-cli download law-ai/InLegalBERT --local-dir models/InLegalBERT",
                )
            )

    # Mistral-7B GGUF
    mistral_path: Path = resolved["mistral_gguf_path"]
    if not mistral_path.is_file():
        errors.append(
            ModelValidationError(
                "Mistral-7B GGUF weights",
                mistral_path,
                "Download from HuggingFace: "
                "huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF "
                "mistral-7b-instruct-v0.2.Q4_K_M.gguf "
                "--local-dir models/Mistral-7B-Instruct-v0.2-GGUF",
            )
        )

    return errors


def format_validation_report(errors: list[ModelValidationError]) -> str:
    """Return a human-readable diagnostic report."""
    if not errors:
        return "All model files verified ✓"

    lines = [
        "=" * 60,
        "MODEL FILES MISSING — Backend cannot fully start",
        "=" * 60,
        "",
        f"Found {len(errors)} missing model file(s):",
        "",
    ]
    for err in errors:
        lines.append(str(err))
        lines.append("")

    lines.extend([
        "Set LEGALEAGLE_DEMO_MODE=true to run with mock models instead.",
        "=" * 60,
    ])
    return "\n".join(lines)


# Singleton settings instance
settings = Settings()
