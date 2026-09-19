# LegalEagle v2 — Source Citation System & Provenance Report (Sprint 2D)

**Date**: September 18, 2026  
**Module**: Answer Provenance & Citation Subsystem (`backend/app/models/schemas.py`, `pipeline.py`, `retriever.py`)  
**Phase**: Sprint 2D — Source Citation System

---

## 1. Executive Summary

Legal applications require absolute transparency, traceability, and legal provenance. Unanchored LLM outputs or vague sources (e.g. *"Retrieved Document"*) compromise user confidence and violate legal research standards.

In Sprint 2D, the citation subsystem was overhauled to ensure that **every retrieved chunk** exposes complete statutory metadata, jurisdictional authority, year of enactment, and classification details.

---

## 2. Canonical Citation Schema

Every chunk returned from the retrieval pipeline and exposed to the frontend/API includes structured provenance attributes:

```json
{
  "id": "src-d4e5f6a7",
  "title": "Indian Penal Code Section 420: Cheating and dishonestly inducing delivery of property",
  "citation": "Indian Penal Code — Section 420",
  "act": "Indian Penal Code, 1860",
  "section": "420",
  "domain": "criminal_law",
  "source_type": "statute",
  "jurisdiction": "Supreme Court / Statutory Law of India",
  "year": 1860,
  "score": 0.0100,
  "excerpt": "Act: Indian Penal Code\nSection 420: Cheating and dishonestly inducing delivery of property\nWhoever cheats and thereby dishonestly induces the person deceived to deliver any property..."
}
```

---

## 3. Provenance Field Specification

| Field | Type | Description | Example |
| :--- | :---: | :--- | :--- |
| **`act`** | `str` | Formal statutory enactment title | `Indian Penal Code, 1860` / `Bharatiya Nyaya Sanhita, 2023` |
| **`section`** | `str` | Specific statutory section or constitutional article | `420`, `318`, `Article 21`, `173`, `61` |
| **`title`** | `str` | Official heading of the provision or case law | `Cheating and dishonestly inducing delivery of property` |
| **`domain`** | `str` | Legal domain taxonomy | `criminal_law`, `constitutional_law`, `procedural_law`, etc. |
| **`source_type`** | `str` | Legal nature of authority | `statute`, `case_law`, `qa` |
| **`jurisdiction`** | `str` | Authoritative judicial body or sovereign | `Supreme Court of India`, `Statutory Law of India` |
| **`year`** | `int` | Year of promulgation or judgment | `1860`, `1922`, `1950`, `1973`, `2023`, `2024` |
| **`score`** | `float` | InLegalBERT L2 distance / priority score | `0.0100` (Direct Statutory), `0.0500` (Mapped Companion) |

---

## 4. Citation Output Examples

### Example 1: Historical IPC Query
**Query**: *"What is Section 420 IPC?"*

**Primary Citation (#1)**:
```
Source:      Indian Penal Code, 1860
Section:     420
Title:       Cheating and dishonestly inducing delivery of property
Domain:      criminal_law
Source Type: statute
Jurisdiction: Supreme Court / Statutory Law of India
Year:        1860
Score:       0.0100
```

**Modern Bharatiya Companion Citation (#2)**:
```
Source:      Bharatiya Nyaya Sanhita, 2023
Section:     318
Title:       Cheating
Domain:      criminal_law
Source Type: statute
Jurisdiction: Supreme Court / Statutory Law of India
Year:        2023
Score:       0.0500
```

---

### Example 2: Constitutional Law Query
**Query**: *"What is Article 21?"*

**Primary Citation (#1)**:
```
Source:      Constitution of India
Section:     Article 21
Title:       Protection of life and personal liberty
Domain:      constitutional_law
Source Type: statute
Jurisdiction: Supreme Court / Statutory Law of India
Year:        1950
Score:       0.0100
```

---

### Example 3: Procedural Law Query
**Query**: *"What is FIR?"*

**Primary Citation (#1)**:
```
Source:      Bharatiya Nagarik Suraksha Sanhita, 2023
Section:     173
Title:       Information in cognizable cases (First Information Report / FIR)
Domain:      procedural_law
Source Type: statute
Jurisdiction: Supreme Court / Statutory Law of India
Year:        2023
Score:       0.0500
```

---

### Example 4: Law of Evidence Query
**Query**: *"What is electronic evidence?"*

**Primary Citation (#1)**:
```
Source:      Bharatiya Sakshya Adhiniyam, 2023
Section:     61
Title:       Electronic and digital records as evidence
Domain:      law_of_evidence
Source Type: statute
Jurisdiction: Supreme Court / Statutory Law of India
Year:        2023
Score:       0.0100
```

---

### Example 5: Tax Law Precedent Query
**Query**: *"Summarize CIT v A.W. Figgies."*

**Primary Citation (#1)**:
```
Source:      Income Tax Act 1922
Section:     Section 66(1) & Section 25(4)
Title:       Commissioner of Income Tax, West Bengal v A. W. Figgies and Company (1953 AIR 455)
Domain:      tax_law
Source Type: case_law
Jurisdiction: Supreme Court of India
Year:        1953
Score:       23.0463
```

---

## 5. Backward & Frontend Compatibility

All modifications maintain complete backwards compatibility:
1. `SourceResponse` in `backend/app/models/schemas.py` retains all original fields (`id`, `title`, `citation`, `jurisdiction`, `year`, `excerpt`, `url`, `type`, `score`, `is_starred`, `created_at`).
2. New fields (`act`, `section`, `domain`, `source_type`) are optional and non-breaking for existing Next.js frontend components.
3. The frontend citation cards seamlessly display enriched titles with exact section headers and enacted acts.
