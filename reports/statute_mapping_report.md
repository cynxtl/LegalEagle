# LegalEagle v2 — Statute Mapping Engine Report (Sprint 2C)

**Date**: September 18, 2026  
**Module**: Statutory Cross-Reference & Translation Subsystem (`services/rag/statute_mapper.py`)  
**Phase**: Sprint 2C — Statute Mapping Engine

---

## 1. Executive Summary

On July 1, 2024, the Republic of India overhauled its colonial-era criminal jurisprudence, replacing:
- **Indian Penal Code, 1860 (IPC)** $\longrightarrow$ **Bharatiya Nyaya Sanhita, 2023 (BNS)**
- **Code of Criminal Procedure, 1973 (CrPC)** $\longrightarrow$ **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)**
- **Indian Evidence Act, 1872 (IEA)** $\longrightarrow$ **Bharatiya Sakshya Adhiniyam, 2023 (BSA)**

Indian citizens and legal practitioners frequently query provisions using their historical numbers (e.g., *"Section 420"*, *"Section 302"*, *"Section 154 CrPC"*, *"Section 65B"*), while contemporary filings require knowledge of the corresponding new acts.

The Statute Mapping Engine enables bidirectional alias cross-referencing so that queries mentioning either historical or modern provisions automatically retrieve both statutory counterparts.

---

## 2. Core Bidirectional Mappings

### A. IPC $\longleftrightarrow$ BNS (Substantive Criminal Law)
| Historical Provision (IPC) | Modern Equivalent (BNS) | Legal Subject Matter |
| :--- | :--- | :--- |
| **Section 420** | **Section 318(4)** | Cheating and dishonestly inducing delivery of property |
| **Section 415 / 417** | **Section 318(1), (2)** | Cheating definition and general penalty |
| **Section 416 / 419** | **Section 319** | Cheating by personation |
| **Section 302** | **Section 103** | Punishment for murder |
| **Section 300** | **Section 101** | Definition of murder |
| **Section 299** | **Section 100** | Culpable homicide |
| **Section 304A** | **Section 106** | Causing death by negligence |
| **Section 304B** | **Section 80** | Dowry death |
| **Section 307** | **Section 109** | Attempt to murder |
| **Section 378 / 379** | **Section 303** | Theft and punishment |
| **Section 383** | **Section 308** | Extortion |
| **Section 390** | **Section 309** | Robbery |
| **Section 391** | **Section 310** | Dacoity |
| **Section 403** | **Section 314** | Dishonest misappropriation of property |
| **Section 405 / 406** | **Section 316** | Criminal breach of trust |
| **Section 34** | **Section 3(5)** | Joint liability / Common intention |
| **Section 120A / 120B** | **Section 61** | Criminal conspiracy |
| **Section 141** | **Section 189** | Unlawful assembly |
| **Section 319 / 320** | **Section 114 / 115** | Hurt and Grievous hurt |
| **Section 339 / 340** | **Section 126 / 127** | Wrongful restraint and confinement |
| **Section 351** | **Section 130** | Assault |
| **Section 354** | **Section 74** | Assault or criminal force to woman with intent to outrage modesty |
| **Section 375 / 376** | **Section 63 / 64** | Rape and statutory penalties |
| **Section 498A** | **Section 85 / 86** | Cruelty by husband or relatives of husband |
| **Section 499 / 500** | **Section 356** | Defamation |
| **Section 503 / 506** | **Section 351** | Criminal intimidation |
| **Section 511** | **Section 62** | Attempt to commit offences |

### B. CrPC $\longleftrightarrow$ BNSS (Criminal Procedure)
| Historical Provision (CrPC) | Modern Equivalent (BNSS) | Procedural Subject Matter |
| :--- | :--- | :--- |
| **Section 154** | **Section 173** | Information in cognizable cases (FIR / e-FIR) |
| **Section 41** | **Section 35** | Police power to arrest without warrant |
| **Section 161** | **Section 180** | Witness examination by investigating police |
| **Section 436A** | **Section 479** | Undertrial prisoner maximum detention period |
| **Section 437** | **Section 480** | Regular bail in non-bailable offences |
| **Section 438** | **Section 482** | Anticipatory bail |
| **Section 439** | **Section 483** | Special bail powers of High Court & Sessions |

### C. IEA $\longleftrightarrow$ BSA (Law of Evidence)
| Historical Provision (IEA) | Modern Equivalent (BSA) | Evidentiary Subject Matter |
| :--- | :--- | :--- |
| **Section 3** | **Section 2(1)(e)** | Interpretation clause / Definition of Evidence |
| **Section 25 / 26** | **Section 22 / 23** | Inadmissibility of police confessions |
| **Section 62** | **Section 57** | Primary evidence |
| **Section 63** | **Section 58** | Secondary evidence |
| **Section 65B** | **Section 61 / 63** | Admissibility & certificate for electronic records |
| **Section 101** | **Section 104** | Burden of proof |

---

## 3. Query-Time Dual Retrieval Behavior

When a user asks:
```
"What is Section 420 IPC?"
```
The retrieval pipeline:
1. Detects `act: "IPC"`, `section: "420"`.
2. Queries `statute_mapper.get_bns_for_ipc("420")` $\rightarrow$ resolves `act: "BNS"`, `section: "318"`.
3. Injects both targets into the prioritized candidate retrieval pool:
   - **Primary Match**: Section 420 IPC (Statutory definition & essential ingredients).
   - **Modern Companion**: Section 318 BNS (Modern statutory equivalent).
4. Both statutory chunks are retrieved and presented to the LLM and user with provenance.
