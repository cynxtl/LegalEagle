"""
LegalEagle Corpus Ingestion & FAISS Index Builder.

Separates ingestion from runtime retrieval.
Reads structured Indian Penal Code sections from `corpus/`,
chunks them via RecursiveCharacterTextSplitter (chunk_size=600, overlap=60),
validates chunk sizes (<= 800 chars), generates real 768-dim InLegalBERT embeddings,
and builds a clean, persistent FAISS index in `LegalKB_FAISS/ipc_embed_db`.
"""

import json
import os
import sys
import logging
from pathlib import Path

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
    """Load all JSON and text legal documents from corpus directory."""
    documents = []
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    for file_path in sorted(corpus_dir.glob("*.json")):
        logger.info("Loading corpus file: %s", file_path.name)
        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                documents.extend(data)
            elif isinstance(data, dict):
                documents.append(data)
        except Exception as exc:
            logger.error("Failed to read %s: %s", file_path, exc)

    return documents


def chunk_documents(documents: list[dict]) -> tuple[list[str], list[dict]]:
    """Chunk legal documents using RecursiveCharacterTextSplitter.

    Constraints:
      - chunk_size = 600
      - chunk_overlap = 60
      - Max chunk size <= 800 chars
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=60,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunk_texts = []
    all_chunk_metadatas = []

    for doc in documents:
        section = str(doc.get("section", "")).strip()
        title = doc.get("title", "").strip()
        act = doc.get("act", "IPC").strip()
        content = doc.get("content", "").strip()

        if not content:
            continue

        raw_chunks = splitter.split_text(content)
        total_chunks = len(raw_chunks)

        for idx, chunk in enumerate(raw_chunks, start=1):
            # Prepend contextual header so dense embedder retains section association
            contextual_text = f"Act: {act}\nSection {section}: {title}\n\n{chunk}"

            # Validate hard upper bound
            if len(contextual_text) > 800:
                logger.warning(
                    "Chunk for Section %s exceeded 800 chars (%d). Splitting further.",
                    section,
                    len(contextual_text),
                )
                sub_chunks = splitter.split_text(contextual_text)
                for sub_idx, sub_c in enumerate(sub_chunks, start=1):
                    all_chunk_texts.append(sub_c)
                    all_chunk_metadatas.append(
                        {
                            "section": section,
                            "title": title,
                            "act": act,
                            "chunk_id": f"{idx}.{sub_idx}",
                            "total_chunks": total_chunks,
                        }
                    )
            else:
                all_chunk_texts.append(contextual_text)
                all_chunk_metadatas.append(
                    {
                        "section": section,
                        "title": title,
                        "act": act,
                        "chunk_id": idx,
                        "total_chunks": total_chunks,
                    }
                )

    return all_chunk_texts, all_chunk_metadatas


def rebuild_index():
    """Main execution function to rebuild FAISS index."""
    logger.info("=" * 65)
    logger.info("Starting LegalEagle Corpus Ingestion & FAISS Index Rebuild")
    logger.info("=" * 65)

    corpus_dir = PROJECT_ROOT / "corpus"
    index_dir = PROJECT_ROOT / "LegalKB_FAISS" / "ipc_embed_db"
    index_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load Corpus
    docs = load_corpus(corpus_dir)
    logger.info("Loaded %d legal documents from %s", len(docs), corpus_dir)

    # 2. Chunk Corpus
    chunk_texts, chunk_metadatas = chunk_documents(docs)
    logger.info("Generated %d chunks from %d documents", len(chunk_texts), len(docs))

    # Verification: Verify no chunk > 800 characters
    oversized = [len(c) for c in chunk_texts if len(c) > 800]
    if oversized:
        raise ValueError(f"Found {len(oversized)} chunks exceeding 800 characters: {oversized}")
    logger.info("✓ Chunk validation passed: all %d chunks are <= 800 chars (max: %d)", len(chunk_texts), max(len(c) for c in chunk_texts))

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
    print("FAISS REBUILD SUMMARY REPORT")
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
    print("=" * 65 + "\n")


if __name__ == "__main__":
    rebuild_index()
