# Backend Response Format Examples

This document shows the exact format your backend should return for each API endpoint.

## 1. Chat Message Response

**Endpoint**: `POST /api/chat`

**Example Request**:
```json
{
  "message": "What are tenant rights in India?",
  "category": "Property",
  "threadId": null
}
```

**Example Response**:
```json
{
  "id": "msg-1704067200000",
  "content": "Under Indian law, tenant rights are protected by the Rent Control Act. Key rights include:\n\n1. **Right to Occupancy**: Tenant has secure right to occupy the property for agreed duration.\n\n2. **Notice Period**: Landlord must provide 15-30 days notice for eviction.\n\n3. **Deposit Protection**: Security deposit must be returned with interest.\n\n4. **Repair & Maintenance**: Landlord is responsible for structural repairs.\n\n5. **Reasonable Rent**: Rent increases must be reasonable and gradual.",
  "confidence": "high",
  "sources": [
    {
      "id": "src-rent-act",
      "title": "Rent Control Act, 1958",
      "type": "act",
      "excerpt": "A tenant shall not be liable to pay any rent in excess of the standard rent...",
      "jurisdiction": "India",
      "year": 1958
    },
    {
      "id": "src-tpa",
      "title": "Transfer of Property Act, 1882 - Section 106",
      "type": "act",
      "excerpt": "Either party to a lease may determine it in the manner provided for in the lease...",
      "jurisdiction": "India",
      "year": 1882
    },
    {
      "id": "src-case-1",
      "title": "Olga Tellis v. Bombay Municipal Corporation",
      "type": "case",
      "excerpt": "The right to livelihood is a fundamental right guaranteed under Article 21...",
      "jurisdiction": "India",
      "year": 1985
    }
  ],
  "threadId": "thread-new"
}
```

---

## 2. Chat Threads Response

**Endpoint**: `GET /api/chat/threads`

**Example Response**:
```json
[
  {
    "id": "thread-t1",
    "title": "Tenant rights under Rent Control Act",
    "category": "Property",
    "updatedAt": "2 min ago",
    "messageCount": 5
  },
  {
    "id": "thread-t2",
    "title": "Section 420 IPC - Cheating",
    "category": "Criminal",
    "updatedAt": "1 hour ago",
    "messageCount": 3
  },
  {
    "id": "thread-t3",
    "title": "Corporate GST Compliance",
    "category": "Corporate",
    "updatedAt": "1 day ago",
    "messageCount": 12
  }
]
```

---

## 3. Documents Upload Response

**Endpoint**: `POST /api/documents/upload`

**Request Format**: FormData
```
file: File (PDF, DOCX, TXT)
category: "Property" | "Criminal" | "Corporate" | "Labor" | "Constitutional"
```

**Example Response**:
```json
{
  "id": "doc-lease-2024",
  "name": "lease_agreement_2024.pdf",
  "size": 245678,
  "uploadedAt": "2024-01-15T10:30:00Z",
  "category": "Property",
  "status": "ready",
  "pages": 5,
  "extractedText": "This Lease Agreement made this 15th day of January, 2024...",
  "insights": {
    "hasTerminationClause": true,
    "depositRequired": "2 months rent",
    "noticePeriod": "30 days"
  }
}
```

---

## 4. Documents List Response

**Endpoint**: `GET /api/documents`

**Example Response**:
```json
[
  {
    "id": "doc-lease-2024",
    "name": "lease_agreement_2024.pdf",
    "size": 245678,
    "uploadedAt": "2024-01-15T10:30:00Z",
    "category": "Property",
    "status": "ready",
    "pages": 5
  },
  {
    "id": "doc-contract-2024",
    "name": "employment_contract.pdf",
    "size": 128956,
    "uploadedAt": "2024-01-14T14:20:00Z",
    "category": "Labor",
    "status": "ready",
    "pages": 3
  },
  {
    "id": "doc-policy-2024",
    "name": "company_policy.docx",
    "size": 98765,
    "uploadedAt": "2024-01-10T09:15:00Z",
    "category": "Corporate",
    "status": "processing",
    "pages": 8
  }
]
```

---

## 5. Settings Get Response

**Endpoint**: `GET /api/settings`

**Example Response**:
```json
{
  "jurisdiction": "India",
  "jurisdictionState": "Maharashtra",
  "language": "English",
  "aiModel": "gpt-4-turbo",
  "privacyMode": false,
  "notificationsEnabled": true,
  "emailUpdates": true,
  "theme": "dark",
  "fontSize": "normal",
  "autoSave": true,
  "citationFormat": "APA",
  "searchDepth": "comprehensive"
}
```

---

## 6. Settings Update Response

**Endpoint**: `PUT /api/settings`

**Request**: Same as GET response above

**Example Response**:
```json
{
  "success": true,
  "message": "Settings updated successfully",
  "settings": {
    "jurisdiction": "India",
    "jurisdictionState": "Delhi",
    "language": "English",
    "aiModel": "gpt-4-turbo",
    "privacyMode": true,
    "notificationsEnabled": false,
    "emailUpdates": false,
    "theme": "light",
    "fontSize": "large",
    "autoSave": true,
    "citationFormat": "Bluebook",
    "searchDepth": "comprehensive"
  }
}
```

---

## 7. Sources List Response

**Endpoint**: `GET /api/sources`

**Example Response**:
```json
[
  {
    "id": "src-rca58",
    "title": "Rent Control Act, 1958",
    "type": "act",
    "jurisdiction": "India",
    "year": 1958,
    "excerpt": "This Act provides for the regulation of the relationship between landlords and tenants...",
    "url": "/sources/rent-control-act-1958",
    "isSaved": true,
    "relevanceScore": 0.95
  },
  {
    "id": "src-tpa82",
    "title": "Transfer of Property Act, 1882",
    "type": "act",
    "jurisdiction": "India",
    "year": 1882,
    "excerpt": "This Act relates to the transfer of property and contains the law of contracts...",
    "url": "/sources/transfer-property-act",
    "isSaved": false,
    "relevanceScore": 0.87
  },
  {
    "id": "src-olga-tellis",
    "title": "Olga Tellis v. Bombay Municipal Corporation",
    "type": "case",
    "jurisdiction": "India",
    "year": 1985,
    "excerpt": "The Supreme Court held that the right to livelihood is implicit in the right to life...",
    "url": "/sources/olga-tellis-case",
    "isSaved": true,
    "relevanceScore": 0.92,
    "caseNumber": "1985 AIR 152",
    "court": "Supreme Court of India"
  }
]
```

---

## 8. Save Source Response

**Endpoint**: `POST /api/sources/:id`

**Example Request**:
```
POST /api/sources/src-rca58
```

**Example Response**:
```json
{
  "success": true,
  "message": "Source saved successfully",
  "sourceId": "src-rca58",
  "saved": true
}
```

---

## 9. Unsave Source Response

**Endpoint**: `DELETE /api/sources/:id`

**Example Request**:
```
DELETE /api/sources/src-rca58
```

**Example Response**:
```json
{
  "success": true,
  "message": "Source removed from saved",
  "sourceId": "src-rca58",
  "saved": false
}
```

---

## 10. Delete Document Response

**Endpoint**: `DELETE /api/documents/:id`

**Example Request**:
```
DELETE /api/documents/doc-lease-2024
```

**Example Response**:
```json
{
  "success": true,
  "message": "Document deleted successfully",
  "documentId": "doc-lease-2024"
}
```

---

## 11. Error Responses

All endpoints should return error responses in this format:

```json
{
  "success": false,
  "error": "Invalid document format",
  "code": "INVALID_FORMAT",
  "details": "Only PDF, DOCX, and TXT files are supported"
}
```

**Common Error Codes**:
- `INVALID_FORMAT` - File type not supported
- `FILE_TOO_LARGE` - File exceeds size limit (10MB)
- `INVALID_CATEGORY` - Category not recognized
- `UNAUTHORIZED` - User not authenticated
- `NOT_FOUND` - Resource doesn't exist
- `SERVER_ERROR` - Internal server error

---

## Response Format Rules

1. **Always include success status**: `"success": true/false`
2. **Use ISO 8601 for timestamps**: `"2024-01-15T10:30:00Z"`
3. **Include confidence scores 0-1**: For relevance metrics
4. **Provide helpful error messages**: For failed requests
5. **Nest related data**: Keep sources, documents organized
6. **Use consistent field names**: Match these examples

---

## Testing Your Backend

### Using cURL

```bash
# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Section 420 IPC?",
    "category": "Criminal"
  }'

# Test settings endpoint
curl -X GET http://localhost:5000/api/settings

# Test documents list
curl -X GET http://localhost:5000/api/documents
```

### Using Python

```python
import requests
import json

# Chat message
response = requests.post(
    "http://localhost:5000/api/chat",
    json={
        "message": "What is Section 420 IPC?",
        "category": "Criminal"
    }
)
print(json.dumps(response.json(), indent=2))

# Get settings
response = requests.get("http://localhost:5000/api/settings")
print(json.dumps(response.json(), indent=2))
```

---

## Notes

- All timestamps should be in ISO 8601 format
- IDs can be UUID, slug, or custom format (just keep them unique)
- Confidence scores should be 0-1 (convert to percentage in frontend)
- Sources can be acts, cases, articles, or other legal documents
- Category should match allowed values from frontend
- File upload max size: 10MB (configurable)
- Response times should be < 5 seconds for better UX

---

This format ensures smooth integration with the frontend! 🚀
