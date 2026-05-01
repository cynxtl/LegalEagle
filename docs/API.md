# API Reference

Base URL for local development:

```text
http://127.0.0.1:8000
```

Interactive docs:

```text
http://127.0.0.1:8000/docs
```

## Health

```http
GET /health
```

Example response:

```json
{
  "status": "degraded",
  "models_loaded": false,
  "faiss_index_loaded": true,
  "demo_mode": true,
  "version": "2.0.0",
  "missing_models": ["InLegalBERT model weights", "Mistral-7B GGUF weights"]
}
```

## Chat

```http
POST /chat
Content-Type: application/json
```

Request:

```json
{
  "message": "What is Section 420 IPC?",
  "category": "Criminal Law",
  "chat_history": [
    {
      "role": "user",
      "content": "Explain cheating under IPC."
    }
  ]
}
```

Response:

```json
{
  "answer": "Generated answer text.",
  "sources": [
    {
      "id": "src-12345678",
      "title": "Indian Penal Code Reference",
      "citation": null,
      "jurisdiction": null,
      "year": null,
      "excerpt": "Retrieved source text.",
      "url": null,
      "type": "statute"
    }
  ],
  "confidence": "medium"
}
```

## Upload

```http
POST /upload
Content-Type: multipart/form-data
```

Supported files:

- PDF
- DOCX
- TXT

Maximum size:

```text
25 MB
```

Example:

```bash
curl -X POST http://127.0.0.1:8000/upload -F "file=@document.pdf"
```

Response:

```json
{
  "id": "doc-abc123",
  "name": "document.pdf",
  "size": "1.2 MB",
  "pages": 10,
  "status": "indexed",
  "message": "Document 'document.pdf' processed: 12 chunks indexed."
}
```

## API Contract Decisions

- The backend is stateless for chat history.
- The frontend sends prior context in `chat_history`.
- Responses are single JSON payloads.
- SSE streaming is a future enhancement.
- Source metadata may be partial for MVP.

## Source Metadata

The desired frontend source object is:

```ts
type Source = {
  id: string
  title: string
  citation?: string | null
  jurisdiction?: string | null
  year?: number | null
  excerpt: string
  url?: string | null
  type: "case" | "statute" | "regulation" | "commentary" | "retrieved_chunk"
}
```

Current FAISS retrieval may only provide raw chunks. In that case, the backend returns fallback metadata:

```json
{
  "title": "Retrieved Document",
  "citation": null,
  "jurisdiction": null,
  "year": null,
  "excerpt": "retrieved text",
  "type": "retrieved_chunk"
}
```

