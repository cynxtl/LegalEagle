# Development Guide

## Backend Commands

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Run backend:

```bash
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Check health:

```bash
curl http://127.0.0.1:8000/health
```

Send a chat request:

```bash
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"What is Article 21?\"}"
```

## Frontend Commands

```bash
cd frontend
npm install
npm run dev
npm run build
npm run lint
```

## Environment Variables

Backend variables use the `LEGALEAGLE_` prefix.

| Variable | Default | Purpose |
|---|---:|---|
| `LEGALEAGLE_HOST` | `0.0.0.0` | Backend bind host |
| `LEGALEAGLE_PORT` | `8000` | Backend port |
| `LEGALEAGLE_DEBUG` | `false` | Debug mode |
| `LEGALEAGLE_DEMO_MODE` | `false` | Mock/demo behavior when model weights are missing |
| `LEGALEAGLE_CORS_ORIGINS` | `["*"]` | Allowed CORS origins |
| `LEGALEAGLE_LLM_MAX_NEW_TOKENS` | `512` | Generation length |
| `LEGALEAGLE_LLM_TEMPERATURE` | `0.7` | Generation randomness |
| `LEGALEAGLE_RETRIEVAL_TOP_K` | `3` | Number of chunks retrieved |

Frontend:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## API Contract Rules

Keep these stable unless the frontend and backend are updated together:

- `POST /chat` request field: `message`
- Optional request fields: `category`, `chat_history`
- Response fields: `answer`, `sources`, `confidence`
- Source fields: `id`, `title`, `citation`, `jurisdiction`, `year`, `excerpt`, `url`, `type`

## Adding Rich Source Metadata

The current fallback source metadata is acceptable for MVP. A richer implementation should:

1. Update document ingestion to parse metadata.
2. Store metadata alongside FAISS documents.
3. Return metadata through `SourceResponse`.
4. Update frontend source cards only after the backend contract is stable.

Recommended metadata:

- title
- citation
- jurisdiction/court
- year
- source type
- source path or URL
- excerpt

## Code Review Focus

Review changes for:

- API contract compatibility
- model path handling
- graceful missing-model behavior
- upload validation and cleanup
- frontend error states
- legal disclaimer visibility
- accidental committed weights or private data

