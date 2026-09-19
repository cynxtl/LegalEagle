# LegalEagle v2 — Retrieval Quality Benchmark Report (Sprint 2E)
**Date**: September 18, 2026  
**Embedding Engine**: `law-ai/InLegalBERT` (768-dim)  
**Total Vectors in Store**: 594  
**Evaluation Scope**: 15 Canonical Benchmark Queries across 6 Domains  

---

## 1. Executive Summary Table

| Domain | Test Query | Classified Domain | Top Retrieved Statute / Provision | Domain Isolated? | Section Grounded? | Latency |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: |
| **Criminal Law** | What is Section 420 IPC? | `criminal_law` | Indian Penal Code (420) | ✅ PASS | ✅ PASS | 183.0 ms |
| **Criminal Law** | What is Section 302 IPC? | `criminal_law` | Indian Penal Code (302) | ✅ PASS | ✅ PASS | 72.4 ms |
| **Criminal Law** | What is theft? | `criminal_law` | Indian Penal Code (378) | ✅ PASS | ✅ PASS | 85.3 ms |
| **Criminal Law** | What is murder? | `criminal_law` | Indian Penal Code (300) | ✅ PASS | ✅ PASS | 75.8 ms |
| **Criminal Law** | What is cheating? | `criminal_law` | Indian Penal Code (415) | ✅ PASS | ✅ PASS | 67.3 ms |
| **Criminal Law** | What is criminal intimidation? | `criminal_law` | Indian Penal Code (503) | ✅ PASS | ✅ PASS | 63.6 ms |
| **Constitutional Law** | What is Article 21? | `constitutional_law` | Constitution of India (Article 21) | ✅ PASS | ✅ PASS | 64.7 ms |
| **Constitutional Law** | What are Fundamental Rights? | `constitutional_law` | Constitution of India (Article 32) | ✅ PASS | ✅ PASS | 62.8 ms |
| **Procedural Law** | What is FIR? | `procedural_law` | Bharatiya Nagarik Suraksha Sanhita (173) | ✅ PASS | ✅ PASS | 73.1 ms |
| **Procedural Law** | What is bail? | `procedural_law` | Bharatiya Nagarik Suraksha Sanhita (480) | ✅ PASS | ✅ PASS | 87.8 ms |
| **Procedural Law** | What is anticipatory bail? | `procedural_law` | Bharatiya Nagarik Suraksha Sanhita (482) | ✅ PASS | ✅ PASS | 93.1 ms |
| **Evidence Law** | What is evidence? | `law_of_evidence` | Bharatiya Sakshya Adhiniyam (2) | ✅ PASS | ✅ PASS | 89.8 ms |
| **Evidence Law** | What is electronic evidence? | `law_of_evidence` | Bharatiya Sakshya Adhiniyam (61) | ✅ PASS | ✅ PASS | 103.8 ms |
| **Tenancy Law** | What rights do tenants have? | `tenancy_law` | Rent Control & Tenancy Law (Tenant Right 2) | ✅ PASS | ✅ PASS | 96.7 ms |
| **Tax Law** | Summarize CIT v A.W. Figgies. | `tax_law` | Income Tax Act 1922 (Section 66(1) & Section 25(4)) | ✅ PASS | ✅ PASS | 85.7 ms |

---

## 2. Benchmark Verification Metrics

- **Total Test Queries**: 15
- **Domain Isolation Rate**: 15/15 (100.0%)
- **Statutory Section Grounding Rate**: 15/15 (100.0%)
- **Cross-Domain Leakage**: 0.0% (Zero instances of criminal/tax or constitutional/tenancy contamination)

---

## 3. Comprehensive Per-Query Results

### Query: "What is Section 420 IPC?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.81`
- **Detected Sections**: `[{'act': 'IPC', 'section': '420'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 420 | Cheating and dishonestly inducing d | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 318 | Cheating | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Bharatiya Nyaya Sanhita | 318 | Cheating | `criminal_law` | `statute` | `37.9117` | `dense_semantic` |
| #4 | Bharatiya Nyaya Sanhita | 106 | Causing death by negligence | `criminal_law` | `statute` | `39.1090` | `dense_semantic` |
| #5 | Indian Penal Code | 417 | Punishment for cheating | `criminal_law` | `statute` | `39.1416` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 420: Cheating and dishonestly inducing delivery of property

Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, and which is capable of being converte...
```

### Query: "What is Section 302 IPC?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.81`
- **Detected Sections**: `[{'act': 'IPC', 'section': '302'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 302 | Punishment for murder | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 103 | Punishment for murder | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Bharatiya Nyaya Sanhita | 106 | Causing death by negligence | `criminal_law` | `statute` | `38.5390` | `dense_semantic` |
| #4 | Indian Penal Code | 141 | Unlawful assembly | `criminal_law` | `statute` | `39.0828` | `dense_semantic` |
| #5 | Indian Penal Code | 120A | Definition of criminal conspiracy | `criminal_law` | `statute` | `39.4108` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 302: Punishment for murder

Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.
```

### Query: "What is theft?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.65`
- **Detected Sections**: `[{'act': 'IPC', 'section': '378'}, {'act': 'BNS', 'section': '303'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 378 | Theft | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 303 | Theft | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Bharatiya Nyaya Sanhita | 303 | Theft | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #4 | Indian Penal Code | 379 | Punishment for theft | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #5 | Bharatiya Nyaya Sanhita | 106 | Causing death by negligence | `criminal_law` | `statute` | `47.6533` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 378: Theft

Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, moves that property in order to such taking, is said to commit theft.

Essential Ingredients of Theft:
1. Dishonest intention to take property (animus furandi).
2. The property mus...
```

### Query: "What is murder?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.65`
- **Detected Sections**: `[{'act': 'IPC', 'section': '300'}, {'act': 'IPC', 'section': '302'}, {'act': 'BNS', 'section': '101'}, {'act': 'BNS', 'section': '103'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 300 | Murder | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 101 | Murder | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Indian Penal Code | 302 | Punishment for murder | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #4 | Bharatiya Nyaya Sanhita | 103 | Punishment for murder | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #5 | Indian Penal Code | 300 | Murder | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 300: Murder

Except in the cases hereinafter excepted, culpable homicide is murder, if the act by which the death is caused is done:
1. With the intention of causing death; or
2. With the intention of causing such bodily injury as the offender knows to be likely to cause the death of the person to whom the harm is cau...
```

### Query: "What is cheating?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.65`
- **Detected Sections**: `[{'act': 'IPC', 'section': '415'}, {'act': 'IPC', 'section': '420'}, {'act': 'BNS', 'section': '318'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 415 | Cheating | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 318 | Cheating | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Indian Penal Code | 420 | Cheating and dishonestly inducing d | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #4 | Bharatiya Nyaya Sanhita | 318 | Cheating | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #5 | Bharatiya Nyaya Sanhita | 318 | Cheating | `criminal_law` | `statute` | `0.0100` | `primary_statute` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 415: Cheating

Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he we...
```

### Query: "What is criminal intimidation?" (Criminal Law)

- **Query Classification**: Primary Domain: `criminal_law` | Confidence: `0.65`
- **Detected Sections**: `[{'act': 'IPC', 'section': '503'}, {'act': 'BNS', 'section': '351'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Indian Penal Code | 503 | Criminal intimidation | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Nyaya Sanhita | 351 | Criminal intimidation | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #3 | Bharatiya Nyaya Sanhita | 351 | Criminal intimidation | `criminal_law` | `statute` | `0.0100` | `primary_statute` |
| #4 | Indian Penal Code | 503 | Criminal intimidation | `criminal_law` | `statute` | `0.0500` | `mapped_companion` |
| #5 | Indian Penal Code | 417 | Punishment for cheating | `criminal_law` | `statute` | `40.1437` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Indian Penal Code
Section 503: Criminal intimidation

Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, or to cause that person to do any act which he is not legally bound to do, or to omit to d...
```

### Query: "What is Article 21?" (Constitutional Law)

- **Query Classification**: Primary Domain: `constitutional_law` | Confidence: `0.83`
- **Detected Sections**: `[{'act': 'Constitution', 'section': '21'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Constitution of India | Article 21 | Protection of life and personal lib | `constitutional_law` | `statute` | `0.0100` | `primary_statute` |
| #2 | Constitution of India | Article 32 | Remedies for enforcement of fundame | `constitutional_law` | `statute` | `50.7327` | `dense_semantic` |
| #3 | Constitution of India | Articles 23 & 24 | Right against exploitation | `constitutional_law` | `statute` | `51.5591` | `dense_semantic` |
| #4 | Constitution of India | Article 15 | Prohibition of discrimination on gr | `constitutional_law` | `statute` | `52.0487` | `dense_semantic` |
| #5 | Constitution of India | Article 21A | Right to education | `constitutional_law` | `statute` | `52.1357` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Constitution of India
Article 21: Protection of life and personal liberty

Article 21: Protection of Life and Personal Liberty — No person shall be deprived of his life or personal liberty except according to procedure established by law. Judicially expanded to include right to dignity, right to privacy, right to livelihood, right to health, c...
```

### Query: "What are Fundamental Rights?" (Constitutional Law)

- **Query Classification**: Primary Domain: `constitutional_law` | Confidence: `0.67`
- **Detected Sections**: `[]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Constitution of India | Article 32 | Remedies for enforcement of fundame | `constitutional_law` | `statute` | `53.5678` | `dense_semantic` |
| #2 | Constitution of India | Articles 23 & 24 | Right against exploitation | `constitutional_law` | `statute` | `54.8487` | `dense_semantic` |
| #3 | Constitution of India | Article 21 | Protection of life and personal lib | `constitutional_law` | `statute` | `55.0222` | `dense_semantic` |
| #4 | Constitution of India | Articles 29-30 | Cultural and educational rights of  | `constitutional_law` | `statute` | `57.2256` | `dense_semantic` |
| #5 | Constitution of India | Article 15 | Prohibition of discrimination on gr | `constitutional_law` | `statute` | `57.2276` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Constitution of India
Article 32: Remedies for enforcement of fundamental rights

Article 32: Right to Constitutional Remedies — Right to move the Supreme Court for the enforcement of Fundamental Rights. The Supreme Court has power to issue directions, orders or prerogative writs including habeas corpus, mandamus, prohibition, quo warranto and...
```

### Query: "What is FIR?" (Procedural Law)

- **Query Classification**: Primary Domain: `procedural_law` | Confidence: `0.67`
- **Detected Sections**: `[{'act': 'BNSS', 'section': '173'}, {'act': 'CrPC', 'section': '154'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Bharatiya Nagarik Suraksha Sanhita | 173 | Information in cognizable cases (Fi | `procedural_law` | `statute` | `0.0500` | `mapped_companion` |
| #2 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `57.7050` | `dense_semantic` |
| #3 | Bharatiya Nagarik Suraksha Sanhita | 173 | Information in cognizable cases (Fi | `procedural_law` | `statute` | `58.2230` | `dense_semantic` |
| #4 | Bharatiya Nagarik Suraksha Sanhita | 35 | When police may arrest without warr | `procedural_law` | `statute` | `58.3033` | `dense_semantic` |
| #5 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `58.5453` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Bharatiya Nagarik Suraksha Sanhita
Section 173: Information in cognizable cases (First Information Report / FIR)

Section 173 BNSS: Information in cognizable cases —
(1) Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, shall be reduced to writing by him or under ...
```

### Query: "What is bail?" (Procedural Law)

- **Query Classification**: Primary Domain: `procedural_law` | Confidence: `0.67`
- **Detected Sections**: `[{'act': 'BNSS', 'section': '480'}, {'act': 'CrPC', 'section': '437'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `0.0500` | `mapped_companion` |
| #2 | Bharatiya Nagarik Suraksha Sanhita | 482 | Direction for grant of bail to pers | `procedural_law` | `statute` | `47.8522` | `dense_semantic` |
| #3 | Bharatiya Nagarik Suraksha Sanhita | 482 | Direction for grant of bail to pers | `procedural_law` | `statute` | `48.3027` | `dense_semantic` |
| #4 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `48.7719` | `dense_semantic` |
| #5 | Bharatiya Nagarik Suraksha Sanhita | 479 | Maximum period for which an undertr | `procedural_law` | `statute` | `49.2130` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Bharatiya Nagarik Suraksha Sanhita
Section 480: When bail may be taken in case of non-bailable offence

Section 480 BNSS: Regular Bail in non-bailable offences —
When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station or appears ...
```

### Query: "What is anticipatory bail?" (Procedural Law)

- **Query Classification**: Primary Domain: `procedural_law` | Confidence: `0.81`
- **Detected Sections**: `[{'act': 'BNSS', 'section': '482'}, {'act': 'CrPC', 'section': '438'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Bharatiya Nagarik Suraksha Sanhita | 482 | Direction for grant of bail to pers | `procedural_law` | `statute` | `0.0500` | `mapped_companion` |
| #2 | Bharatiya Nagarik Suraksha Sanhita | 482 | Direction for grant of bail to pers | `procedural_law` | `statute` | `46.2944` | `dense_semantic` |
| #3 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `47.1901` | `dense_semantic` |
| #4 | Bharatiya Nagarik Suraksha Sanhita | 480 | When bail may be taken in case of n | `procedural_law` | `statute` | `49.5141` | `dense_semantic` |
| #5 | Bharatiya Nagarik Suraksha Sanhita | 479 | Maximum period for which an undertr | `procedural_law` | `statute` | `49.7056` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Bharatiya Nagarik Suraksha Sanhita
Section 482: Direction for grant of bail to person apprehending arrest (Anticipatory Bail)

Section 482 BNSS: Anticipatory Bail —
Where any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, he may apply to the High Court or the Court of Session f...
```

### Query: "What is evidence?" (Evidence Law)

- **Query Classification**: Primary Domain: `law_of_evidence` | Confidence: `0.65`
- **Detected Sections**: `[{'act': 'BSA', 'section': '2'}, {'act': 'IEA', 'section': '3'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Bharatiya Sakshya Adhiniyam | 2 | Definition of Evidence | `law_of_evidence` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Sakshya Adhiniyam | 57 | Primary evidence | `law_of_evidence` | `statute` | `49.1654` | `dense_semantic` |
| #3 | Bharatiya Sakshya Adhiniyam | 61 | Electronic and digital records as e | `law_of_evidence` | `statute` | `50.9982` | `dense_semantic` |
| #4 | Bharatiya Sakshya Adhiniyam | 57 | Primary evidence | `law_of_evidence` | `statute` | `51.0140` | `dense_semantic` |
| #5 | Bharatiya Sakshya Adhiniyam | 104 | Burden of proof | `law_of_evidence` | `statute` | `53.0979` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Bharatiya Sakshya Adhiniyam
Section 2: Definition of Evidence

Section 2(1)(e) BSA: Evidence means and includes —
(i) all statements which the Court permits or requires to be made before it by witnesses, in relation to matters of fact under inquiry; such statements are called oral evidence;
(ii) all documents including electronic or digital re...
```

### Query: "What is electronic evidence?" (Evidence Law)

- **Query Classification**: Primary Domain: `law_of_evidence` | Confidence: `0.80`
- **Detected Sections**: `[{'act': 'BSA', 'section': '61'}, {'act': 'IEA', 'section': '65B'}]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Bharatiya Sakshya Adhiniyam | 61 | Electronic and digital records as e | `law_of_evidence` | `statute` | `0.0100` | `primary_statute` |
| #2 | Bharatiya Sakshya Adhiniyam | 2 | Definition of Evidence | `law_of_evidence` | `statute` | `40.0580` | `dense_semantic` |
| #3 | Bharatiya Sakshya Adhiniyam | 57 | Primary evidence | `law_of_evidence` | `statute` | `40.2490` | `dense_semantic` |
| #4 | Bharatiya Sakshya Adhiniyam | 57 | Primary evidence | `law_of_evidence` | `statute` | `42.0833` | `dense_semantic` |
| #5 | Bharatiya Sakshya Adhiniyam | 104 | Burden of proof | `law_of_evidence` | `statute` | `43.5608` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Bharatiya Sakshya Adhiniyam
Section 61: Electronic and digital records as evidence

Section 61 BSA: Admissibility of electronic records —
Nothing in this Adhiniyam shall apply to deny the admissibility, validity or enforceability of any electronic or digital record as evidence, such as server logs, documents on computers, messages, website con...
```

### Query: "What rights do tenants have?" (Tenancy Law)

- **Query Classification**: Primary Domain: `tenancy_law` | Confidence: `0.67`
- **Detected Sections**: `[]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Rent Control & Tenancy Law | Tenant Right 2 | Right to essential services | `tenancy_law` | `statute` | `42.6657` | `dense_semantic` |
| #2 | Rent Control & Tenancy Law | Tenant Right 5 | Right to repairs and maintenance | `tenancy_law` | `statute` | `43.0023` | `dense_semantic` |
| #3 | Rent Control & Tenancy Law | Tenant Right 4 | Right to rent receipts | `tenancy_law` | `statute` | `43.6384` | `dense_semantic` |
| #4 | Rent Control & Tenancy Law | Tenant Right 1 | Right to peaceful possession | `tenancy_law` | `statute` | `44.9678` | `dense_semantic` |
| #5 | Rent Control & Tenancy Law | Tenant Right 7 | Right to privacy and notice | `tenancy_law` | `statute` | `45.6735` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Act: Rent Control & Tenancy Law
Section Tenant Right 2: Right to essential services

Right to essential services: Landlords cannot cut off essential utilities like electricity, water supply, sewage, or gas to force a tenant to vacate.
```

### Query: "Summarize CIT v A.W. Figgies." (Tax Law)

- **Query Classification**: Primary Domain: `tax_law` | Confidence: `0.88`
- **Detected Sections**: `[]`
- **Retrieved Results**: Top 5 chunks

| Rank | Act Name | Section | Title | Domain | Source Type | L2 Score | Stage |
| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: |
| #1 | Income Tax Act 1922 | Section 66(1) & Section 25(4) | Commissioner of Income Tax, West Be | `tax_law` | `case_law` | `23.0463` | `dense_semantic` |
| #2 | Income Tax Act 1922 | Section 66(1) & Section 25(4) | Commissioner of Income Tax, West Be | `tax_law` | `case_law` | `23.3362` | `dense_semantic` |
| #3 | Income Tax Act 1922 | Section 66(1) & Section 25(4) | Commissioner of Income Tax, West Be | `tax_law` | `case_law` | `23.6893` | `dense_semantic` |
| #4 | Income Tax Act 1922 | Section 66(1) & Section 25(4) | Commissioner of Income Tax, West Be | `tax_law` | `case_law` | `24.6788` | `dense_semantic` |
| #5 | Income Tax Act 1922 | Section 66(1) & Section 25(4) | Commissioner of Income Tax, West Be | `tax_law` | `case_law` | `24.9851` | `dense_semantic` |

**Top Chunk Content Excerpt**:
```text
Case Law: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
Act: Income Tax Act 1922

Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others
Supreme Court of India
```
