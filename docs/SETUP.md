# Setup Guide

This guide explains how to run LegalEagle locally.

## Requirements

- Windows PowerShell or a compatible shell
- Python 3.10+
- Node.js 20+ recommended
- npm
- 8 GB RAM minimum for demo mode
- More RAM and disk space for full local model inference

## Backend Setup

From the repository root:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

Start in demo mode:

```bash
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Demo mode is recommended for first-time setup because the large model files are not committed.

Health check:

```bash
curl http://127.0.0.1:8000/health
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

The frontend defaults to:

```text
http://127.0.0.1:8000
```

To override it, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## Full Model Mode

To run with real local models:

1. Download InLegalBERT files.
2. Download the Mistral GGUF file.
3. Keep `LEGALEAGLE_DEMO_MODE` unset or set to `false`.
4. Start the backend.

See [MODELS.md](MODELS.md).

## Common Problems

### Backend reports missing models

This is expected if the large weight files have not been downloaded. Use demo mode or download the files listed in [MODELS.md](MODELS.md).

### Chat returns 503

The RAG pipeline did not initialize. Check:

- `GET /health`
- backend startup logs
- model file paths
- FAISS index availability

### Frontend cannot reach backend

Check:

- Backend is running on port `8000`.
- `NEXT_PUBLIC_API_URL` points to the backend.
- CORS is enabled for local development.

