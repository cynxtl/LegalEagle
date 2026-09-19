# LegalEagle v2 — Corpus Audit & Coverage Analysis Report

**Date**: September 18, 2026  
**Module**: Legal Knowledge Engineering & Retrieval Audit  
**Phase**: Phase 1 — Corpus Audit & Coverage Analysis

---

## 1. Executive Summary

LegalEagle v2 recently transitioned from a corrupted legacy knowledge base (which contained 1 income tax case and 101 bare vocabulary terms) to a structured Indian Penal Code (IPC) corpus. While this restored retrieval of key criminal provisions (such as cheating, murder, criminal breach of trust, and defamation), the knowledge base remains tightly scoped to 35 core provisions.

The purpose of this audit is to baseline current coverage against the complete statutory breadth of Indian statutory law, quantify coverage percentages, and establish the technical groundwork for expanding across criminal, constitutional, procedural, evidentiary, tenancy, tax, and legal Q&A domains.

---

## 2. Quantitative Coverage Metrics

| Metric | Current Status | Statutory Benchmark | Coverage / Status |
| :--- | :--- | :--- | :--- |
| **Total IPC Sections Indexed** | 35 sections | 511 sections (IPC 1860) | **6.85%** |
| **Missing IPC Sections** | 476 sections | — | **93.15% missing** |
| **Active Legal Documents** | 35 documents | — | Baseline |
| **Generated Chunks in FAISS** | 56 vectors | — | 1.6 chunks/document |
| **Embedding Model** | law-ai/InLegalBERT | — | 768 dimensions |
| **FAISS Index File Size** | 199.7 KB | — | index.faiss: 168.0 KB<br>index.pkl: 31.6 KB |
| **Chunk Size Distribution** | Min: 153 chars<br>Max: 722 chars | Upper bound: 800 chars | Avg: 426.7 chars |
| **Domain Representation** | 100% Criminal Law | Target: Multi-domain | 0% Procedure, 0% Constitution, 0% Tenancy, 0% Tax |

---

## 3. Currently Indexed IPC Sections

The 35 indexed provisions cover major offenses against person and property:

1. **Offences Against Property & Fraud (13 sections)**:
   - Section 415 (*Cheating*), Section 416 (*Cheating by personation*), Section 417 (*Punishment for cheating*), Section 418 (*Cheating with knowledge of wrongful loss*), Section 419 (*Punishment for cheating by personation*), Section 420 (*Cheating and dishonestly inducing delivery of property*).
   - Section 378 (*Theft*), Section 379 (*Punishment for theft*), Section 383 (*Extortion*), Section 390 (*Robbery*), Section 391 (*Dacoity*), Section 403 (*Dishonest misappropriation of property*), Section 405 (*Criminal breach of trust*).
2. **Offences Affecting Life & Bodily Harm (15 sections)**:
   - Section 299 (*Culpable homicide*), Section 300 (*Murder*), Section 302 (*Punishment for murder*), Section 304 (*Punishment for culpable homicide not amounting to murder*), Section 304A (*Causing death by negligence*), Section 304B (*Dowry death*), Section 307 (*Attempt to murder*).
   - Section 319 (*Hurt*), Section 320 (*Grievous hurt*), Section 339 (*Wrongful restraint*), Section 340 (*Wrongful confinement*), Section 351 (*Assault*), Section 354 (*Assault or criminal force to woman with intent to outrage modesty*), Section 362 (*Abduction*), Section 375 (*Rape*).
3. **General Principles, Inchoate Crimes & Others (7 sections)**:
   - Section 34 (*Acts done by several persons in furtherance of common intention*), Section 120A (*Definition of criminal conspiracy*), Section 141 (*Unlawful assembly*), Section 498A (*Husband or relative of husband subjecting woman to cruelty*), Section 499 (*Defamation*), Section 503 (*Criminal intimidation*), Section 511 (*Punishment for attempting to commit offences*).

---

## 4. Major Statutory Gaps & Missing Chapters

The current corpus lacks 476 sections across critical IPC chapters:
- **General Exceptions (Sections 76–106)**: Private defence, mistake of fact, accident, infancy, insanity, intoxication, necessity.
- **Offences Against the State (Sections 121–130)**: Waging war, sedition.
- **Offences Against Public Tranquillity (Sections 142–160)**: Rioting, affray, promoting enmity.
- **Offences by or Relating to Public Servants (Sections 161–171)**: Public servant disobeying law, framing incorrect document.
- **Contempts of Lawful Authority of Public Servants (Sections 172–190)**: Absconding to avoid service, refusing oath/signature (Section 180).
- **False Evidence & Offences Against Public Justice (Sections 191–229)**: Perjury, fabricating false evidence.
- **Offences Affecting Public Health, Safety, Decency (Sections 268–294A)**: Public nuisance, rash driving (Section 279), negligent conduct.
- **Offences Relating to Religion (Sections 295–298)**.
- **Offences Relating to Documents & Property Marks (Sections 463–489E)**: Forgery, falsification of accounts.
- **Criminal Breach of Contracts of Service (Sections 490–492)**.
- **Offences Relating to Marriage (Sections 493–498)**: Bigamy, adultery.

---

## 5. Domain Distribution & Knowledge Imbalance

`
Current Corpus Domain Distribution:
====================================
Criminal Law (IPC)          : 100.0% (35 documents / 56 chunks)
Constitutional Law          :   0.0% (0 documents / 0 chunks)
Procedural Law (CrPC/BNSS)  :   0.0% (0 documents / 0 chunks)
Law of Evidence (BSA)       :   0.0% (0 documents / 0 chunks)
Tenancy & Property Law      :   0.0% (0 documents / 0 chunks)
Tax Law                     :   0.0% (0 documents / 0 chunks)
General Legal Q&A           :   0.0% (0 documents / 0 chunks)
`

The system cannot answer questions concerning civil law, fundamental rights, tenancy protection, bail, FIR procedures, or trial rules without hallucination or out-of-domain retrieval.

---

## 6. Target Architecture for Expansion

To achieve balanced legal coverage, the corpus must be migrated and expanded into a modular domain directory tree:
1. corpus/criminal/: Core IPC sections and new Bharatiya Nyaya Sanhita (BNS) provisions.
2. corpus/procedure/: Bharatiya Nagarik Suraksha Sanhita (BNSS) & CrPC procedure.
3. corpus/evidence/: Bharatiya Sakshya Adhiniyam (BSA) provisions.
4. corpus/constitution/: Fundamental rights & constitutional remedies.
5. corpus/tenancy/: Tenant protections & rent control principles.
6. corpus/qa/: Cleaned legal Q&A dataset (200 records from mini_train.jsonl).
7. corpus/cases/: Landmark case law (tax and constitutional precedents).
