# LegalEagle v2 Frontend - Complete Guide

**Status**: ✅ **PRODUCTION READY**  
**Last Updated**: January 2025

A modern, full-stack legal research chatbot frontend with fixed sidebars, real-time chat, document upload, and full backend API integration.

---

## 📋 Quick Links

- 🚀 [Quick Start](#-quick-start)
- 🏗️ [Architecture](#-architecture)
- 🔌 [Backend Integration](#-backend-integration)
- 📁 [Project Structure](#-project-structure)
- 🎨 [Customization](#-customization)
- 📚 [Documentation](#-documentation-files)

---

## 🚀 Quick Start

### 1. Install & Run

```bash
cd frontend
npm install
npm run dev
```

Opens: **http://localhost:3000**

### 2. Configure Backend

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

### 3. Start Your Backend

Your backend must implement these endpoints:

```
POST   /api/chat                    # Send message
GET    /api/chat/threads            # Get history
POST   /api/documents/upload        # Upload file
GET    /api/documents               # List documents
GET    /api/settings                # Get settings
PUT    /api/settings                # Update settings
GET    /api/sources                 # List sources
```

See **API_RESPONSE_FORMAT.md** for exact response formats.

### 4. Test

1. Open http://localhost:3000/chat
2. Send a message
3. Should call your backend and display response

---

## 🏗️ Architecture

### Layout Structure

```
┌─────────────────────────────────────────────┐
│       Next.js 16 + React 19 + Tailwind 4   │
├─────────────────────────────────────────────┤
│                                             │
│  Fixed Sidebars + Responsive Main Content  │
│                                             │
│  ┌──────────┬──────────────────┬─────────┐ │
│  │ Sidebar  │  Main Content    │ Panel   │ │
│  │ (fixed)  │  (scrolls)       │(fixed)  │ │
│  │ scrolls  │  - Messages      │ scrolls │ │
│  │          │  - Input         │         │ │
│  │ - Nav    │  - Sources       │- Sources│ │
│  │ - Chat   │                  │- Acts   │ │
│  │ - Files  │                  │- Summary│ │
│  └──────────┴──────────────────┴─────────┘ │
│                                             │
│       ↓ HTTP API ↓                         │
│       Backend (Flask/Django/Node)          │
│                                             │
└─────────────────────────────────────────────┘
```

### Key Features

✅ **Fixed Sidebars**
- Left sidebar: 288px fixed, scrollable content
- Right panel: 360px fixed (desktop only), scrollable tabs
- Main content: Full-width with responsive margins
- Mobile: Sidebars hidden, content full-width

✅ **Chat Interface**
- Message list with timestamps
- User/assistant distinction
- Source citations as cards
- Confidence badges (high/medium/low)
- Expandable "view source" feature
- Sticky input bar at bottom
- File attachment button

✅ **Pages**
- Landing page (hero, features, testimonials)
- Chat page (main interface)
- Documents page (upload & management)
- Settings page (user preferences)
- Sources page (citation library)

✅ **Backend Ready**
- API client with all endpoints defined
- Error handling with fallback responses
- Environment-based configuration
- TypeScript for type safety
- Ready for immediate backend connection

---

## 🔌 Backend Integration

### Expected API Endpoints

Your backend should implement (see `API_RESPONSE_FORMAT.md` for examples):

#### Chat
```
POST /api/chat
{
  message: string
  category?: string
  threadId?: string
}
→ { id, content, confidence, sources }

GET /api/chat/threads
→ [{ id, title, category, updatedAt }]

GET /api/chat/threads/:id
→ { id, title, messages, ... }
```

#### Documents
```
POST /api/documents/upload
FormData: file, category
→ { id, name, size, uploadedAt, ... }

GET /api/documents
→ [{ id, name, size, category, ... }]

DELETE /api/documents/:id
→ { success: true }
```

#### Settings
```
GET /api/settings
→ { jurisdiction, language, aiModel, ... }

PUT /api/settings
{ jurisdiction, language, aiModel, ... }
→ { success: true }
```

#### Sources
```
GET /api/sources
→ [{ id, title, type, excerpt, ... }]

POST /api/sources/:id
→ { success: true, saved: true }

DELETE /api/sources/:id
→ { success: true, saved: false }
```

### Using the API Client

```typescript
import { apiClient } from "@/lib/api-client"

// Chat
await apiClient.chat.sendMessage("What is Section 420?", "Criminal")
await apiClient.chat.getThreads()

// Documents
await apiClient.documents.upload(file, "Property")
await apiClient.documents.list()

// Settings
await apiClient.settings.get()
await apiClient.settings.update({ jurisdiction: "Delhi" })

// Sources
await apiClient.sources.list()
await apiClient.sources.save("src-123")
```

---

## 📁 Project Structure

```
frontend/
├── app/
│   ├── page.tsx                      Landing page
│   ├── layout.tsx                    Root layout
│   ├── globals.css                   Global styles
│   └── (app)/                        App shell
│       ├── layout.tsx                Sidebar + main layout
│       ├── chat/
│       │   └── page.tsx              Chat interface
│       ├── documents/
│       │   └── page.tsx              Upload & files
│       ├── settings/
│       │   └── page.tsx              User settings
│       └── sources/
│           └── page.tsx              Citation library
│
├── components/
│   ├── legal/                        Custom components
│   │   ├── sidebar.tsx               Fixed left sidebar
│   │   ├── right-panel.tsx           Fixed right panel
│   │   ├── chat-message.tsx          Message with sources
│   │   ├── chat-input.tsx            Input bar
│   │   ├── source-card.tsx           Citation card
│   │   ├── confidence-badge.tsx      Confidence indicator
│   │   ├── disclaimer-banner.tsx     Legal disclaimer
│   │   ├── document-upload-card.tsx  Upload UI
│   │   ├── loading-skeleton.tsx      Loading state
│   │   ├── empty-state.tsx           Empty placeholder
│   │   ├── theme-toggle.tsx          Dark mode
│   │   ├── mobile-header.tsx         Mobile nav
│   │   └── logo.tsx                  App logo
│   │
│   └── ui/                           Shadcn UI (60+ components)
│       ├── button.tsx
│       ├── tabs.tsx
│       ├── input.tsx
│       └── ...
│
├── hooks/
│   ├── use-chat.ts                   Chat + API
│   ├── use-document-upload.ts        File upload
│   └── use-settings.ts               Settings persistence
│
├── lib/
│   ├── api-client.ts                 API client
│   ├── legal-data.ts                 Types & mock data
│   ├── utils.ts                      Helpers
│   └── cn.ts                         Tailwind merge
│
├── .env.example                      Environment template
├── .env.local                        Your config (CREATE THIS)
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## 🎨 Customization

### Change Backend URL
```bash
# .env.local
NEXT_PUBLIC_API_URL=https://your-api.com
```

### Add Authentication
`lib/api-client.ts`:
```typescript
const headers = {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`
}
```

### Customize Colors
`app/globals.css`:
```css
:root {
  --primary: 210 100% 50%;          /* Blue */
  --sidebar-bg: 224 71% 4%;         /* Dark slate */
  /* ... more variables ... */
}
```

### Modify Tailwind
`tailwind.config.ts`:
```typescript
module.exports = {
  theme: {
    extend: {
      colors: {
        // Your custom colors
      }
    }
  }
}
```

---

## 🧪 Testing

### Frontend Only (with Mock)
```bash
npm run dev
# Messages use fallback mock responses
```

### With Backend
```bash
# Terminal 1: Frontend
npm run dev

# Terminal 2: Backend
python app.py  # or your backend command

# Open http://localhost:3000/chat
```

### Test API Directly
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","category":"General"}'
```

---

## 📦 Deployment

### Build
```bash
npm run build
npm run start
```

### Vercel (Recommended)
```bash
npm install -g vercel
vercel --prod
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD npm run start
```

### Environment Variables (Prod)
Create `.env.production.local`:
```bash
NEXT_PUBLIC_API_URL=https://api.legaleagle.com
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| API error: 404 | Check backend running, verify URL in .env.local |
| Network error | Check CORS on backend, firewall settings |
| Mock response | Backend unavailable - start backend, check URL |
| Build fails | `npm install`, delete `node_modules/.next`, rebuild |
| Sidebar overlaps | Check `lg:ml-72` and `xl:mr-[360px]` classes |

---

## 📚 Documentation Files

| File | Contains |
|------|----------|
| `IMPLEMENTATION_COMPLETE.md` | Overview, setup, architecture |
| `SETUP_GUIDE.md` | Detailed installation & setup |
| `FRONTEND_BACKEND_INTEGRATION.md` | Backend integration guide |
| `API_RESPONSE_FORMAT.md` | API response examples |
| `QUICK_REFERENCE.md` | Developer cheat sheet |

---

## 📊 Component Reference

| Component | Purpose |
|-----------|---------|
| Sidebar | Fixed nav with chat history, theme toggle |
| RightPanel | Fixed sources/acts/summary tabs |
| ChatMessage | Message with confidence, sources |
| ChatInput | Textarea + send + file attach |
| SourceCard | Interactive citation card |
| ConfidenceBadge | High/medium/low indicator |
| DisclaimerBanner | Legal disclaimer |
| DocumentUploadCard | Drag-drop upload UI |
| LoadingSkeleton | Message loading animation |
| EmptyState | No results fallback |
| ThemeToggle | Dark/light mode switch |
| MobileHeader | Mobile navigation |

---

## 🎯 Development Workflow

1. **Setup**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure**
   - Create `.env.local` with backend URL
   - Start your backend

3. **Develop**
   ```bash
   npm run dev
   # Edit components in components/legal/
   # Styles in tailwind (TailwindCSS v4)
   ```

4. **Test**
   - Open http://localhost:3000
   - Test all pages and features
   - Check API calls in DevTools

5. **Build**
   ```bash
   npm run build
   npm run start
   ```

6. **Deploy**
   - Vercel: `vercel --prod`
   - Other: Use Docker or server deployment

---

## 🔐 Security

- Add CORS headers on backend
- Use HTTPS in production
- Validate all API responses
- Sanitize user inputs
- Use secure auth tokens
- Don't commit `.env.local`

---

## 📈 Performance

- Next.js 16 optimizations built-in
- Image optimization with next/image
- Code splitting automatic
- Static generation where possible
- API caching with SWR/React Query (optional)

---

## 🚀 Next Steps

1. ✅ Frontend is ready
2. 📋 Implement backend endpoints (see API_RESPONSE_FORMAT.md)
3. 🔗 Connect backend URL in `.env.local`
4. 🧪 Test each endpoint
5. 🎨 Customize styling/branding
6. 📦 Deploy to production

---

## 💡 Key Features

✨ **Modern Stack**
- Next.js 16 (React 19)
- Tailwind CSS v4 with OKLch colors
- TypeScript 5.7
- Shadcn/UI (60+ components)

✨ **Professional UI**
- Dark mode first
- Responsive design
- Accessible (WCAG)
- Smooth animations

✨ **Production Ready**
- Error handling
- Loading states
- Fallback responses
- Type safety

---

## 📞 Support

1. Check documentation files
2. Review code comments
3. Check browser console
4. Check backend logs
5. Verify API response format

---

**Built with ❤️ for legal professionals**

Next.js 16 • Tailwind CSS 4 • Shadcn/UI • TypeScript 5
