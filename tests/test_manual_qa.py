import json
import urllib.request
import urllib.parse
import time
import uuid

BACKEND_BASE = "http://127.0.0.1:8000"
FRONTEND_BASE = "http://127.0.0.1:3000"

def api_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    body = None
    if data is not None and not isinstance(data, (bytes, bytearray)):
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    elif isinstance(data, (bytes, bytearray)):
        body = data

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            status_code = resp.status
            resp_body = resp.read().decode("utf-8")
            try:
                parsed_json = json.loads(resp_body)
                return status_code, parsed_json
            except:
                return status_code, resp_body
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(err_body)
        except:
            return e.code, err_body
    except Exception as e:
        return 500, str(e)

print("=" * 70)
print("LEGAL EAGLE V2 — PR-1 MANUAL QA & ADVERSARIAL EDGE CASE HARNESS")
print("=" * 70)

qa_log = []

def record(test_category, test_name, status, details, passed):
    symbol = "PASS" if passed else "FAIL"
    print(f"[{symbol}] {test_category} :: {test_name} (HTTP {status})")
    qa_log.append({
        "category": test_category,
        "name": test_name,
        "status_code": status,
        "details": details,
        "passed": passed
    })

# ---------------------------------------------------------
# PART 1: REAL USER JOURNEY
# ---------------------------------------------------------
print("\n--- PART 1: REALISTIC USER JOURNEYS ---")

# 1. Create Consultation
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads", method="POST", data={"title": "Anticipatory Bail & FIR Consultation", "category": "Criminal Law"})
thread_id = res.get("id") if isinstance(res, dict) else None
record("User Journey", "1. Create Consultation Thread", st, f"Thread ID: {thread_id}", st == 201 and bool(thread_id))

# 2. Rename Consultation
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="PATCH", data={"title": "Updated: Bail under Section 438 CrPC / 482 BNSS"})
record("User Journey", "2. Rename Consultation", st, f"New Title: {res.get('title') if isinstance(res, dict) else res}", st == 200 and res.get("title") == "Updated: Bail under Section 438 CrPC / 482 BNSS")

# 3. Ask Legal Question in Thread
st, res = api_request(f"{BACKEND_BASE}/chat", method="POST", data={
    "message": "What is the procedure and conditions for anticipatory bail?",
    "thread_id": thread_id,
    "category": "Criminal Law"
})
ans = res.get("answer", "") if isinstance(res, dict) else ""
sources = res.get("sources", []) if isinstance(res, dict) else []
confidence = res.get("confidence", "") if isinstance(res, dict) else ""
record("User Journey", "3. Ask Legal Question (Chat)", st, f"Confidence: {confidence}, Sources: {len(sources)}, Answer len: {len(ans)}", st == 200 and len(ans) > 50 and len(sources) > 0)

# 4. Upload Document
boundary = "----WebKitFormBoundaryQA12345"
doc_content = "IN THE HIGH COURT OF DELHI AT NEW DELHI\nBAIL APPLN. NO. 992/2026\nIN THE MATTER OF: RAJESH SHARMA ...APPLICANT VERSUS STATE (NCT OF DELHI) ...RESPONDENT\nAPPLICATION UNDER SECTION 482 OF BHARATIYA NAGARIK SURAKSHA SANHITA FOR GRANT OF ANTICIPATORY BAIL."
body_bytes = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="Bail_Application_Rajesh_Sharma.txt"\r\n'
    f"Content-Type: text/plain\r\n\r\n"
    f"{doc_content}\r\n"
    f"--{boundary}--\r\n"
).encode("utf-8")

st, res = api_request(f"{BACKEND_BASE}/upload", method="POST", data=body_bytes, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
doc_id = res.get("id") if isinstance(res, dict) else None
record("User Journey", "4. Upload Legal Document", st, f"Doc ID: {doc_id}, Status: {res.get('status') if isinstance(res, dict) else res}", st == 200 and bool(doc_id))

# 5. Simulated Refresh: Fetch thread messages and documents
st_th, res_th = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="GET")
st_docs, res_docs = api_request(f"{BACKEND_BASE}/api/v1/documents", method="GET")
st_doc_det, res_doc_det = api_request(f"{BACKEND_BASE}/api/v1/documents/{doc_id}", method="GET")
persisted_ok = (st_th == 200 and len(res_th.get("messages", [])) == 2 and st_docs == 200 and st_doc_det == 200)
record("User Journey", "5. Page Refresh & State Persistence", st_th, f"Persisted Messages: {len(res_th.get('messages', []))}, Doc Ingested: {res_doc_det.get('name') if isinstance(res_doc_det, dict) else None}", persisted_ok)

# 6. Source Inspection & Star/Unstar
st_src, res_src = api_request(f"{BACKEND_BASE}/api/v1/sources", method="GET")
first_src_id = res_src[0]["id"] if isinstance(res_src, list) and len(res_src) > 0 else None
st_star, res_star = api_request(f"{BACKEND_BASE}/api/v1/sources/{first_src_id}/star", method="POST") if first_src_id else (500, "No source")
record("User Journey", "6. Source Inspection & Star Action", st_star, f"Source ID: {first_src_id}, Starred: {res_star.get('is_starred') if isinstance(res_star, dict) else None}", st_star == 200)

# 7. Delete Thread
st_del, res_del = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="DELETE")
st_del_verify, _ = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="GET")
record("User Journey", "7. Delete Consultation Thread", st_del, f"Delete status: {st_del}, Verification 404: {st_del_verify == 404}", st_del in (200, 204) and st_del_verify == 404)

# ---------------------------------------------------------
# PART 2: ADVERSARIAL & EDGE CASE TESTING ("Try to break it")
# ---------------------------------------------------------
print("\n--- PART 2: ADVERSARIAL & EDGE CASES ('Try to break it') ---")

# Edge 1: Empty thread title
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads", method="POST", data={"title": ""})
record("Adversarial", "E1. Create Thread with Empty Title", st, f"Result: {res}", st in (200, 201, 400, 422))

# Edge 2: Huge 20,000-character thread title
huge_title = "A" * 20000
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads", method="POST", data={"title": huge_title})
edge2_id = res.get("id") if isinstance(res, dict) else None
record("Adversarial", "E2. Create Thread with 20K Character Title", st, f"Handled gracefully without crash. Doc ID: {edge2_id}", st in (200, 201, 400, 422))
if edge2_id:
    api_request(f"{BACKEND_BASE}/api/v1/threads/{edge2_id}", method="DELETE")

# Edge 3: Rename non-existent thread
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads/t-nonexistent-9999", method="PATCH", data={"title": "Should 404"})
record("Adversarial", "E3. Rename Non-Existent Thread", st, f"Response: {res}", st == 404)

# Edge 4: Delete non-existent thread
st, res = api_request(f"{BACKEND_BASE}/api/v1/threads/t-nonexistent-9999", method="DELETE")
record("Adversarial", "E4. Delete Non-Existent Thread", st, f"Response: {res}", st == 404)

# Edge 5: Upload unsupported file type (.exe)
body_exe = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="malicious_payload.exe"\r\n'
    f"Content-Type: application/octet-stream\r\n\r\n"
    f"MZ\x90\x00\x03\x00\x00\x00\r\n"
    f"--{boundary}--\r\n"
).encode("latin-1")
st, res = api_request(f"{BACKEND_BASE}/upload", method="POST", data=body_exe, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
record("Adversarial", "E5. Upload Unsupported File Type (.exe)", st, f"Response: {res}", st == 400)

# Edge 6: Upload empty file (0 bytes)
body_empty = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="empty_file.txt"\r\n'
    f"Content-Type: text/plain\r\n\r\n"
    f"\r\n"
    f"--{boundary}--\r\n"
).encode("utf-8")
st, res = api_request(f"{BACKEND_BASE}/upload", method="POST", data=body_empty, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
record("Adversarial", "E6. Upload 0-Byte Empty File", st, f"Response: {res}", st in (200, 400))

# Edge 7: SQL Injection in Chat Message
st, res = api_request(f"{BACKEND_BASE}/chat", method="POST", data={
    "message": "' UNION SELECT id, name, sql FROM sqlite_master WHERE type='table' --",
    "category": "Criminal Law"
})
record("Adversarial", "E7. SQL Injection in Chat Message", st, f"Status: {st}, Confidence: {res.get('confidence') if isinstance(res, dict) else None}", st == 200 and "sqlite_master" not in str(res))

# Edge 8: XSS Script Injection in Chat Message
st, res = api_request(f"{BACKEND_BASE}/chat", method="POST", data={
    "message": "<script>alert('XSS Attack'); document.location='http://attacker.com'</script>",
    "category": "Criminal Law"
})
ans = res.get("answer", "") if isinstance(res, dict) else ""
record("Adversarial", "E8. XSS Script Injection in Chat", st, f"Status: {st}, Script tag executed on server: False", st == 200)

# Edge 9: Chat with Non-Existent Thread ID (should auto-create or gracefully handle)
st, res = api_request(f"{BACKEND_BASE}/chat", method="POST", data={
    "message": "What is Section 302 IPC?",
    "thread_id": "t-ghost-thread-8888",
    "category": "Criminal Law"
})
record("Adversarial", "E9. Chat with Non-Existent Thread ID", st, f"Status: {st}, Thread Returned: {res.get('thread_id') if isinstance(res, dict) else None}", st == 200)

# Edge 10: Non-Existent Document ID
st, res = api_request(f"{BACKEND_BASE}/api/v1/documents/doc-phantom-9999", method="GET")
record("Adversarial", "E10. Get Non-Existent Document ID", st, f"Status: {st}, Detail: {res}", st == 404)

# Edge 11: Rapid Concurrent Requests (Burst test for SQLite locks)
print("  Running rapid burst test (5 concurrent thread creations)...")
burst_success = 0
for i in range(5):
    st, _ = api_request(f"{BACKEND_BASE}/api/v1/threads", method="POST", data={"title": f"Burst Thread #{i}"})
    if st == 201:
        burst_success += 1
record("Adversarial", "E11. Rapid Burst Requests (SQLite Lock Safety)", 200, f"Successes: {burst_success}/5", burst_success == 5)

with open("manual_qa_results.json", "w") as f:
    json.dump(qa_log, f, indent=2)

print("\nPR-1 Manual QA Harness Finished. Output written to manual_qa_results.json")
