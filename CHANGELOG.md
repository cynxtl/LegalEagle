# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-01-15

### Added
- **New Next.js Frontend** 🎉
  - Modern, responsive chat interface with Next.js 16 and React 19
  - Fixed left sidebar (288px) with chat history and navigation
  - Fixed right panel (360px, desktop only) with sources and citations
  - Dark mode support with theme toggle
  - Invisible scrollbars for clean UI
  - Mobile responsive design
  - Document upload interface
  - Settings page for user preferences
  - Source citation management

### Features
- Chat interface with real-time message display
- Support for user and assistant messages
- Source citations with expandable details
- Confidence badges (high/medium/low)
- Loading states and error handling
- Sticky input bar with send button and file attachment
- Auto-scroll to latest message
- Message history display
- Category tags for legal topics

### Technical Stack
- Next.js 16 (React framework)
- React 19 (UI library)
- Tailwind CSS v4 (styling with OKLch colors)
- TypeScript 5.7 (type safety)
- Shadcn/UI (60+ reusable components)
- Lucide React (icons)

### UI Improvements
- Professional legal-tech design
- Neutral color palette with blue accents
- Rounded cards (rounded-xl/2xl) with subtle shadows
- Proper spacing and typography
- Accessibility features (semantic HTML, ARIA labels)

### Developer Experience
- Full TypeScript support
- Well-organized component structure
- Custom hooks for state management (useChat, useSettings, useDocumentUpload)
- Reusable UI components
- Clean, modular codebase
- Tailwind CSS for rapid development

### Configuration
- Environment-based setup
- Dark mode configuration (class-based)
- Next.js 16 optimizations
- Turbopack support for fast builds

### Pages
- `/` - Landing page with hero, features, and testimonials
- `/chat` - Main chat interface
- `/documents` - Document upload and management
- `/settings` - User preferences
- `/sources` - Citation library

### Documentation
- Comprehensive README with setup instructions
- Code comments for clarity
- Component documentation

---

## [0.1.0] - Initial Release

### Added
- Backend chatbot with Streamlit UI
- FAISS vector search
- Indian legal knowledge base
- Document upload and analysis
- Multi-turn conversations
