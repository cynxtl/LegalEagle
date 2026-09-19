# LegalEagle v2 — Answer Generation Audit Report (Phase 4)

**Date**: September 18, 2026  
**Auditor**: Senior Legal AI Architect & Staff RAG Systems Engineer  
**Scope**: Generation Pipeline Investigation, Hallucination Analysis, and Prompt Robustness  
**Evaluated Model**: `Mistral-7B-Instruct-v0.2.Q4_K_M.gguf` via CTransformers (Local Quantized)

---

## 1. Executive Summary

A comprehensive generation audit was executed against the existing generation pipeline (`backend/app/services/llm/generator.py` and `backend/app/services/rag/pipeline.py`) across three critical test cases:
1. **`What is Section 302 IPC?`** (Authoritative penal provision present in index)
2. **`What is Section 420 IPC?`** (Core penal cheating statute present in index)
3. **`What is Section 149 IPC?`** (Unlawful assembly provision **absent** from indexed corpus)

The audit revealed **three severe failure modes** in the unconstrained generation pipeline:
- **Statutory Hallucination**: Fabricating non-existent subsections, cross-sections, and bogus penalties.
- **Prompt Echo & Contamination**: Echoing system prompt instructions and hallucinating simulated conversation dialogue.
- **Uncontrolled Extrapolation on Out-of-Corpus Queries**: When querying unindexed sections (Section 149 IPC), the model fabricated that Section 149 covers "criminal breach of trust" with invented penalty brackets instead of acknowledging absence of data.

---

## 2. Per-Query Empirical Audit Results

### Case 1: "What is Section 302 IPC?"

#### A. Retrieved Chunks Sent to Model
- **Chunk 1**: `Indian Penal Code | Section 302: Punishment for murder` (Statutory text: death or imprisonment for life, and fine)
- **Chunk 2**: `Bharatiya Nyaya Sanhita | Section 103: Punishment for murder` (Statutory text: death or imprisonment for life, and fine)
- **Chunk 3**: `Bharatiya Nyaya Sanhita | Section 106: Causing death by negligence`

#### B. Actual Model Output
```text
ANSWER:
Section 302 IPC of the Indian Penal Code is an offence against murder committed by one person with the intention to cause death or injury to another person in the commission of an act that amounts to a grave offence punishable with death, life imprisonment, or rigorous imprisonment for a term which may extend to seven years. The offence carries mandatory minimum punishment under section 120B, read along with subsection (4) of Section 302 IPC.

Section 103 BN provides for an offence of murder by the commission of which any other offence is committed with the same intent or with the intention to cause death or injury to another person. The offence under this section carries mandatory minimum punishment under Section 120B, read along with subsection (4) of Section 302 IPC.
...
In conclusion, Section 302 IPC and Section 106 IPC are two different provisions of Indian law that carry mandatory minimum punishment for murder...
```

#### C. Failure Mode Identification
- **Hallucinated Subsections**: Fabricated `"subsection (4) of Section 302 IPC"`. Section 302 IPC is a single-paragraph provision with no subsections.
- **Incompatible Statutory Cross-References**: Injected Section 120B (criminal conspiracy) as a mandatory component of Section 302 murder.
- **Statutory Conflation**: Claimed Section 106 (negligence death) carries "mandatory minimum punishment for murder".

---

### Case 2: "What is Section 420 IPC?"

#### A. Retrieved Chunks Sent to Model
- **Chunk 1**: `Indian Penal Code | Section 420: Cheating and dishonestly inducing delivery of property`
- **Chunk 2**: `Bharatiya Nyaya Sanhita | Section 318: Cheating`
- **Chunk 3**: `Bharatiya Nyaya Sanhita | Section 318: Cheating`

#### B. Actual Model Output
```text
CONCLUSION:
Thank you for answering our previous questions in this chat room! It has been interesting learning from your knowledge about Indian law. We hope to have more questions in the future, so please do not hesitate to share your insights with us.
```

#### C. Failure Mode Identification
- **Chat History & Roleplay Drift**: Because the prompt template explicitly contained `CHAT HISTORY: No previous conversation.`, Mistral misinterpreted its persona as a chatroom participant thanking an interlocutor rather than acting as an authoritative legal research engine.
- **Zero Legal Substance**: Generated zero analysis of cheating or delivery of property despite having authentic chunks in context.

---

### Case 3: "What is Section 149 IPC?" (Out-of-Corpus Query)

#### A. Retrieved Chunks Sent to Model
- **Chunk 1**: `Bharatiya Nyaya Sanhita | Section 106: Causing death by negligence`
- **Chunk 2**: `Indian Penal Code | Section 120A: Definition of criminal conspiracy`
- **Chunk 3**: `Indian Penal Code | Section 304B: Dowry death`
*(Notice: None of the retrieved chunks cover Section 149 IPC).*

#### B. Actual Model Output
```text
You are an expert assistant specializing in Indian law...

CONTEXT:
Act: Indian Penal Code
Section 149: Criminal breach of trust

Puniishment under Section 149: Imprisonment for a term which shall not be less than six months but which may extend to two years or with fine which shall not be less than ten thousand rupees and which may extend to ten times the value of such amount...
```

#### C. Failure Mode Identification
- **Catastrophic Legal Fabrication**: In reality, Section 149 IPC defines constructive liability for members of an **unlawful assembly**. The model falsely stated it was **criminal breach of trust** (which is actually Section 405/406 IPC).
- **Invented Penalties**: Fabricated a non-existent multi-tier penalty scale with fines and age concessions.
- **Prompt Reflection**: Reflected the `[INST]` instructions and `CONTEXT:` labels back into the response stream.

---

## 3. Root Cause Analysis

1. **Permissive Prompt Wording**: The template instructed: *"Provide a clear and structured answer detailing key aspects of the applicable Indian law..."*. This implicitly prompted the LLM to rely on parametric pre-training weights when context was sparse.
2. **Missing Out-of-Corpus Guardrail**: The prompt did not specify an exact deterministic string when information is missing from the corpus.
3. **No Structure Delineation**: Output did not separate substantive legal principles, statutory text, and citations.
4. **CTransformers Generation Hyperparameters**: `temperature = 0.3` was sufficiently high to allow token drift and prompt echoing on quantized GGUF models.

---

## 4. Remediation Plan (Phase 5)

1. **Enforce Deterministic Grounding**:
   Re-engineer `QA_PROMPT` to mandate that answers must be derived **solely and strictly** from the text between `CONTEXT_START` and `CONTEXT_END`.
2. **Deterministic Corpus Absence Trigger**:
   When the target section is not in context or retrieval yields no matching statute, output exactly:
   ```
   Relevant information not found in the indexed corpus.
   ```
3. **Structured Response Output**:
   Enforce three discrete sections:
   - `### Legal Summary`
   - `### Applicable Statutory Provisions`
   - `### Citations & Cross-References`
4. **Output Sanitization Post-Processor**:
   Strip any leading instruction tokens (`<s>`, `[INST]`, system preamble echoes) prior to returning responses to the API.
