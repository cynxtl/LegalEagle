import json
import urllib.request
import urllib.parse
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

print("Starting E2E Product Verification...")
report = {}

# ==========================================
# FLOW 1: Create Thread -> Ask Question -> Refresh -> History Persists
# ==========================================
print("\n--- FLOW 1: Thread & Message Persistence ---")
st, thread_data = api_request(f"{BACKEND_BASE}/api/v1/threads", method="POST", data={"title": "E2E Murder Law Consultation"})
print(f"1. Create Thread: status={st}, id={thread_data.get('id') if isinstance(thread_data, dict) else thread_data}")
thread_id = thread_data["id"]

st, chat_data = api_request(f"{BACKEND_BASE}/chat", method="POST", data={
    "message": "What is Section 302 IPC punishment for murder?",
    "thread_id": thread_id,
    "category": "criminal_law"
})
print(f"2. Ask Question (POST /chat): status={st}, confidence={chat_data.get('confidence')}")

st, thread_detail = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="GET")
msgs = thread_detail.get("messages", [])
print(f"3. Retrieve Thread History: status={st}, total messages={len(msgs)}")
flow1_passed = (st == 200 and len(msgs) == 2 and msgs[0]["role"] == "user" and msgs[1]["role"] == "assistant")
print(f"Flow 1 Verdict: {'PASSED' if flow1_passed else 'FAILED'}")
report["Flow 1: Thread & Chat Persistence"] = {
    "status": "PASSED" if flow1_passed else "FAILED",
    "thread_id": thread_id,
    "messages_persisted": len(msgs)
}

# ==========================================
# FLOW 2: Upload Document -> Refresh -> Document Persists
# ==========================================
print("\n--- FLOW 2: Document Upload & Retrieval ---")
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
sample_text = "PETITION UNDER ARTICLE 32 OF THE CONSTITUTION OF INDIA\nIn the Supreme Court of India\nPetitioner: State of Test\nRespondent: Test Party\nSubject: Fundamental Rights Enforcement."
body_bytes = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="e2e_petition_test.txt"\r\n'
    f"Content-Type: text/plain\r\n\r\n"
    f"{sample_text}\r\n"
    f"--{boundary}--\r\n"
).encode("utf-8")

st, upload_data = api_request(
    f"{BACKEND_BASE}/upload",
    method="POST",
    data=body_bytes,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)
doc_id = upload_data.get("id") if isinstance(upload_data, dict) else None
print(f"1. Upload Document: status={st}, doc_id={doc_id}, filename={upload_data.get('name') if isinstance(upload_data, dict) else None}")

st, doc_list = api_request(f"{BACKEND_BASE}/api/v1/documents", method="GET")
found_in_list = any(d.get("id") == doc_id for d in doc_list) if isinstance(doc_list, list) else False
print(f"2. List Documents: status={st}, count={len(doc_list) if isinstance(doc_list, list) else 0}, found uploaded={found_in_list}")

st_detail, doc_detail = api_request(f"{BACKEND_BASE}/api/v1/documents/{doc_id}", method="GET")
print(f"3. Get Document Detail (GET /documents/{{id}}): status={st_detail}, id={doc_detail.get('id') if isinstance(doc_detail, dict) else None}")

flow2_passed = (st == 200 and found_in_list and st_detail == 200)
print(f"Flow 2 Verdict: {'PASSED' if flow2_passed else 'FAILED'}")
report["Flow 2: Document Upload & Detail Persistence"] = {
    "status": "PASSED" if flow2_passed else "FAILED",
    "doc_id": doc_id,
    "detail_endpoint_status": st_detail
}

# ==========================================
# FLOW 3: Ask Legal Question -> View Sources -> Open Citation -> Star
# ==========================================
print("\n--- FLOW 3: Citations & Star Action ---")
st, sources_list = api_request(f"{BACKEND_BASE}/api/v1/sources", method="GET")
print(f"1. List Sources: status={st}, count={len(sources_list) if isinstance(sources_list, list) else 0}")
source_id = None
if isinstance(sources_list, list) and len(sources_list) > 0:
    source_id = sources_list[0]["id"]
    print(f"   Selected Source: id={source_id}, title={sources_list[0].get('title')}, citation={sources_list[0].get('citation')}")
    
    st_star, star_res = api_request(f"{BACKEND_BASE}/api/v1/sources/{source_id}/star", method="POST")
    print(f"2. Toggle Star: status={st_star}, is_starred={star_res.get('is_starred') if isinstance(star_res, dict) else None}")
    flow3_passed = (st == 200 and st_star == 200 and isinstance(star_res.get("is_starred"), bool))
else:
    flow3_passed = False
    
print(f"Flow 3 Verdict: {'PASSED' if flow3_passed else 'FAILED'}")
report["Flow 3: Source Citations & Star Action"] = {
    "status": "PASSED" if flow3_passed else "FAILED",
    "source_id": source_id,
    "star_toggle_success": flow3_passed
}

# ==========================================
# FLOW 4: Thread Rename -> Thread Delete
# ==========================================
print("\n--- FLOW 4: Thread Rename & Deletion ---")
st_rename, rename_res = api_request(
    f"{BACKEND_BASE}/api/v1/threads/{thread_id}",
    method="PATCH",
    data={"title": "Renamed Consultation via PATCH"}
)
print(f"1. Rename Thread (PATCH /threads/{{id}}): status={st_rename}, new_title={rename_res.get('title') if isinstance(rename_res, dict) else None}")

st_del, del_res = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="DELETE")
print(f"2. Delete Thread (DELETE /threads/{{id}}): status={st_del}")

st_verify, _ = api_request(f"{BACKEND_BASE}/api/v1/threads/{thread_id}", method="GET")
print(f"3. Verify Deleted (GET /threads/{{id}}): status={st_verify} (Expected: 404)")

flow4_passed = (st_rename == 200 and st_del in (200, 204) and st_verify == 404)
print(f"Flow 4 Verdict: {'PASSED' if flow4_passed else 'FAILED'}")
report["Flow 4: Thread Rename & Deletion"] = {
    "status": "PASSED" if flow4_passed else "FAILED",
    "rename_status": st_rename,
    "delete_status": st_del,
    "removal_verified_404": (st_verify == 404)
}

# ==========================================
# FLOW 5: Navigation Between Frontend Pages
# ==========================================
print("\n--- FLOW 5: Frontend Page Routing ---")
pages = ["/chat", "/documents", "/sources", "/settings"]
page_results = {}
all_pages_ok = True
for p in pages:
    st_p, body_p = api_request(f"{FRONTEND_BASE}{p}", method="GET")
    is_ok = (st_p == 200 and "<html" in str(body_p).lower())
    page_results[p] = {"status_code": st_p, "ok": is_ok}
    print(f"Page {p}: HTTP {st_p} | Rendered HTML: {is_ok}")
    if not is_ok:
        all_pages_ok = False

print(f"Flow 5 Verdict: {'PASSED' if all_pages_ok else 'FAILED'}")
report["Flow 5: Frontend Page Navigation"] = {
    "status": "PASSED" if all_pages_ok else "FAILED",
    "pages": page_results
}

with open("product_test_summary.json", "w") as f:
    json.dump(report, f, indent=2)

print("\nE2E product testing complete.")
