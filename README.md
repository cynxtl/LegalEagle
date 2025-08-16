# LegalEagle: Indian Law Document & Query Chatbot

A powerful, privacy-focused chatbot that helps you understand Indian legal documents and law. Runs fully locally—no cloud APIs required.

## Features

- Upload and analyze PDF/DOCX legal documents
- Interactive chat interface for Indian law (statutes, Q&A, case law)
- Local AI-powered analysis (no internet needed after setup)
- Specialized for Indian law: statutes, Q&A, legal dictionary
- Memory of previous conversations
- Fast semantic search using FAISS

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download required models (see below)

## Hardware Requirements

- 16GB+ RAM recommended
- NVIDIA GPU with 8GB+ VRAM (recommended for speed)
- ~20GB free disk space for models and index

## Usage

1. Run the app:
   ```bash
   streamlit run app.py
   ```
2. Upload your legal documents (PDF/DOCX) in the UI
3. Ask questions about Indian law, statutes, or your uploaded docs

## Data & Models

- Minimal Indian legal datasets in `mini_dataset/`
- Legal knowledge base index in `LegalKB_FAISS/ipc_embed_db/`
- Local models required in `models/`:
  - `InLegalBERT` (for embeddings)
  - `Mistral-7B-Instruct-v0.2-GGUF` (for text generation)

> **Note:** Large model files are not included in the repo. Download instructions are provided in the `models/` directory or see project wiki.

## Example Questions

- What is Article 21 of the Indian Constitution?
- How do I file a complaint against my employer in India?
- What is Section 420 IPC?
- What is habeas corpus?
- Paste a clause from a contract for analysis

## Technical Stack
- Streamlit (UI)
- LangChain (reasoning, chains)
- FAISS (vector search)
- InLegalBERT (embeddings)
- Mistral-7B (LLM)

## Disclaimer
This chatbot is for informational purposes only and does not constitute legal advice. Always consult a qualified legal professional for specific legal matters.