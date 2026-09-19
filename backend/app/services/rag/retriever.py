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
from backend.app.services.rag.query_classifier import classify_query, QueryClassification
from backend.app.services.rag.statute_mapper import statute_mapper

logger = logging.getLogger(__name__)


class FAISSRetriever:
    """Manages the FAISS vector store for Indian legal knowledge retrieval."""

    DOMAIN_EXCLUSIONS = {
        "criminal_law": {"tax_law", "tenancy_law"},
        "constitutional_law": {"tax_law", "tenancy_law", "criminal_law"},
        "procedural_law": {"tax_law", "tenancy_law"},
        "law_of_evidence": {"tax_law", "tenancy_law"},
        "tenancy_law": {"tax_law", "criminal_law", "procedural_law", "law_of_evidence"},
        "tax_law": {"criminal_law", "constitutional_law", "procedural_law", "law_of_evidence", "tenancy_law"},
    }

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
        """Retrieve the top-k most relevant documents for a legal query.

        Applies multi-stage domain-intelligent retrieval:
          Tier 1: Exact statutory section and modern/historical companion resolution
                  (e.g., Section 420 IPC -> 420 IPC [primary] + 318 BNS [companion]).
          Tier 2: Domain-filtered dense semantic retrieval prioritizing candidate
                  pool matching the classified legal domain, while strictly
                  excluding incompatible domains (e.g. tax law excluded from criminal queries).
        
        Returns a list of dicts with content, score, metadata, provenance, and index.
        """
        if not self.is_loaded or self.vector_store is None:
            logger.warning("retrieve() called but FAISS index is not loaded")
            return []

        top_k = k or settings.retrieval_top_k

        try:
            classification = classify_query(query)
            primary_domain = classification.primary_domain
            detected_sections = classification.detected_sections
            excluded = self.DOMAIN_EXCLUSIONS.get(primary_domain, set())

            final_results = []
            seen_contents = set()

            # ── Tier 1: Statutory Match & Companion Alias Lookup ───────
            if detected_sections and self.vector_store.docstore:
                for item in detected_sections:
                    act = item["act"].upper()
                    sec = item["section"].upper()

                    # 1. Primary statutory section lookup
                    for doc_id, doc in self.vector_store.docstore._dict.items():
                        m = doc.metadata
                        m_sec = str(m.get("section", "")).strip().upper()
                        m_act = str(m.get("act", "")).strip().upper()

                        sec_match = (
                            m_sec == sec
                            or m_sec == f"ARTICLE {sec}"
                            or m_sec == f"SECTION {sec}"
                            or f"SECTION {sec}" in m_sec
                            or f"ARTICLE {sec}" in m_sec
                        )
                        act_match = False
                        if "IPC" in act or "PENAL" in act:
                            act_match = "PENAL" in m_act or "IPC" in m_act
                        elif "BNS" in act or "NYAYA" in act:
                            act_match = "NYAYA" in m_act or "BNS" in m_act
                        elif "CRPC" in act or "PROCEDURE" in act:
                            act_match = "PROCEDURE" in m_act or "CRPC" in m_act
                        elif "BNSS" in act or "SURAKSHA" in act:
                            act_match = "SURAKSHA" in m_act or "BNSS" in m_act
                        elif "IEA" in act or "EVIDENCE" in act:
                            act_match = "EVIDENCE" in m_act or "IEA" in m_act
                        elif "BSA" in act or "SAKSHYA" in act:
                            act_match = "SAKSHYA" in m_act or "BSA" in m_act
                        elif "CONSTITUTION" in act:
                            act_match = "CONSTITUTION" in m_act

                        if sec_match and act_match:
                            clean_text = doc.page_content.strip()
                            if clean_text not in seen_contents:
                                seen_contents.add(clean_text)
                                final_results.append({
                                    "content": clean_text,
                                    "score": 0.0100,
                                    "metadata": m,
                                    "retrieval_stage": "primary_statute",
                                })
                                break

                    # 2. Companion statute lookup (IPC <-> BNS, CrPC <-> BNSS, IEA <-> BSA)
                    equivalents = statute_mapper.get_equivalents(act, sec)
                    for equiv in equivalents:
                        eq_act = equiv["act"].upper()
                        eq_sec = equiv["section"].upper()

                        for doc_id, doc in self.vector_store.docstore._dict.items():
                            m = doc.metadata
                            m_sec = str(m.get("section", "")).strip().upper()
                            m_act = str(m.get("act", "")).strip().upper()

                            sec_match = (
                                m_sec == eq_sec
                                or m_sec == f"SECTION {eq_sec}"
                                or f"SECTION {eq_sec}" in m_sec
                            )
                            act_match = (
                                ("NYAYA" in eq_act and "NYAYA" in m_act)
                                or ("PENAL" in eq_act and "PENAL" in m_act)
                                or ("SURAKSHA" in eq_act and "SURAKSHA" in m_act)
                                or ("PROCEDURE" in eq_act and "PROCEDURE" in m_act)
                                or ("SAKSHYA" in eq_act and "SAKSHYA" in m_act)
                                or ("EVIDENCE" in eq_act and "EVIDENCE" in m_act)
                            )
                            if sec_match and act_match:
                                clean_text = doc.page_content.strip()
                                if clean_text not in seen_contents:
                                    seen_contents.add(clean_text)
                                    final_results.append({
                                        "content": clean_text,
                                        "score": 0.0500,
                                        "metadata": m,
                                        "retrieval_stage": "mapped_companion",
                                    })
                                    break

            # ── Tier 2: Domain-Filtered Dense Similarity Search ────────
            total_vectors = len(self.vector_store.docstore._dict) if self.vector_store.docstore else 100
            dense_candidates = self.vector_store.similarity_search_with_score(
                query, k=total_vectors
            )

            primary_pool = []
            secondary_pool = []
            general_pool = []

            for doc, score in dense_candidates:
                txt = doc.page_content.strip()
                if txt in seen_contents:
                    continue

                d = doc.metadata.get("domain", "")
                if d in excluded:
                    continue

                is_primary = (
                    d == primary_domain
                    or (primary_domain == "general_legal_qa" and d in {"legal_qa", "general_legal_qa"})
                )
                is_secondary = d in classification.secondary_domains
                is_legal_qa = d in {"legal_qa", "general_legal_qa"}

                cand = {
                    "content": txt,
                    "score": float(score),
                    "metadata": doc.metadata,
                    "retrieval_stage": "dense_semantic",
                }

                if is_primary:
                    primary_pool.append(cand)
                elif is_secondary or is_legal_qa:
                    secondary_pool.append(cand)
                else:
                    general_pool.append(cand)

            # Fill remaining slots up to top_k: primary domain first
            for item in primary_pool:
                if len(final_results) >= top_k:
                    break
                seen_contents.add(item["content"])
                final_results.append(item)

            for item in secondary_pool:
                if len(final_results) >= top_k:
                    break
                seen_contents.add(item["content"])
                final_results.append(item)

            for item in general_pool:
                if len(final_results) >= top_k:
                    break
                seen_contents.add(item["content"])
                final_results.append(item)

            # Assign index and provenance metadata
            for i, res in enumerate(final_results):
                res["index"] = i
                m = res.get("metadata") or {}
                res["provenance"] = {
                    "act": m.get("act"),
                    "section": m.get("section"),
                    "title": m.get("title"),
                    "domain": m.get("domain"),
                    "source_type": m.get("source_type"),
                    "year": m.get("year"),
                }

            return final_results[:top_k]

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
