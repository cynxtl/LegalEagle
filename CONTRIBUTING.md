# Project Guide

## Directory Structure

```
Law.ai/
├── frontend/                    # Next.js 16 React frontend (NEW!)
│   ├── app/
│   │   ├── page.tsx            # Landing page
│   │   ├── layout.tsx          # Root layout
│   │   ├── globals.css         # Global styles (includes scrollbar hiding)
│   │   └── (app)/              # App shell with sidebars
│   │       ├── layout.tsx      # Sidebar + main layout
│   │       ├── chat/           # Chat page
│   │       ├── documents/      # Document upload
│   │       ├── settings/       # User settings
│   │       └── sources/        # Citation library
│   │
│   ├── components/
│   │   ├── legal/              # Custom legal components
│   │   │   ├── sidebar.tsx
│   │   │   ├── right-panel.tsx
│   │   │   ├── chat-message.tsx
│   │   │   ├── chat-input.tsx
│   │   │   └── ... (more components)
│   │   └── ui/                 # Shadcn UI components (60+)
│   │
│   ├── hooks/
│   │   ├── use-chat.ts
│   │   ├── use-document-upload.ts
│   │   └── use-settings.ts
│   │
│   ├── lib/
│   │   ├── legal-data.ts       # Types and mock data
│   │   ├── utils.ts            # Utilities
│   │   └── cn.ts               # Tailwind merge
│   │
│   ├── public/                 # Static assets
│   ├── styles/                 # Additional styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.mjs
│   └── postcss.config.mjs
│
├── app.py                       # Backend Streamlit app
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
├── .gitignore                   # Git configuration
└── models/                      # AI models (not in repo)
    └── ... (download separately)
```

## Getting Started

### Frontend
```bash
cd frontend
npm install
npm run dev
# Opens http://localhost:3000
```

### Backend
```bash
pip install -r requirements.txt
streamlit run app.py
# Opens http://localhost:8501
```

## Key Features

### Frontend UI
- ✅ Modern Next.js 16 interface
- ✅ Fixed sidebars with scrollable content
- ✅ Dark mode support
- ✅ Mobile responsive
- ✅ Invisible scrollbars
- ✅ TypeScript for type safety
- ✅ Tailwind CSS styling

### Backend
- Chat with context awareness
- Document analysis
- FAISS vector search
- Indian legal knowledge base

## Development

### Code Style
- Use TypeScript for all frontend code
- Components in `components/legal/`
- Styles using Tailwind CSS classes
- Reusable hooks in `hooks/`

### Adding New Pages
1. Create in `app/(app)/[page]/page.tsx`
2. Update sidebar navigation in `components/legal/sidebar.tsx`
3. Add to types in `lib/legal-data.ts`

### Adding New Components
1. Create in `components/legal/[component].tsx`
2. Export from component files
3. Use in pages
4. Document with JSDoc comments

## Deployment

### Frontend (Vercel)
```bash
vercel --prod
```

### Backend (Your Server)
```bash
python app.py
# Or use systemd/supervisor for production
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

MIT - See LICENSE file

## Contact

For questions, issues, or feature requests, open a GitHub issue.

---

**Made with ❤️ for legal professionals**
