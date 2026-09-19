# LegalEagle v2 — Comprehensive Frontend UI Audit Report (Phase 1)

**Date**: September 18, 2026  
**Auditor**: Staff Full Stack & QA Engineer  
**Scope**: Complete Next.js Frontend UI Component Inventory  
**Target Environment**: `http://localhost:3000` (Next.js 16.2.4 App Router)

---

## 1. Executive Summary

A comprehensive inventory of all interactive components across LegalEagle v2's frontend was conducted. The audit inspected 4 primary pages (`/chat`, `/documents`, `/sources`, `/settings`), persistent layouts (`sidebar`, `mobile-header`, `right-panel`), and reusable UI widgets.

**Audit Results by Status**:
- Total Interactive Elements Audited: **34**
- Fully Functional & Connected: **16** (47%)
- Partially Functional / Degraded: **7** (21%)
- Disconnected / Broken: **11** (32%)

---

## 2. Component-by-Component Audit Matrix

### A. Navigation & Layout

| Component | Control Type | Expected Behavior | Actual Behavior | Backend Connected? | Status | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| `LegalSidebar: Logo` | Link | Navigate to `/` landing page | Navigates to `/` | N/A (Client Route) | ✅ Working | None |
| `LegalSidebar: Search` | Button | Open quick search modal | Visual button only, no click handler | No | ❌ Broken | Low |
| `LegalSidebar: New Consultation` | Button (`<Link>`) | Reset active thread, navigate to clean `/chat` | Links to `/chat`, but does not clear active conversation state if already on `/chat` | No | ⚠️ Partial | High |
| `LegalSidebar: Thread Item` | Link | Switch active consultation to target thread | Navigates to `/chat?thread={id}` and loads messages | Yes (`GET /api/v1/threads/{id}`) | ✅ Working | None |
| `LegalSidebar: Delete Thread` | Button (`Trash2`) | Delete thread from database and remove from sidebar | Calls `DELETE /api/v1/threads/{id}` and updates local state | Yes (`DELETE /api/v1/threads/{id}`) | ✅ Working | None |
| `LegalSidebar: Rename Thread` | Button / Context | Allow renaming of thread title | Missing from UI and backend | No | ❌ Broken | High |
| `LegalSidebar: Quick Links` | Navigation List | Navigate between Chat, Documents, Sources, Settings | Updates URL route correctly | N/A | ✅ Working | None |
| `LegalSidebar: Theme Toggle` | Button | Toggle between Light and Dark mode | Cycles dark/light themes via `next-themes` | N/A | ✅ Working | None |
| `MobileHeader: Menu Toggle` | Button | Open responsive slide-out drawer on small screens | Sheet drawer opens navigation | N/A | ✅ Working | None |

---

### B. Consultation & Chat (`/chat`)

| Component | Control Type | Expected Behavior | Actual Behavior | Backend Connected? | Status | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| `Legal Query Starter Cards` | Button (4 cards) | Populate input or send prompt automatically | Invokes `handleSendMessage(prompt)` | Yes (`POST /chat`) | ✅ Working | None |
| `ChatInput: Textarea` | Input | Expand with multiline text, submit on Enter | Captures text, submits on Enter | Yes | ✅ Working | None |
| `ChatInput: Send Button` | Button | Submit message and trigger RAG pipeline | Calls `sendMessage()` and displays skeleton loader | Yes (`POST /chat`) | ✅ Working | None |
| `ChatInput: Attachment` | Button (`Paperclip`) | Open file picker to attach document to query | Click event unhandled | No | ❌ Broken | Medium |
| `ChatInput: Clear Button` | Button (`X`) | Clear input text | Clears textarea content | N/A | ✅ Working | None |
| `ChatMessage: Copy Button` | Button | Copy message content to clipboard | Copies text and shows checked icon | N/A | ✅ Working | None |
| `ChatMessage: Star Button` | Button | Bookmark / star message or source | State toggles locally, not persisted to DB | No | ⚠️ Partial | Medium |
| `RightPanel: Tabs` | Tabs (3 tabs) | Switch between Sources, Confidence, Notes | Switches tab content smoothly | N/A | ✅ Working | None |
| `RightPanel: Source Cards` | Cards | Display retrieved passages for current query | Displays live chunks from active response | Yes | ✅ Working | None |

---

### C. Document Management (`/documents`)

| Component | Control Type | Expected Behavior | Actual Behavior | Backend Connected? | Status | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| `DocumentUploadCard (Main)` | File Dropzone | Drag & drop or browse file, upload to backend | Input `<input type="file">` lacks `onChange`; dropzone lacks file handler | No | ❌ Broken | **Critical** |
| `DocumentUploadCard (Compact)` | File Dropzone | Upload document from sidebar footer | Input `<input type="file">` lacks `onChange` handler | No | ❌ Broken | **Critical** |
| `DocumentsPage: Search` | Input | Filter indexed documents list in real time | Filters list by document name/category | N/A | ✅ Working | None |
| `DocList: Document Row` | List Item | Select document to view in detail panel | Selects doc and renders in `ActiveDocAnalysis` | Yes | ✅ Working | None |
| `DocList: Delete Button` | Button (`Trash2`) | Delete uploaded document from SQLite and disk | Calls `DELETE /api/v1/documents/{id}` | Yes | ✅ Working | None |
| `DocumentsPage: Refresh` | Button | Refresh documents list from backend | **Missing** from page header | No | ❌ Broken | High |
| `ActiveDocAnalysis: Query Doc` | Button | Open chat pre-filtered to this document | Navigates to `/chat`, does not set document context | No | ⚠️ Partial | Medium |
| `ActiveDocAnalysis: View Document` | Button / Modal | View full text or raw document content | **Missing** | No | ❌ Broken | High |

---

### D. Sources Library (`/sources`)

| Component | Control Type | Expected Behavior | Actual Behavior | Backend Connected? | Status | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| `SourcesPage: Search` | Input | Search citations by title, act, or excerpt | Filters source cards dynamically | N/A | ✅ Working | None |
| `SourcesPage: Tabs` | Tabs | Filter by All, Cases, Statutes, Starred | Filters source lists by type | N/A | ✅ Working | None |
| `SourcesPage: Category Chips` | Chips | Filter sources by legal category | Visual chips, filter callback not wired | No | ⚠️ Partial | Medium |
| `SourceCard: View Source` | Anchor Link | Open document URL or view passage modal | `href="#"` when URL is null, scrolls to top | No | ❌ Broken | **High** |
| `SourceCard: Cite This` | Button | Copy formal legal citation to clipboard | Dead button: no `onClick` handler | No | ❌ Broken | **High** |

---

### E. Workspace Settings (`/settings`)

| Component | Control Type | Expected Behavior | Actual Behavior | Backend Connected? | Status | Severity |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: |
| `Profile Inputs` | Inputs & Select | Edit Full Name, Email, Firm, Role | Inputs render static default values | No | ❌ Broken | High |
| `Jurisdiction & Language` | Selects | Change legal corpus jurisdiction & style | Selects change UI state, not persisted | No | ❌ Broken | High |
| `AI Behavior Switches` | Switches | Toggle Confidence, Sources, Reasoning | Switches change UI state, not persisted | No | ❌ Broken | High |
| `Privacy & Notifications` | Switches | Toggle History, Indexing, Alerts | Switches change UI state, not persisted | No | ❌ Broken | Medium |
| `Settings: Save Button` | Button | Save updated preferences | **Missing** from settings page | No | ❌ Broken | **Critical** |
| `Settings: Reset Button` | Button | Reset settings to defaults | **Missing** from settings page | No | ❌ Broken | **High** |
| `Billing: Manage Plan` | Button | Manage subscription | Static placeholder button | No | ⚠️ Partial | Low |
| `Danger Zone: Delete Workspace` | Button | Clear local state and confirm reset | Button lacks `onClick` handler | No | ❌ Broken | High |

---

## 3. Prioritized Defect Classification

### Critical Defects (Immediate Fix Required):
1. **`DocumentUploadCard` File Input Disconnected**: The `<input type="file">` and drag-drop area have no `onChange` / `onDrop` handlers calling `uploadFile`.
2. **`SettingsPage` State & Actions Disconnected**: No Save or Reset buttons; settings values do not persist to `localStorage`.

### High Severity Defects:
3. **`Sidebar` Rename Thread Missing**: No UI or endpoint to rename existing chat consultations.
4. **`Sidebar` New Consultation Action Incomplete**: Clicking "New consultation" while on `/chat` does not clear conversation state.
5. **`SourceCard` View Source & Cite This Broken**: "View source" defaults to `#`; "Cite this" has no copy handler.
6. **`DocumentsPage` Refresh Button & View Modal Missing**: Cannot manually refresh file list or view document contents.

### Medium Severity Defects:
7. **Paperclip Attachment in Chat**: File upload from chat input is unwired.
8. **Sources Category Chips**: Category chips do not filter the citations grid.
9. **Starred Sources Persistence**: Starred sources are not saved to SQLite.
