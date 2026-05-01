# LegalEagle

LegalEagle is a local-first Indian legal research assistant. It combines a Next.js chat interface with a FastAPI retrieval backend that searches a FAISS knowledge base and generates grounded legal answers using local model weights.

> LegalEagle is an informational research tool. It does not provide legal advice. Users should consult a qualified legal professional for matter-specific guidance.

## Features

- Chat interface for Indian legal questions
- Retrieval-augmented generation over a local FAISS index
- Source-aware responses shaped for frontend citation cards
- PDF, DOCX, and TXT document upload endpoint
- Demo mode for development without model weights
- Local model paths for InLegalBERT embeddings and Mistral GGUF generation
- Modern Next.js app shell with chat, documents, sources, and settings pages

## Repository Structure

```text
LegalEagle/
  backend/                 FastAPI API service
    app/
      routes/              /chat, /upload, /health
      services/rag/        Embedding, retrieval, loading, RAG pipeline
      services/llm/        Local LLM generation wrapper
      models/              Pydantic API schemas
      core/                Settings and model validation
  frontend/                Next.js + React + TypeScript UI
    app/                   App routes
    components/            Legal UI and reusable UI components
    hooks/                 Chat, upload, and settings hooks
    lib/                   Shared frontend types and sample data
  LegalKB_FAISS/           Local FAISS index files
  mini_dataset/            Small legal dataset used for demos/indexing
  models/                  Local model folders; large weights are not committed
  docs/                    Project documentation
```

## Quick Start

### 1. Backend

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open the API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Demo mode lets the backend start even when large model weights are missing.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

If your backend is not running on `http://127.0.0.1:8000`, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Required Model Files

Large model weights are intentionally not stored in Git. The current backend expects:

- `models/InLegalBERT/pytorch_model.bin` or `models/InLegalBERT/model.safetensors`
- `models/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf`

At the time of documentation, the repository contains configuration/tokenizer placeholders but may not contain the actual weights. See [docs/MODELS.md](docs/MODELS.md) for download commands and validation notes.

## API Contract

The frontend expects chat responses in this shape:

```json
{
  "answer": "string",
  "confidence": "high | medium | low",
  "sources": [
    {
      "id": "src-123",
      "title": "Retrieved Document",
      "citation": null,
      "jurisdiction": null,
      "year": null,
      "excerpt": "Source text used by the answer",
      "url": null,
      "type": "retrieved_chunk"
    }
  ]
}
```

The current FAISS index mostly stores raw text chunks, so the backend uses fallback metadata when richer citation fields are unavailable. See [docs/API.md](docs/API.md).

## Current MVP Decisions

- Authentication: not required for local MVP; production should add API key or user auth.
- CORS: `allow_origins=["*"]` is acceptable only for local development/demo.
- Chat history: frontend sends relevant conversation context with each request.
- Streaming: single JSON response only; SSE can be added later as `/chat/stream`.
- Source metadata: fallback source metadata is acceptable for MVP; richer metadata should be added during ingestion.

## Documentation

- [Setup Guide](docs/SETUP.md)
- [Model Setup](docs/MODELS.md)
- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Security Notes](docs/SECURITY.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Tech Stack

Backend:

- FastAPI
- Uvicorn
- Pydantic
- FAISS
- LangChain community vector store support
- Sentence Transformers / Transformers
- CTransformers for GGUF inference

Frontend:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Radix UI primitives
- Lucide icons

## License

License is not finalized in this repository. Add a `LICENSE` file before public release.

