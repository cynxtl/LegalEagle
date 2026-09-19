import json
import urllib.request
import time

BACKEND_BASE = "http://127.0.0.1:8000"

def api_chat(message):
    req = urllib.request.Request(
        f"{BACKEND_BASE}/chat",
        data=json.dumps({"message": message, "category": "General"}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

print("=" * 70)
print("LEGAL EAGLE V2 — PR-2 HALLUCINATION & GROUNDING BENCHMARK")
print("=" * 70)

test_queries = [
    {
        "id": "HQ-1",
        "question": "What is Section 302 IPC?",
        "type": "in_corpus",
        "expected_statute": "Section 302",
        "expected_act": "Indian Penal Code",
        "expected_concept": "murder"
    },
    {
        "id": "HQ-2",
        "question": "What is Section 420 IPC?",
        "type": "in_corpus",
        "expected_statute": "Section 420",
        "expected_act": "Indian Penal Code",
        "expected_concept": "cheating"
    },
    {
        "id": "HQ-3",
        "question": "What is Article 21?",
        "type": "in_corpus",
        "expected_statute": "Article 21",
        "expected_act": "Constitution of India",
        "expected_concept": "life and personal liberty"
    },
    {
        "id": "HQ-4",
        "question": "What is Section 149 IPC?",
        "type": "out_of_corpus",
        "expected_fallback": "Relevant information not found in the indexed corpus."
    },
    {
        "id": "HQ-5",
        "question": "What is Section 99999 IPC?",
        "type": "fictional_section",
        "expected_fallback": "Relevant information not found in the indexed corpus."
    }
]

results = []

for item in test_queries:
    q = item["question"]
    print(f"\nEvaluating [{item['id']}]: '{q}' ...")
    start_t = time.time()
    st, res = api_chat(q)
    latency = round((time.time() - start_t) * 1000, 1)
    
    ans = res.get("answer", "").strip()
    sources = res.get("sources", [])
    confidence = res.get("confidence", "")
    
    print(f"  Status: HTTP {st} | Latency: {latency}ms | Confidence: {confidence}")
    print(f"  Sources returned: {len(sources)}")
    print(f"  Answer Snippet: {ans[:150]}...")
    
    passed = False
    notes = ""
    
    if item["type"] == "in_corpus":
        has_statute = item["expected_statute"].lower() in ans.lower() or any(item["expected_statute"].lower() in s.get("title", "").lower() for s in sources)
        has_concept = item["expected_concept"].lower() in ans.lower()
        has_sources = len(sources) > 0
        passed = (st == 200 and has_sources and confidence in ("high", "medium") and (has_statute or has_concept))
        notes = f"Grounding verified: statute_match={has_statute}, concept_match={has_concept}, sources={len(sources)}"
    else:
        # Out-of-corpus or fictional section: MUST return exact fallback and low confidence
        is_fallback = "Relevant information not found in the indexed corpus." in ans
        no_fake_penalties = "punished with" not in ans.lower() or is_fallback
        passed = (st == 200 and is_fallback and no_fake_penalties and confidence == "low" and len(sources) == 0)
        notes = f"Fallback verified: is_fallback={is_fallback}, confidence_low={confidence == 'low'}, zero_sources={len(sources) == 0}"
        
    print(f"  Verdict: {'[PASS]' if passed else '[FAIL]'} - {notes}")
    
    results.append({
        "id": item["id"],
        "question": q,
        "type": item["type"],
        "latency_ms": latency,
        "status_code": st,
        "confidence": confidence,
        "sources_count": len(sources),
        "sources": sources,
        "answer": ans,
        "passed": passed,
        "notes": notes
    })

with open("hallucination_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nHallucination testing complete. Results saved to hallucination_results.json")
