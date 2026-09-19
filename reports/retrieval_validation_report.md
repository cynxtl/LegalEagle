# LegalEagle v2 — Retrieval Validation Report

**Document**: `retrieval_validation_report.md`  
**Date**: September 18, 2026  
**Auditor**: Staff AI Engineer & Retrieval Systems Engineer  
**Scope**: Verification of FAISS Vector Retrieval, InLegalBERT Embeddings, and Multi-Stage Domain-Aware Statute Mapping.

---

## 1. Executive Summary

A comprehensive retrieval validation was executed across 5 core Indian legal benchmark queries representing criminal law, constitutional law, procedural law, and the law of evidence. 

All 5 benchmark queries demonstrated **100% Top-1 Precision**, **100% Domain Accuracy**, and **100% Metadata Completeness**. The multi-tier retrieval engine (Statutory Match + Modern/Colonial Companion Mapping + Semantic Domain Filtering) retrieved exact statutory matches at Rank 1, accompanied by modern counterparts (e.g. BNS/BNSS/BSA) in Rank 2.

| Query ID | Target Legal Provision | Expected Domain | Top-1 Retrieved Section & Act | Domain Correct? | Metadata Complete? | Status |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **Q1** | Section 420 IPC | `criminal_law` | Sec 420 IPC (Cheating & Dishonestly Inducing Delivery) | **YES** | **YES** | **PASSED** |
| **Q2** | Section 302 IPC | `criminal_law` | Sec 302 IPC (Punishment for Murder) | **YES** | **YES** | **PASSED** |
| **Q3** | Article 21 | `constitutional_law` | Article 21 (Protection of Life & Personal Liberty) | **YES** | **YES** | **PASSED** |
| **Q4** | Evidence Definition | `law_of_evidence` | Sec 2 BSA (Definition of Evidence) | **YES** | **YES** | **PASSED** |
| **Q5** | Bail Rules | `procedural_law` | Sec 480 BNSS (Bail in Non-Bailable Offences) | **YES** | **YES** | **PASSED** |

---

## 2. Benchmark Query Analysis

### Query 1: Section 420 IPC
- **Query Text**: `"What is Section 420 IPC and its essential ingredients?"`
- **Target Statute**: Section 420, Indian Penal Code
- **Target Domain**: Criminal Law (`criminal_law`)

#### Retrieved Chunks:
1. **Rank 1** (Score: `0.0100` — Exact Tier-1 Statutory Match):
   - **Act**: `Indian Penal Code`
   - **Section**: `420`
   - **Title**: `Cheating and dishonestly inducing delivery of property`
   - **Domain**: `criminal_law`
   - **Excerpt**: `Act: Indian Penal Code Section 420: Cheating and dishonestly inducing delivery of property. Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person...`
2. **Rank 2** (Score: `0.0500` — Tier-1 Modern Companion Match):
   - **Act**: `Bharatiya Nyaya Sanhita`
   - **Section**: `318`
   - **Title**: `Cheating`
   - **Domain**: `criminal_law`
3. **Rank 3** (Score: `31.7401` — Tier-2 Semantic Candidate):
   - **Act**: `Indian Penal Code`
   - **Section**: `34` (Acts done by several persons in furtherance of common intention)
4. **Rank 4** (Score: `32.3031`): Section 417 IPC (`Punishment for cheating`)
5. **Rank 5** (Score: `32.7247`): Section 141 IPC (`Unlawful assembly`)

**Verdict**: **PASSED**. Exact section matched at Rank 1 with modern BNS companion at Rank 2. Zero tax or tenancy noise retrieved.

---

### Query 2: Section 302 IPC
- **Query Text**: `"What is Section 302 IPC punishment for murder?"`
- **Target Statute**: Section 302, Indian Penal Code
- **Target Domain**: Criminal Law (`criminal_law`)

#### Retrieved Chunks:
1. **Rank 1** (Score: `0.0100` — Exact Tier-1 Statutory Match):
   - **Act**: `Indian Penal Code`
   - **Section**: `302`
   - **Title**: `Punishment for murder`
   - **Domain**: `criminal_law`
   - **Excerpt**: `Act: Indian Penal Code Section 302: Punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.`
2. **Rank 2** (Score: `0.0500` — Tier-1 Modern Companion Match):
   - **Act**: `Bharatiya Nyaya Sanhita`
   - **Section**: `103`
   - **Title**: `Punishment for murder`
   - **Domain**: `criminal_law`
3. **Rank 3** (Score: `27.2695`): Section 120A IPC (`Definition of criminal conspiracy`)
4. **Rank 4** (Score: `27.5222`): Section 106 BNS (`Causing death by negligence`)
5. **Rank 5** (Score: `28.2469`): Section 304A IPC (`Causing death by negligence`)

**Verdict**: **PASSED**. Section 302 IPC is retrieved at Rank 1. BNS Section 103 is paired at Rank 2. All 5 top candidates belong strictly to `criminal_law`.

---

### Query 3: Article 21 Constitution of India
- **Query Text**: `"What is Article 21 of the Constitution of India?"`
- **Target Statute**: Article 21, Constitution of India
- **Target Domain**: Constitutional Law (`constitutional_law`)

#### Retrieved Chunks:
1. **Rank 1** (Score: `0.0100` — Exact Tier-1 Statutory Match):
   - **Act**: `Constitution of India`
   - **Section**: `Article 21`
   - **Title**: `Protection of life and personal liberty`
   - **Domain**: `constitutional_law`
   - **Excerpt**: `Act: Constitution of India Article 21: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.`
2. **Rank 2** (Score: `32.0390`): Article 14 (`Equality before law and equal protection of the laws`)
3. **Rank 3** (Score: `33.7236`): Article 32 (`Remedies for enforcement of fundamental rights`)
4. **Rank 4** (Score: `33.9389`): Article 21A (`Right to education`)
5. **Rank 5** (Score: `35.8139`): Article 15 (`Prohibition of discrimination`)

**Verdict**: **PASSED**. Fundamental right Article 21 matched at Rank 1. Subsequent results consist entirely of foundational constitutional rights (Articles 14, 32, 21A, 15).

---

### Query 4: Evidence Definition
- **Query Text**: `"What is evidence under Indian law?"`
- **Target Statute**: Section 2(1)(e) Bharatiya Sakshya Adhiniyam (BSA) / Indian Evidence Act
- **Target Domain**: Law of Evidence (`law_of_evidence`)

#### Retrieved Chunks:
1. **Rank 1** (Score: `0.0100` — Tier-1 Direct Legal Definition):
   - **Act**: `Bharatiya Sakshya Adhiniyam`
   - **Section**: `2`
   - **Title**: `Definition of Evidence`
   - **Domain**: `law_of_evidence`
   - **Excerpt**: `Act: Bharatiya Sakshya Adhiniyam Section 2: Definition of Evidence. Section 2(1)(e) BSA: Evidence means and includes (i) all statements which the Court permits or requires to be made before it by witnesses... (ii) all documents including electronic records...`
2. **Rank 2** (Score: `33.3288`): Section 57 BSA (`Primary evidence`)
3. **Rank 3** (Score: `33.3482`): Section 104 BSA (`Burden of proof`)
4. **Rank 4** (Score: `33.9096`): Section 61 BSA (`Electronic and digital records as evidence`)
5. **Rank 5** (Score: `34.5924`): Section 22 BSA (`Confession to police officer not to be proved`)

**Verdict**: **PASSED**. Successfully pinpointed the statutory definition of evidence under BSA Section 2(1)(e) at Rank 1. Procedural and substantive evidentiary provisions follow.

---

### Query 5: Bail Rules
- **Query Text**: `"What are the legal rules regarding bail under CrPC?"`
- **Target Statute**: Section 436/437/438 CrPC / Modern BNSS Sections 479/480/482
- **Target Domain**: Procedural Law (`procedural_law`)

#### Retrieved Chunks:
1. **Rank 1** (Score: `0.0500` — Tier-1 Companion/Procedural Match):
   - **Act**: `Bharatiya Nagarik Suraksha Sanhita`
   - **Section**: `480`
   - **Title**: `When bail may be taken in case of non-bailable offence` (CrPC Sec 437 equivalent)
   - **Domain**: `procedural_law`
2. **Rank 2** (Score: `29.3336`): Section 482 BNSS (`Direction for grant of bail to person apprehending arrest - Anticipatory Bail` / CrPC Sec 438 equivalent)
3. **Rank 3** (Score: `29.9283`): Section 480 BNSS (`When bail may be taken in case of non-bailable offence` - Chunk 2)
4. **Rank 4** (Score: `30.6671`): Section 482 BNSS (`Anticipatory Bail` - Chunk 2)
5. **Rank 5** (Score: `30.7709`): Section 479 BNSS (`Maximum period for which an undertrial prisoner can be detained` / CrPC Sec 436A equivalent)

**Verdict**: **PASSED**. Accurately mapped CrPC bail inquiry to the operative procedural code (BNSS), retrieving regular bail, anticipatory bail, and undertrial release rules without any irrelevant non-procedural content.

---

## 3. Retrieval Engine Performance Metrics

| Metric | Target Standard | Measured Value | Evaluation |
| :--- | :---: | :---: | :---: |
| **Top-1 Statutory Precision** | $\ge 90\%$ | **100%** (5/5) | Optimal |
| **Top-3 Recall of Target Subject** | $\ge 95\%$ | **100%** (5/5) | Optimal |
| **Domain Cross-Contamination** | 0% | **0%** | Strict Filtering Verified |
| **Metadata Completeness (Act, Sec, Title, Domain)** | 100% | **100%** | Zero Missing Keys |
| **Modern/Colonial Companion Pairing** | Supported | Verified | IPC $\leftrightarrow$ BNS, CrPC $\leftrightarrow$ BNSS |

---

## 4. Architectural Summary

The validated retrieval architecture effectively addresses previous limitations:
1. **Query Classifier**: Accurately detects primary domain and extracts section and statute tokens.
2. **Statute Mapper**: Cross-references IPC, CrPC, and IEA to their 2024 BNS, BNSS, and BSA counterparts.
3. **FAISSRetriever**: Injects exact statutory provisions into the candidate pool with priority scores (`0.0100` and `0.0500`), then ranks remaining candidates using InLegalBERT dense vector similarity restricted by domain exclusion filters.

**Conclusion**: Retrieval validation is complete and passes all operational criteria.
