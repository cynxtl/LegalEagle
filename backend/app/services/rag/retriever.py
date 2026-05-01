"""
FAISS-based vector retriever.

Extracted from app.py initialize_legal_knowledge_base() (lines 290-407)
and the chat handler retrieval logic (lines 841-854).
Loads the pre-built FAISS index from LegalKB_FAISS/ipc_embed_db or
rebuilds from mini_dataset if the index is missing.
"""

import json
import logging
import os
from pathlib import Path
from typing import Optional

from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

from backend.app.core.config import settings
from backend.app.services.rag.embedder import InLegalBERTEmbeddings

logger = logging.getLogger(__name__)


class FAISSRetriever:
    """Manages the FAISS vector store for Indian legal knowledge retrieval."""

    def __init__(self, embedder: InLegalBERTEmbeddings):
        self.embedder = embedder
        self.vector_store: Optional[FAISS] = None
        self._loaded = False

    @property
    def is_loaded(self) -> bool:
        return self._loaded and self.vector_store is not None

    def load_index(self) -> bool:
        """Load the pre-built FAISS index from disk.

        Returns True if loading succeeded, False otherwise.
        If the pre-built index is missing, attempts to build from datasets.
        """
        index_dir = settings.faiss_index_path
        index_faiss = index_dir / "index.faiss"
        index_pkl = index_dir / "index.pkl"

        logger.info("Looking for FAISS index at %s", index_dir)

        if index_faiss.exists() and index_pkl.exists():
            try:
                self.vector_store = FAISS.load_local(
                    str(index_dir),
                    self.embedder,
                    allow_dangerous_deserialization=True,
                )
                self._loaded = True
                logger.info("FAISS index loaded from %s", index_dir)
                return True
            except Exception as exc:
                logger.error("Failed to load FAISS index: %s", exc)

        # Fallback: build from dataset files
        logger.info("Pre-built index not found — building from datasets…")
        return self._build_from_datasets()

    def _build_from_datasets(self) -> bool:
        """Build a FAISS index from the mini_dataset (and extra_dataset if present)."""
        all_docs: list[str] = []
        dataset_dir = settings.dataset_path

        # ── mini_dataset ──────────────────────────────────────────────
        cases_path = dataset_dir / "mini_legal_cases.txt"
        dict_path = dataset_dir / "mini_legal_dictionary.txt"
        qa_path = dataset_dir / "mini_train.jsonl"

        if cases_path.exists():
            logger.info("Loading %s", cases_path)
            all_docs.append(cases_path.read_text(encoding="utf-8"))

        if dict_path.exists():
            logger.info("Loading %s", dict_path)
            lines = dict_path.read_text(encoding="utf-8").splitlines()
            all_docs.extend(line.strip() for line in lines if line.strip())

        if qa_path.exists():
            logger.info("Loading %s", qa_path)
            try:
                content = qa_path.read_text(encoding="utf-8")
                qa_items = json.loads(content)
                for item in qa_items:
                    if isinstance(item, dict):
                        q = item.get("Instruction") or item.get("question")
                        a = item.get("output") or item.get("answer") or item.get("Response")
                        if q and a:
                            all_docs.append(f"Q: {q}\nA: {a}")
            except Exception as exc:
                logger.warning("Failed to parse %s: %s", qa_path, exc)

        # ── extra_dataset (optional) ──────────────────────────────────
        extra_dir = settings.project_root / "extra_dataset"
        if extra_dir.is_dir():
            for fname in [
                "ipc_qa.json",
                "crpc_qa.json",
                "constitution_qa.json",
                "IndicLegalQA Dataset_10K_Revised.json",
            ]:
                fpath = extra_dir / fname
                if fpath.exists():
                    logger.info("Loading extra dataset: %s", fpath)
                    try:
                        items = json.loads(fpath.read_text(encoding="utf-8"))
                        for item in items:
                            q = item.get("question")
                            a = item.get("answer")
                            if q and a:
                                all_docs.append(f"Q: {q}\nA: {a}")
                    except Exception as exc:
                        logger.warning("Failed to parse %s: %s", fpath, exc)

        if not all_docs:
            logger.warning("No documents found to build FAISS index")
            return False

        # Limit for reasonable build time
        doc_limit = 300
        if len(all_docs) > doc_limit:
            logger.info(
                "Limiting to %d documents (of %d) for index build",
                doc_limit,
                len(all_docs),
            )
            all_docs = all_docs[:doc_limit]

        try:
            logger.info("Embedding %d documents…", len(all_docs))
            batch_size = settings.embedding_batch_size
            embeddings: list[list[float]] = []

            for i in range(0, len(all_docs), batch_size):
                batch = all_docs[i : i + batch_size]
                batch_emb = self.embedder.embed_documents(batch)
                embeddings.extend(batch_emb)
                logger.info(
                    "  Embedded %d / %d",
                    min(i + batch_size, len(all_docs)),
                    len(all_docs),
                )

            text_embeddings = list(zip(all_docs, embeddings))
            self.vector_store = FAISS.from_embeddings(
                text_embeddings, self.embedder
            )

            # Persist to disk
            index_dir = settings.faiss_index_path
            index_dir.mkdir(parents=True, exist_ok=True)
            self.vector_store.save_local(str(index_dir))
            self._loaded = True
            logger.info("FAISS index built and saved to %s", index_dir)
            return True

        except Exception as exc:
            logger.error("Failed to build FAISS index: %s", exc)
            return False

    # ── Retrieval ─────────────────────────────────────────────────────

    def retrieve(
        self, query: str, k: int | None = None
    ) -> list[dict]:
        """Retrieve the top-k most relevant documents for a query.

        Returns a list of dicts with ``content`` and ``score`` keys.
        """
        if not self.is_loaded:
            logger.warning("retrieve() called but FAISS index is not loaded")
            return []

        top_k = k or settings.retrieval_top_k

        try:
            docs_with_scores = self.vector_store.similarity_search_with_score(
                query, k=top_k
            )
            results = []
            for i, (doc, score) in enumerate(docs_with_scores):
                results.append(
                    {
                        "content": doc.page_content,
                        "score": float(score),
                        "metadata": doc.metadata,
                        "index": i,
                    }
                )
            return results
        except Exception as exc:
            logger.error("Retrieval failed: %s", exc)
            return []

    def add_documents(self, texts: list[str]) -> bool:
        """Embed and add new document chunks to the vector store."""
        if not self.is_loaded:
            logger.warning("add_documents() called but FAISS index is not loaded")
            return False

        try:
            new_store = FAISS.from_texts(
                texts=texts, embedding=self.embedder
            )
            self.vector_store.merge_from(new_store)

            # Persist updated index
            index_dir = settings.faiss_index_path
            self.vector_store.save_local(str(index_dir))
            logger.info("Added %d chunks and saved updated index", len(texts))
            return True
        except Exception as exc:
            logger.error("Failed to add documents: %s", exc)
            return False
