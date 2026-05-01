# Contributing to LegalEagle

Thanks for improving LegalEagle. This project is still MVP-stage, so contributions should prioritize correctness, clear contracts, reproducibility, and safe handling of legal information.

## Development Principles

- Keep the backend and frontend API contract aligned.
- Do not commit model weights, private legal documents, secrets, or personal data.
- Prefer small, reviewable pull requests.
- Add or update documentation when behavior changes.
- Treat all generated legal answers as informational, not legal advice.

## Local Setup

Backend:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

See [docs/SETUP.md](docs/SETUP.md) and [docs/MODELS.md](docs/MODELS.md) for full setup details.

## Branches and Commits

Use focused branches:

```bash
git checkout -b feature/source-metadata
git checkout -b fix/model-validation
git checkout -b docs/api-contract
```

Commit messages should be short and specific:

```text
docs: add model setup guide
fix: return frontend-compatible source metadata
feat: add upload validation errors
```

## Backend Guidelines

- Keep routes thin; place retrieval/generation logic in services.
- Maintain Pydantic schemas in `backend/app/models/schemas.py`.
- Return stable JSON contracts even when optional metadata is missing.
- Use `LEGALEAGLE_DEMO_MODE=true` for development without model weights.
- Add clear startup diagnostics for missing model files.

## Frontend Guidelines

- Keep shared types in `frontend/lib/legal-data.ts`.
- Keep reusable app components in `frontend/components/legal/`.
- Use the existing UI component and styling patterns.
- Avoid assuming all source metadata is present; citation, jurisdiction, and year may be null or empty.
- Keep chat state client-owned for the MVP.

## Testing Checklist

Before opening a pull request:

- Backend starts in demo mode.
- `GET /health` returns a valid response.
- `POST /chat` returns `answer`, `confidence`, and `sources`.
- Frontend builds or runs locally.
- Chat UI handles backend errors cleanly.
- Documentation reflects any setup or contract change.

Useful commands:

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
curl http://127.0.0.1:8000/health
cd frontend
npm run build
npm run lint
```

## Pull Request Checklist

- Describe the change and why it is needed.
- Mention affected areas: backend, frontend, docs, models, data, or API.
- Include screenshots for UI changes.
- Include sample request/response for API changes.
- Confirm no model weights or private documents are committed.

## Legal and Safety Notes

LegalEagle must always communicate that generated output is informational. Do not remove disclaimers, and avoid wording that presents the system as a replacement for a qualified lawyer.

