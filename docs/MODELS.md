# Model Setup

LegalEagle is designed to run with local models. Large model weights are not committed to GitHub.

## Required Files

The backend validates these paths at startup:

```text
models/InLegalBERT/
  config.json
  tokenizer_config.json
  special_tokens_map.json
  vocab.txt
  pytorch_model.bin       required, or model.safetensors

models/Mistral-7B-Instruct-v0.2-GGUF/
  config.json
  mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

Current repository note:

- The Mistral folder may contain only `config.json` and `.placeholder`.
- The InLegalBERT folder may contain tokenizer/config files but not `pytorch_model.bin`.
- If weights are absent locally, full model mode will not be available.

## Download InLegalBERT

```bash
huggingface-cli download law-ai/InLegalBERT --local-dir models/InLegalBERT
```

The backend accepts either:

```text
models/InLegalBERT/pytorch_model.bin
models/InLegalBERT/model.safetensors
```

## Download Mistral GGUF

```bash
huggingface-cli download TheBloke/Mistral-7B-Instruct-v0.2-GGUF mistral-7b-instruct-v0.2.Q4_K_M.gguf --local-dir models/Mistral-7B-Instruct-v0.2-GGUF
```

Expected file:

```text
models/Mistral-7B-Instruct-v0.2-GGUF/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

## Demo Mode

Use demo mode when the real model files are missing:

```bash
set LEGALEAGLE_DEMO_MODE=true
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

Demo mode is useful for frontend development and API contract testing.

## Git Policy

Do not commit:

- `.gguf`
- `.bin`
- `.safetensors`
- `.pt`
- `.pth`
- private model caches

The `.gitignore` is intended to keep these files out of version control.

