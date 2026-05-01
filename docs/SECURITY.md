# Security Notes

LegalEagle is currently configured for local MVP development. It is not production-hardened yet.

## Current MVP Position

- Authentication is not enabled.
- CORS may allow all origins.
- Chat history is supplied by the frontend, not persisted by the server.
- Uploaded documents are processed locally and temporary files are removed after indexing.
- Large model files are local and should not be committed.

## Before Production

Add:

- Authentication for chat and upload endpoints
- Restricted CORS origins
- Request size and rate limits
- Structured audit logging
- Safer upload scanning and file validation
- Per-user data separation
- Retention policy for uploaded documents and indexed chunks
- Secrets management
- HTTPS termination

## Sensitive Data

Do not commit:

- legal client documents
- private case files
- model weights
- `.env` files
- access tokens
- API keys
- generated indexes containing confidential documents

## Responsible Use

LegalEagle output should remain informational. The product must not imply that generated answers replace a qualified lawyer or professional legal advice.

