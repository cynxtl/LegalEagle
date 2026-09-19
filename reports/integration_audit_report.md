# LegalEagle v2 — Frontend-Backend Integration Audit Report (Phase 2)

**Date**: September 18, 2026  
**Auditor**: Staff Backend & Full Stack Engineer  
**Scope**: Verification of API Contracts, Route Mappings, and Frontend Hooks  
**Backend Host**: `http://127.0.0.1:8000` (FastAPI 2.0.0, Uvicorn)

---

## 1. Executive Summary

This integration audit cross-referenced every frontend user action against backend API implementations, route paths, payload structures, response mapping, and error handling.

**Integration Status Overview**:
- Total Frontend Action Endpoints Evaluated: **12**
- Fully Integrated & Operational: **8** (67%)
- Disconnected or Missing Handlers: **4** (33%)

---

## 2. API Contract & Integration Matrix

| Frontend Action | Hook / Component | HTTP Method & Path | Backend Router | Status | Gap / Disconnect Description |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **Send Legal Query** | `use-chat.ts: sendMessage()` | `POST /chat` | `chat.py` | ✅ Connected | Request `{message, category, thread_id}` correctly invokes RAG and stores to SQLite. |
| **Load Consultation History** | `use-chat.ts: loadThread()` | `GET /api/v1/threads/{id}` | `threads.py` | ✅ Connected | Fetches thread with full message array, sources, and confidence metadata. |
| **List Recent Consultations** | `sidebar.tsx: fetchThreads()` | `GET /api/v1/threads` | `threads.py` | ✅ Connected | Returns thread summaries, message counts, and previews ordered by `updated_at`. |
| **Delete Consultation** | `sidebar.tsx: handleDeleteThread()` | `DELETE /api/v1/threads/{id}` | `threads.py` | ✅ Connected | Deletes thread cascade in SQLite; removes thread from sidebar list. |
| **Rename Consultation** | `sidebar.tsx` | `PATCH /api/v1/threads/{id}` | `threads.py` | ❌ **Missing** | **Backend route does not exist.** Frontend lacks UI control and API call to update thread titles. |
| **Upload Legal Document** | `use-document-upload.ts: uploadFile()` | `POST /upload` | `upload.py` | ⚠️ **Disconnected** | Backend endpoint works via multipart `file`, but `DocumentUploadCard` `<input>` lacks `onChange` event trigger! |
| **List Indexed Documents** | `use-document-upload.ts: fetchDocuments()` | `GET /api/v1/documents` | `documents.py` | ✅ Connected | Returns all uploaded documents with size, status, and chunk count. |
| **Delete Indexed Document** | `use-document-upload.ts: removeFile()` | `DELETE /api/v1/documents/{id}` | `documents.py` | ✅ Connected | Deletes document record from SQLite and updates UI list. |
| **View Document Details** | `documents/page.tsx` | `GET /api/v1/documents/{id}` | `documents.py` | ❌ **Missing** | No endpoint or modal to view full document text and extraction metadata. |
| **List Saved Citations** | `sources/page.tsx: fetchSources()` | `GET /api/v1/sources` | `sources.py` | ✅ Connected | Populates citations library from consultations; supports filtering by type. |
| **Toggle Star on Citation** | `source-card.tsx` | `POST /api/v1/sources/{id}/star` | `sources.py` | ⚠️ **Disconnected** | Backend endpoint is implemented, but `SourceCard` has no click handler wiring it. |
| **Save / Reset Settings** | `settings/page.tsx` | `localStorage` / Client State | `use-settings.ts` | ❌ **Disconnected** | `useSettings` hook exists but `SettingsPage` was never wired to it. No Save or Reset buttons exist. |

---

## 3. Disconnected Endpoints & Missing Handlers

### 1. Disconnected Document Upload (`DocumentUploadCard`)
- **Location**: `frontend/components/legal/document-upload-card.tsx`
- **Issue**: The `<input type="file" />` element does not pass `onChange={(e) => handleFile(e.target.files?.[0])}`. When a user selects a file or drops a file into the dropzone, no event is emitted, and `uploadFile()` is never invoked.
- **Remediation**: Wire `useDocumentUpload` into `DocumentUploadCard` and connect both file input change and drop events.

### 2. Missing Thread Rename API & UI
- **Location**: `backend/app/routes/threads.py` & `frontend/components/legal/sidebar.tsx`
- **Issue**: Users cannot rename consultation threads.
- **Remediation**:
  - Add `PATCH /api/v1/threads/{thread_id}` in `threads.py` accepting `ThreadUpdate(title=...)`.
  - Add inline edit or rename prompt dialog in `sidebar.tsx`.

### 3. Missing Document Details API & View Modal
- **Location**: `backend/app/routes/documents.py` & `frontend/app/(app)/documents/page.tsx`
- **Issue**: Users cannot view the contents or extraction status of uploaded documents.
- **Remediation**:
  - Add `GET /api/v1/documents/{document_id}` in `documents.py`.
  - Add a "View Document" dialog modal in `documents/page.tsx`.

### 4. Disconnected Settings Persistence
- **Location**: `frontend/app/(app)/settings/page.tsx`
- **Issue**: Form inputs and switches operate as unmanaged or uncontrolled inputs with hardcoded defaults.
- **Remediation**: Connect `SettingsPage` to `useSettings()`, add "Save Settings" and "Reset Defaults" buttons, and display confirmation feedback.

### 5. Dead "Cite this" and "View source" in `SourceCard`
- **Location**: `frontend/components/legal/source-card.tsx`
- **Issue**: "Cite this" button has no `onClick`. "View source" defaults to `href="#"` when URL is null.
- **Remediation**:
  - Implement clipboard copy on "Cite this" with visual toast feedback.
  - Implement a dialog modal on "View source" to show the full statutory passage, enacted year, and jurisdictional authority.
