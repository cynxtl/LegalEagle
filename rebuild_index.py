"""
LegalEagle Corpus Ingestion & FAISS Index Builder.

Separates ingestion from runtime retrieval.
Recursively reads all structured legal documents across multi-domain subdirectories:
  corpus/
  ├── criminal/ (IPC, BNS)
  ├── procedure/ (BNSS, CrPC)
  ├── evidence/ (BSA, IEA)
  ├── constitution/ (Fundamental Rights)
  ├── tenancy/ (Rent Control & Tenant Protections)
  ├── qa/ (Cleaned Indian Legal Q&As)
  └── cases/ (Tax & Constitutional Landmark Cases)

Applies RecursiveCharacterTextSplitter (chunk_size=600, overlap=60) with strict validation:
  - chunk <= 800 chars
  - no empty chunks
  - no duplicate chunks
  - no table-of-contents chunks
  - no heading-only chunks

Generates dense InLegalBERT embeddings (768-dim) and saves persistent FAISS index
at LegalKB_FAISS/ipc_embed_db.
"""

import json
import logging
import re
import sys
from pathlib import Path
from typing import Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.core.config import settings
from backend.app.services.rag.embedder import InLegalBERTEmbeddings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(name)s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("rebuild_index")


def load_corpus(corpus_dir: Path) -> list[dict]:
    """Recursively load all JSON legal documents from all domain subdirectories."""
    documents = []
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    json_files = sorted(corpus_dir.rglob("*.json"))
    logger.info("Discovered %d JSON corpus files across domain folders", len(json_files))

    for file_path in json_files:
        rel_path = file_path.relative_to(corpus_dir)
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            count = 0
            if isinstance(data, list):
                for doc in data:
                    # Infer domain from folder if not explicit
                    if "domain" not in doc:
                        doc["domain"] = rel_path.parent.name
                    documents.append(doc)
                    count += 1
            elif isinstance(data, dict):
                if "domain" not in data:
                    data["domain"] = rel_path.parent.name
                documents.append(data)
                count += 1
            logger.info("Loaded %3d documents from %s", count, rel_path)
        except Exception as exc:
            logger.error("Failed to read %s: %exc", rel_path, exc)

    return documents


def is_table_of_contents(text: str) -> bool:
    """Detect if chunk is a table of contents or outline."""
    lower = text.lower()
    if "table of contents" in lower:
        return True
    if re.search(r"(\.{4,}|\bpage\b\s*\d+)", lower):
        return True
    # If more than 4 section listing lines in short text
    sec_lines = re.findall(r"^(?:section|article|chapter)\s+\d+", lower, re.MULTILINE)
    if len(sec_lines) >= 4 and len(text) < 400:
        return True
    return False


def is_heading_only(text: str) -> bool:
    """Detect if chunk contains only headers without substantive body text."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return True
    if len(text.strip()) >= 120:
        return False
    # Strip metadata header lines
    body_lines = [l for l in lines if not any(l.startswith(prefix) for prefix in [
        "Act:", "Section", "Article", "Domain:", "Topic:", "Case Law:", "Year:", "Question:"
    ])]
    body_text = " ".join(body_lines).strip()
    return len(body_text) < 50


def chunk_documents(documents: list[dict]) -> tuple[list[str], list[dict]]:
    """Chunk legal documents with RecursiveCharacterTextSplitter and strict validation.

    Constraints:
      - chunk_size = 600
      - chunk_overlap = 60
      - chunk <= 800 chars
      - No empty chunks
      - No duplicate chunks
      - No table-of-contents chunks
      - No heading-only chunks
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunk_texts = []
    all_chunk_metadatas = []
    seen_hashes = set()

    for doc in documents:
        doc_id = str(doc.get("id", "")).strip()
        section = str(doc.get("section", "")).strip()
        title = doc.get("title", "").strip()
        act = doc.get("act", "").strip()
        domain = doc.get("domain", "general_law").strip()
        source_type = doc.get("source_type", "statute").strip()
        year = str(doc.get("year", "")).strip()
        content = doc.get("content", "").strip()

        if not content:
            continue

        # Construct semantic header based on source_type
        if source_type == "qa":
            header = f"Domain: Legal Q&A\nTopic: {title}\n\n"
        elif source_type == "case_law":
            header = f"Case Law: {title}\nAct: {act}\n\n"
        elif "article" in section.lower():
            header = f"Act: {act}\n{section}: {title}\n\n"
        elif section:
            header = f"Act: {act}\nSection {section}: {title}\n\n"
        else:
            header = f"Act: {act}\nTitle: {title}\n\n"

        raw_chunks = splitter.split_text(content)
        total_chunks = len(raw_chunks)

        for idx, chunk in enumerate(raw_chunks, start=1):
            contextual_text = f"{header}{chunk}"

            # Sub-split if exceeding hard upper bound
            candidate_chunks = []
            if len(contextual_text) > 800:
                sub_chunks = splitter.split_text(contextual_text)
                candidate_chunks.extend(sub_chunks)
            else:
                candidate_chunks.append(contextual_text)

            for sub_idx, cand in enumerate(candidate_chunks, start=1):
                clean_cand = cand.strip()

                # Validation Rule 1: No empty chunks
                if not clean_cand:
                    continue

                # Validation Rule 2: Hard bound <= 800 chars
                if len(clean_cand) > 800:
                    clean_cand = clean_cand[:800]

                # Validation Rule 3: No duplicate chunks
                norm_key = re.sub(r"\s+", " ", clean_cand.lower())
                if norm_key in seen_hashes:
                    continue
                seen_hashes.add(norm_key)

                # Validation Rule 4: No table-of-contents chunks
                if is_table_of_contents(clean_cand):
                    logger.debug("Filtered TOC chunk: %s", clean_cand[:60])
                    continue

                # Validation Rule 5: No heading-only chunks
                if is_heading_only(clean_cand):
                    logger.debug("Filtered heading-only chunk: %s", clean_cand[:60])
                    continue

                all_chunk_texts.append(clean_cand)
                all_chunk_metadatas.append({
                    "id": f"{doc_id}-{idx}.{sub_idx}" if doc_id else f"{section}-{idx}",
                    "section": section,
                    "title": title,
                    "act": act,
                    "domain": domain,
                    "source_type": source_type,
                    "year": year,
                    "chunk_id": f"{idx}.{sub_idx}" if len(candidate_chunks) > 1 else idx,
                    "total_chunks": total_chunks,
                })

    return all_chunk_texts, all_chunk_metadatas


def rebuild_index():
    """Main execution function to rebuild FAISS index across all domains."""
    logger.info("=" * 65)
    logger.info("LegalEagle Multi-Domain Corpus Ingestion & FAISS Index Rebuild")
    logger.info("=" * 65)

    corpus_dir = PROJECT_ROOT / "corpus"
    index_dir = PROJECT_ROOT / "LegalKB_FAISS" / "ipc_embed_db"
    index_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Multi-Domain Corpus
    docs = load_corpus(corpus_dir)
    logger.info("Loaded %d legal documents across all subdirectories", len(docs))

    # 2. Chunk Corpus with Strict Validation
    chunk_texts, chunk_metadatas = chunk_documents(docs)
    logger.info("Generated %d validated chunks from %d documents", len(chunk_texts), len(docs))

    # Verification: Verify no chunk > 800 characters
    oversized = [len(c) for c in chunk_texts if len(c) > 800]
    if oversized:
        raise ValueError(f"Found {len(oversized)} chunks exceeding 800 characters: {oversized}")
    logger.info("✓ Validation passed: all %d chunks are <= 800 chars (max: %d chars)", len(chunk_texts), max(len(c) for c in chunk_texts))

    # Domain Breakdown
    domain_counts = {}
    source_type_counts = {}
    for meta in chunk_metadatas:
        d = meta.get("domain", "unknown")
        st = meta.get("source_type", "unknown")
        domain_counts[d] = domain_counts.get(d, 0) + 1
        source_type_counts[st] = source_type_counts.get(st, 0) + 1

    # 3. Initialize InLegalBERT Embedder
    logger.info("Initializing InLegalBERT embedding engine...")
    embedder = InLegalBERTEmbeddings(demo_mode=False)
    logger.info("✓ InLegalBERT ready (768 dimensions)")

    # 4. Build Vector Store
    logger.info("Generating dense embeddings and building FAISS vector store...")
    vector_store = FAISS.from_texts(
        texts=chunk_texts,
        embedding=embedder,
        metadatas=chunk_metadatas,
    )

    # 5. Persist FAISS Index
    logger.info("Saving index to %s ...", index_dir)
    vector_store.save_local(str(index_dir))

    faiss_file = index_dir / "index.faiss"
    pkl_file = index_dir / "index.pkl"
    faiss_size_kb = faiss_file.stat().st_size / 1024
    pkl_size_kb = pkl_file.stat().st_size / 1024
    total_size_kb = faiss_size_kb + pkl_size_kb

    # 6. Index Summary Report
    print("\n" + "=" * 65)
    print("FAISS MULTI-DOMAIN REBUILD SUMMARY REPORT")
    print("=" * 65)
    print(f"Documents Indexed     : {len(docs)}")
    print(f"Chunks Generated      : {len(chunk_texts)}")
    print(f"Max Chunk Size        : {max(len(c) for c in chunk_texts)} characters")
    print(f"Min Chunk Size        : {min(len(c) for c in chunk_texts)} characters")
    print(f"Avg Chunk Size        : {sum(len(c) for c in chunk_texts) / len(chunk_texts):.1f} characters")
    print(f"Embedding Model       : law-ai/InLegalBERT")
    print(f"Embedding Dimensions  : {InLegalBERTEmbeddings.EMBEDDING_DIM}")
    print(f"Index Files           : {faiss_file.name} ({faiss_size_kb:.1f} KB), {pkl_file.name} ({pkl_size_kb:.1f} KB)")
    print(f"Total Index Size      : {total_size_kb:.1f} KB ({total_size_kb / 1024:.2f} MB)")
    print(f"Destination Path      : {index_dir}")
    print("-" * 65)
    print("Domain Breakdown:")
    for d, c in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {d:20}: {c:4} chunks ({c/len(chunk_texts)*100:.1f}%)")
    print("-" * 65)
    print("Source Type Breakdown:")
    for st, c in sorted(source_type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {st:20}: {c:4} chunks ({c/len(chunk_texts)*100:.1f}%)")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    rebuild_index()
