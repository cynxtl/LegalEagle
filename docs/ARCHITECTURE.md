# Architecture

LegalEagle has two primary applications:

- FastAPI backend for retrieval and generation
- Next.js frontend for the user interface

## High-Level Flow

```text
User
  -> Next.js chat UI
  -> POST /chat
  -> FastAPI route
  -> RAG pipeline
  -> FAISS retriever
  -> local LLM generator
  -> structured JSON response
  -> frontend answer and source cards
```

## Backend

Entry point:

```text
backend/app/main.py
```

Responsibilities:

- Create the FastAPI app
- Configure CORS
- Validate model files at startup
- Initialize embedder, retriever, generator, and RAG pipeline
- Register API routes

Main route files:

```text
backend/app/routes/health.py
backend/app/routes/chat.py
backend/app/routes/upload.py
```

Core services:

```text
backend/app/services/rag/embedder.py
backend/app/services/rag/retriever.py
backend/app/services/rag/loader.py
backend/app/services/rag/pipeline.py
backend/app/services/llm/generator.py
```

## RAG Pipeline

The pipeline:

1. Receives the user message and optional chat history.
2. Retrieves relevant chunks from the FAISS vector store.
3. Builds a prompt context.
4. Sends context and question to the local generator.
5. Formats the answer, confidence, and sources.

## Frontend

Entry points:

```text
frontend/app/layout.tsx
frontend/app/page.tsx
frontend/app/(app)/chat/page.tsx
```

Important folders:

```text
frontend/components/legal/   Product-specific UI
frontend/components/ui/      Reusable UI primitives
frontend/hooks/              Client behavior and API calls
frontend/lib/                Shared types and data
```

The chat hook sends a stateless request to the backend and maps the response into frontend message objects.

## Data and Indexes

```text
LegalKB_FAISS/ipc_embed_db/index.faiss
LegalKB_FAISS/ipc_embed_db/index.pkl
mini_dataset/
```

The current source metadata is limited because the FAISS index stores mostly raw text chunks. Richer citations should be added during ingestion.

## Deployment Shape

For local development:

- Backend on `http://127.0.0.1:8000`
- Frontend on `http://localhost:3000`

For production:

- Restrict CORS origins.
- Add authentication.
- Store model files and indexes outside Git.
- Add structured logging and monitoring.
- Review legal safety and data privacy requirements.

