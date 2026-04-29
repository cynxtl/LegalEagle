# LegalEagle v2 - Fixed Sidebars & Backend Integration Setup

## ✅ What's Done

### 1. **Fixed Sidebars Architecture**

#### Left Sidebar (Desktop)
- ✅ Position: `fixed` with `left-0 top-0`
- ✅ Size: `w-72` (288px) fixed width
- ✅ Content: Scrollable with `overflow-y-auto`
- ✅ Layout margin: Main content has `lg:ml-72`
- ✅ Responsive: Hidden on mobile, visible on `lg` breakpoint

#### Right Panel (Desktop)
- ✅ Position: `fixed` with `right-0 top-0`
- ✅ Size: `w-[360px]` (360px) fixed width
- ✅ Content: Scrollable tabs with `overflow-y-auto`
- ✅ Layout margin: Main content has `xl:mr-[360px]`
- ✅ Responsive: Hidden on mobile, visible on `xl` breakpoint

### 2. **Backend API Integration**

#### API Client (`lib/api-client.ts`)
```typescript
// Provides structured API calls:
apiClient.chat.sendMessage(message, category)
apiClient.documents.upload(file, category)
apiClient.settings.get() / .update()
apiClient.sources.list() / .save() / .unsave()
```

#### Configuration
- Backend URL: `NEXT_PUBLIC_API_URL` environment variable
- Default: `http://localhost:5000`
- Fallback: Mock responses if backend unavailable

#### Error Handling
- Try/catch blocks in all API calls
- Fallback to mock data for development
- User-friendly error messages

---

## 🚀 Quick Start

### Step 1: Set Environment Variables

Create `.env.local` in `/frontend`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
```

For production:
```bash
NEXT_PUBLIC_API_URL=https://api.legaleagle.com
```

### Step 2: Start Frontend

```bash
cd frontend
npm run dev
```

Server runs on: **http://localhost:3000**

### Step 3: Start Backend

Your backend should run on port 5000 (or update `.env.local`):
```bash
# Example Python backend
python app.py  # Should start on port 5000
```

### Step 4: Test Integration

1. Open http://localhost:3000/chat
2. Send a message
3. Check browser console for API logs
4. Backend should receive request

---

## 📁 File Changes Summary

### Layout & Positioning
| File | Changes |
|------|---------|
| `app/(app)/layout.tsx` | Added `lg:ml-72` to main content |
| `components/legal/sidebar.tsx` | Added `fixed left-0 top-0` positioning |
| `components/legal/right-panel.tsx` | Added `fixed right-0 top-0` positioning, reorganized scrollable content |
| `app/(app)/chat/page.tsx` | Added `xl:mr-[360px]` to main content |

### API Integration
| File | Changes |
|------|---------|
| `lib/api-client.ts` | **NEW** - Full API client with structured endpoints |
| `hooks/use-chat.ts` | Updated to call real `apiClient.chat.sendMessage()` |
| `.env.example` | **NEW** - Environment variable template |

### Documentation
| File | Purpose |
|------|---------|
| `FRONTEND_BACKEND_INTEGRATION.md` | Complete backend integration guide |

---

## 🔌 Backend API Specifications

Your backend should implement these endpoints:

### POST /api/chat
Send a chat message and get an AI response.

**Request:**
```json
{
  "message": "What is Section 420 IPC?",
  "category": "Criminal",
  "threadId": "thread-123" // optional
}
```

**Response:**
```json
{
  "id": "msg-456",
  "content": "Section 420 IPC covers cheating and dishonestly inducing delivery of property...",
  "confidence": "high",
  "sources": [
    {
      "id": "src-1",
      "title": "Section 420 IPC",
      "excerpt": "Whoever by deceiving any person...",
      "type": "act",
      "jurisdiction": "India",
      "year": 1860
    }
  ]
}
```

### GET /api/chat/threads
Get list of recent threads.

**Response:**
```json
[
  {
    "id": "thread-1",
    "title": "Tenant rights under Rent Control Act",
    "category": "Property",
    "updatedAt": "2 min ago"
  }
]
```

### POST /api/documents/upload
Upload a legal document.

**Request:** FormData with `file` and `category`
```
file: File object
category: "Property" | "Criminal" | "Corporate" etc.
```

**Response:**
```json
{
  "id": "doc-123",
  "name": "lease_agreement.pdf",
  "size": 245678,
  "uploadedAt": "2024-01-15T10:30:00Z",
  "category": "Property",
  "status": "ready"
}
```

### GET /api/settings
Get user settings.

**Response:**
```json
{
  "jurisdiction": "India",
  "language": "English",
  "aiModel": "gpt-4",
  "privacyMode": false,
  "notificationsEnabled": true
}
```

### PUT /api/settings
Update user settings.

**Request:** Same as GET response

**Response:**
```json
{ "success": true }
```

---

## 🧪 Testing

### Manual Testing
1. **Chat**: Send messages, verify responses in right panel
2. **Upload**: Drag files, check documents page
3. **Settings**: Change preferences, verify they persist
4. **Sidebars**: Scroll content independently from main area

### API Testing
Use curl or Postman:
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello","category":"General"}'
```

### Browser Devtools
- Network tab: Check API calls
- Console: See error logs
- Application > Storage > Local Storage: Check persisted settings

---

## 📝 Common Issues & Solutions

### Issue: "Can't resolve 'tw-animate-css'"
**Solution**: Already fixed - removed from `globals.css`

### Issue: "API error: 404"
**Solution**: Check backend is running on correct port
```bash
# Start backend
cd .. && python app.py
```

### Issue: "Network error"
**Solution**: Check CORS headers in backend
```python
# Flask example
from flask_cors import CORS
CORS(app)
```

### Issue: Fallback response showing
**Solution**: Backend is unreachable
1. Verify backend is running
2. Check `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check browser console for actual error

---

## 🎯 Next Steps

1. **Implement Backend Endpoints**
   - Implement all endpoints in `FRONTEND_BACKEND_INTEGRATION.md`
   - Ensure responses match expected format

2. **Connect Your API URL**
   - Update `NEXT_PUBLIC_API_URL` in `.env.local`
   - Test each endpoint

3. **Add Authentication** (if needed)
   - Update `lib/api-client.ts` to include auth headers
   - Store tokens in secure cookies

4. **Deploy Frontend**
   - Update production URL in `.env.production.local`
   - Deploy to Vercel: `vercel --prod`

5. **Deploy Backend**
   - Deploy to your server/cloud
   - Update frontend API URL

---

## 💡 Key Features Implemented

✅ **Fixed Sidebars**
- Left sidebar: 288px fixed width, scrollable content
- Right panel: 360px fixed width, scrollable tabs
- Main content: Responsive margins accounting for fixed sidebars
- Mobile: Sidebars hidden, only appear on lg/xl breakpoints

✅ **Backend API Client**
- Structured endpoints for all operations
- Error handling with fallback
- Environment-based configuration
- Type-safe request/response

✅ **State Management**
- useChat hook integrates with API
- useDocumentUpload hook ready for file uploads
- useSettings hook for persistence

✅ **Error Recovery**
- Graceful fallback to mock data
- User-friendly error messages
- Console logging for debugging

---

## 📚 Additional Resources

- Frontend guide: See `FRONTEND_BACKEND_INTEGRATION.md`
- Component reference: Check `components/legal/`
- Type definitions: See `lib/legal-data.ts`
- Hooks: See `hooks/` directory

---

## Questions?

Review the code comments in:
- `lib/api-client.ts` - API setup
- `hooks/use-chat.ts` - Chat integration
- `components/legal/sidebar.tsx` - Sidebar layout
- `components/legal/right-panel.tsx` - Right panel layout

Happy coding! 🎉
