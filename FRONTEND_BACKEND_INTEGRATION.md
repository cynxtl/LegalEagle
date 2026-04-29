# Backend Integration Guide - LegalEagle v2 Frontend

## Quick Start

### 1. Configure API URL
Create a `.env.local` file in `/frontend`:
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

For production, update with your backend domain:
```
NEXT_PUBLIC_API_URL=https://api.legaleagle.com
```

### 2. API Client
The API client is in `lib/api-client.ts`. It provides:
- Structured fetch calls with error handling
- Type-safe API endpoints
- Automatic JSON encoding/decoding
- Error state management

### 3. Architecture

#### Fixed Sidebars
- **Left Sidebar**: `components/legal/sidebar.tsx`
  - `position: fixed` on desktop (lg breakpoint)
  - Scrollable content area
  - Main layout margin: `lg:ml-72`

- **Right Panel**: `components/legal/right-panel.tsx`
  - `position: fixed` on desktop (xl breakpoint)
  - Scrollable tabs (sources, acts, summary)
  - Main content margin: `xl:mr-[360px]`

#### State Management
All pages use custom hooks for API integration:
- `hooks/use-chat.ts` - Chat message handling
- `hooks/use-document-upload.ts` - File upload
- `hooks/use-settings.ts` - Settings persistence

---

## API Endpoints Expected

Your backend should implement these endpoints:

### Chat API
```
POST /api/chat
Request: { message: string, category: string, threadId?: string }
Response: { 
  id: string
  content: string
  confidence: "high" | "medium" | "low"
  sources: Source[]
  answer?: string
}

GET /api/chat/threads
Response: Thread[]

GET /api/chat/threads/:id
Response: Thread
```

### Documents API
```
POST /api/documents/upload
Body: FormData { file: File, category: string }
Response: { 
  id: string
  name: string
  size: number
  uploadedAt: string
  category: string
}

GET /api/documents
Response: UploadedDoc[]

DELETE /api/documents/:id
Response: { success: boolean }
```

### Settings API
```
GET /api/settings
Response: {
  jurisdiction: string
  language: string
  aiModel: string
  privacyMode: boolean
  notificationsEnabled: boolean
}

PUT /api/settings
Body: { ...settings }
Response: { success: boolean }
```

### Sources API
```
GET /api/sources
Response: Source[]

POST /api/sources/:id
Response: { success: boolean }

DELETE /api/sources/:id
Response: { success: boolean }
```

---

## Usage Examples

### Making API Calls
```typescript
// Use the apiClient from lib/api-client.ts
import { apiClient } from "@/lib/api-client"

// Chat
const response = await apiClient.chat.sendMessage(
  "What is Section 420 IPC?",
  "Criminal"
)

// Documents
const uploadResult = await apiClient.documents.upload(file, "Property")

// Settings
const settings = await apiClient.settings.get()
```

### In Components
```typescript
"use client"

import { useChat } from "@/hooks/use-chat"

export default function ChatPage() {
  const chat = useChat()
  
  const handleSend = async (message: string) => {
    await chat.sendMessage(message, "Property")
  }
  
  return (
    <div>
      {chat.messages.map(m => <Message key={m.id} message={m} />)}
      <ChatInput onSubmit={handleSend} />
    </div>
  )
}
```

---

## Fallback Behavior

If your backend is unavailable, the frontend will:
1. Try to connect to the API endpoint
2. Log a warning
3. Display a mock response

This ensures development continues even without a running backend.

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:5000` |

---

## Type Definitions

Key types from `lib/legal-data.ts`:

```typescript
interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: string
  confidence?: "high" | "medium" | "low"
  category?: string
  sources?: Source[]
}

interface Source {
  id: string
  title: string
  excerpt: string
  type: "act" | "case" | "article"
  jurisdiction: string
  year?: number
  confidence?: number
}

interface Thread {
  id: string
  title: string
  category: string
  updatedAt: string
}

interface UploadedDoc {
  id: string
  name: string
  size: number
  uploadedAt: string
  category: string
  status?: "pending" | "processing" | "ready"
}
```

---

## Testing API Integration

1. **Development**: `npm run dev` (Next.js dev server on 3000)
2. **API Server**: Run your backend on port 5000 (or update `.env.local`)
3. **Test Messages**: Send messages in the chat - they'll call your backend
4. **Check Logs**: Browser console shows API calls and responses

---

## Troubleshooting

### "API error: 404"
- Check backend is running
- Verify endpoint path matches
- Check `NEXT_PUBLIC_API_URL` environment variable

### "Network error"
- Check CORS headers on backend (allow origin)
- Verify API URL in `.env.local`
- Check backend logs for request details

### "Fallback response shown"
- Backend unavailable but frontend continues
- Check backend is running and accessible
- Verify API endpoint implements the expected format

---

## Next Steps

1. ✅ Frontend is ready with fixed sidebars
2. ✅ API client skeleton in place
3. 📋 Implement your backend endpoints
4. 🔗 Test each endpoint with the API client
5. 🎨 Customize response handling as needed

Happy building! 🚀
