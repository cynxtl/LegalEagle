# LegalEagle Backend

The backend is a FastAPI service for local Indian legal research. It exposes health, chat, and document upload endpoints, then coordinates retrieval from FAISS with local LLM generation.

## Structure

```text
backend/
  app/
    main.py              FastAPI app, startup lifecycle, CORS
    routes/
      chat.py            POST /chat
      upload.py          POST /upload
      health.py          GET /health
    services/
      rag/
        embedder.py      InLegalBERT embeddings
        retriever.py     FAISS vector store access
        loader.py        PDF/DOCX/TXT extraction and chunking
        pipeline.py      RAG orchestration
      llm/
        generator.py     Mistral GGUF generation wrapper
    models/
      schemas.py         Pydantic request and response models
    core/
      config.py          Settings and model validation
```

## Run Locally

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Model Files

Full model mode requires:

```text
models/InLegalBERT/pytorch_model.bin
models/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Use demo mode while those files are missing:

```bash
set LEGALEAGLE_DEMO_MODE=true
```

See [../docs/MODELS.md](../docs/MODELS.md).

## Endpoints

- `GET /health`: backend readiness, model status, missing model diagnostics
- `POST /chat`: legal question in, answer and sources out
- `POST /upload`: upload PDF, DOCX, or TXT for indexing
- `GET /docs`: FastAPI Swagger documentation

## API Contract

The backend should always return frontend-compatible chat responses:

```json
{
  "answer": "string",
  "confidence": "high | medium | low",
  "sources": []
}
```

Sources may use fallback metadata until richer ingestion is implemented.

