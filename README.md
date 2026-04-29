# LegalEagle: Indian Law Document & Query Chatbot

A powerful, privacy-focused chatbot that helps you understand Indian legal documents and law. Runs fully locally—no cloud APIs required.

**Now with a modern Next.js frontend UI!** 🎉

## Features

- 🎨 **Modern Next.js Frontend** - Beautiful, responsive chat interface with fixed sidebars
- 📄 Upload and analyze PDF/DOCX legal documents
- 💬 Interactive chat interface for Indian law (statutes, Q&A, case law)
- 🔍 Fast semantic search using FAISS
- 💾 Memory of previous conversations
- 🏛️ Specialized for Indian law: statutes, Q&A, legal dictionary
- 🔒 Local AI-powered analysis (no internet needed after setup)

## Project Structure

```
Law.ai/
├── frontend/                 # Next.js 16 React frontend (NEW!)
│   ├── app/                 # Pages (chat, documents, settings)
│   ├── components/          # Reusable UI components
│   ├── hooks/              # React hooks (useChat, etc.)
│   ├── lib/                # Utilities and types
│   ├── public/             # Static assets
│   └── styles/             # Tailwind CSS
├── app.py                   # Streamlit backend
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Quick Start

### Backend Setup (Streamlit)

1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd Law.ai
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download required models (see `models/` directory)

4. Run the app:
   ```bash
   streamlit run app.py
   ```

### Frontend Setup (Next.js)

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

4. Open http://localhost:3000 in your browser

## Hardware Requirements

- 16GB+ RAM recommended
- NVIDIA GPU with 8GB+ VRAM (recommended for speed)
- ~20GB free disk space for models and index

## Features in Detail

### Frontend (Next.js)
- ✅ Fixed left sidebar with chat history navigation
- ✅ Fixed right panel with sources and citations (desktop)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Dark mode support
- ✅ Document upload interface
- ✅ Settings page for user preferences
- ✅ Invisible scrollbars for clean UI
- ✅ Real-time chat with typing indicators

### Backend (Streamlit)
- Legal document analysis and Q&A
- Semantic search with FAISS
- Multi-turn conversations
- Document upload and indexing

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

### Backend
- Streamlit (UI)
- LangChain (reasoning, chains)
- FAISS (vector search)
- InLegalBERT (embeddings)

### Frontend
- Next.js 16 (React framework)
- React 19 (UI library)
- Tailwind CSS v4 (styling)
- TypeScript 5.7 (type safety)
- Shadcn/UI (components)

## Roadmap

- [ ] Backend API integration
- [ ] Authentication & user accounts
- [ ] Multi-language support
- [ ] Export to PDF/Word
- [ ] Collaboration features
- [ ] Mobile app (React Native)

## Contributing

Pull requests are welcome! Please ensure:
1. Code is well-typed (TypeScript)
2. Components are reusable
3. Styling uses Tailwind CSS
4. Documentation is updated

## License

MIT License - see LICENSE file for details

## Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Made with ❤️ for legal professionals in India**
- Mistral-7B (LLM)

## Disclaimer
This chatbot is for informational purposes only and does not constitute legal advice. Always consult a qualified legal professional for specific legal matters.