"""
LegalEagle Query Classifier — Legal Domain Intelligence Subsystem.

Classifies incoming user queries into one of the canonical legal domains:
  - criminal_law
  - constitutional_law
  - procedural_law
  - law_of_evidence
  - tenancy_law
  - tax_law
  - general_legal_qa

Extracts statutory citations (e.g. "Section 420 IPC", "Article 21") and assigns
confidence scores based on legal terminology density and statutory markers.
"""

import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class QueryClassification:
    query: str
    primary_domain: str
    confidence: float
    secondary_domains: List[str] = field(default_factory=list)
    detected_sections: List[Dict[str, str]] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    target_source_types: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "primary_domain": self.primary_domain,
            "confidence": round(self.confidence, 4),
            "secondary_domains": self.secondary_domains,
            "detected_sections": self.detected_sections,
            "keywords": self.keywords,
            "target_source_types": self.target_source_types,
        }


class LegalQueryClassifier:
    """Multi-domain legal query classifier with statutory entity extraction."""

    # Explicit statutory markers
    STATUTE_PATTERNS = [
        # IPC / BNS
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:ipc|indian\s+penal\s+code)\b", "criminal_law", "IPC"),
        (r"\b(?:ipc|indian\s+penal\s+code)\s*(?:section|sec\.?)?\s*(\d+[A-Za-z]?)\b", "criminal_law", "IPC"),
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:bns|bharatiya\s+nyaya\s+sanhita)\b", "criminal_law", "BNS"),
        (r"\b(?:bns|bharatiya\s+nyaya\s+sanhita)\s*(?:section|sec\.?)?\s*(\d+[A-Za-z]?)\b", "criminal_law", "BNS"),

        # CrPC / BNSS
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:crpc|code\s+of\s+criminal\s+procedure)\b", "procedural_law", "CrPC"),
        (r"\b(?:crpc|code\s+of\s+criminal\s+procedure)\s*(?:section|sec\.?)?\s*(\d+[A-Za-z]?)\b", "procedural_law", "CrPC"),
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:bnss|bharatiya\s+nagarik\s+suraksha\s+sanhita)\b", "procedural_law", "BNSS"),
        (r"\b(?:bnss|bharatiya\s+nagarik\s+suraksha\s+sanhita)\s*(?:section|sec\.?)?\s*(\d+[A-Za-z]?)\b", "procedural_law", "BNSS"),

        # Evidence Act / BSA
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:evidence\s+act|indian\s+evidence\s+act)\b", "law_of_evidence", "IEA"),
        (r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\s*(?:of\s+the\s+)?(?:bsa|bharatiya\s+sakshya\s+adhiniyam)\b", "law_of_evidence", "BSA"),

        # Constitution Articles
        (r"\barticle\s*(\d+[A-Za-z]?(?:\s*(?:to|-)\s*\d+[A-Za-z]?)?)\s*(?:of\s+the\s+)?(?:constitution|indian\s+constitution)?\b", "constitutional_law", "Constitution"),
    ]

    # Core concept to statutory provisions mappings (fallback when section is omitted)
    CONCEPT_STATUTE_MAPPINGS = [
        (r"\btheft\b", [("IPC", "378"), ("BNS", "303")]),
        (r"\bmurder\b", [("IPC", "300"), ("IPC", "302"), ("BNS", "101"), ("BNS", "103")]),
        (r"\bcheating\b", [("IPC", "415"), ("IPC", "420"), ("BNS", "318")]),
        (r"\bcriminal intimidation\b", [("IPC", "503"), ("BNS", "351")]),
        (r"\b(?:fir|first information report)\b", [("BNSS", "173"), ("CrPC", "154")]),
        (r"\banticipatory bail\b", [("BNSS", "482"), ("CrPC", "438")]),
        (r"\bbail\b", [("BNSS", "480"), ("CrPC", "437")]),
        (r"\b(?:electronic evidence|digital evidence)\b", [("BSA", "61"), ("IEA", "65B")]),
        (r"\bevidence\b", [("BSA", "2"), ("IEA", "3")]),
        (r"\bconfession to police\b", [("BSA", "22"), ("IEA", "25")]),
        (r"\bburden of proof\b", [("BSA", "104"), ("IEA", "101")]),
    ]

    # Domain keyword dictionaries with specific weights
    DOMAIN_LEXICON = {
        "criminal_law": {
            "murder": 3.0, "culpable homicide": 3.0, "cheating": 3.0, "theft": 3.0,
            "extortion": 3.0, "robbery": 3.0, "dacoity": 3.0, "criminal breach of trust": 3.5,
            "criminal intimidation": 3.5, "defamation": 3.0, "rape": 3.0, "assault": 2.5,
            "hurt": 2.0, "grievous hurt": 3.0, "kidnapping": 3.0, "abduction": 3.0,
            "conspiracy": 2.5, "criminal conspiracy": 3.5, "unlawful assembly": 3.0,
            "common intention": 3.0, "cruelty": 2.5, "dowry death": 3.5, "negligence death": 3.0,
            "dishonest misappropriation": 3.5, "ipc": 2.5, "bns": 2.5, "penal code": 2.5,
            "mens rea": 2.5, "actus reus": 2.5, "stolen property": 2.5, "attempt to murder": 3.5,
        },
        "constitutional_law": {
            "article 21": 4.0, "article 14": 4.0, "article 19": 4.0, "article 32": 4.0,
            "fundamental rights": 4.0, "fundamental right": 4.0, "constitution": 2.5,
            "constitutional": 2.5, "writ": 3.5, "writs": 3.5, "habeas corpus": 4.0,
            "mandamus": 4.0, "certiorari": 4.0, "quo warranto": 4.0, "prohibition": 2.5,
            "right to equality": 3.5, "freedom of speech": 3.5, "right to life": 3.5,
            "personal liberty": 3.5, "right to education": 3.5, "directive principles": 3.0,
            "preamble": 3.0, "judicial review": 3.0, "basic structure": 3.5, "supreme court writ": 3.5,
        },
        "procedural_law": {
            "fir": 4.0, "first information report": 4.0, "bail": 4.0, "anticipatory bail": 4.5,
            "regular bail": 4.0, "interim bail": 4.0, "non-bailable": 3.5, "bailable": 3.5,
            "arrest": 3.0, "warrant": 3.0, "summons": 2.5, "remand": 3.5, "police custody": 3.5,
            "judicial custody": 3.5, "undertrial": 3.5, "charge sheet": 3.5, "cognizable": 3.5,
            "non-cognizable": 3.5, "crpc": 3.0, "bnss": 3.0, "investigation": 2.0,
            "magistrate": 2.0, "court of session": 2.0, "trial procedure": 3.0,
        },
        "law_of_evidence": {
            "evidence": 3.5, "electronic evidence": 4.5, "digital evidence": 4.0,
            "primary evidence": 4.0, "secondary evidence": 4.0, "oral evidence": 3.5,
            "documentary evidence": 3.5, "confession": 3.5, "confession to police": 4.5,
            "burden of proof": 4.0, "examination-in-chief": 4.0, "cross-examination": 4.0,
            "re-examination": 3.5, "admissibility": 3.0, "admissible": 2.5,
            "witness": 2.5, "section 65b": 4.5, "bsa": 3.0, "evidence act": 3.0,
        },
        "tenancy_law": {
            "tenant": 4.0, "tenants": 4.0, "landlord": 4.0, "landlords": 4.0,
            "tenancy": 4.0, "rent": 3.0, "eviction": 4.0, "unlawful eviction": 4.5,
            "peaceful possession": 4.0, "essential services": 3.0, "security deposit": 4.0,
            "rent control": 4.5, "lease": 2.5, "subletting": 3.5, "rent agreement": 3.0,
            "tenant rights": 4.5, "rights of tenant": 4.5, "rent receipt": 3.5,
        },
        "tax_law": {
            "tax": 3.0, "income tax": 4.0, "cit": 4.0, "a.w. figgies": 5.0, "figgies": 5.0,
            "assessee": 4.0, "assessment": 3.0, "commissioner of income tax": 4.5,
            "capital gains": 3.5, "partnership tax": 4.0, "income-tax act": 4.0,
            "section 66": 3.0, "section 25(4)": 3.5, "taxation": 3.5,
        },
        "general_legal_qa": {
            "plaint": 3.0, "petition": 2.5, "legal notice": 3.5, "court order": 3.0,
            "disobey court order": 3.5, "affidavit": 3.0, "contempt of court": 3.0,
            "power of attorney": 3.5, "agreement": 2.0, "jurisdiction": 2.0,
            "limitation": 2.0, "interlocutory": 3.0, "injunction": 3.0,
        },
    }

    def classify(self, query: str) -> QueryClassification:
        """Classify a legal query into domain and extract statutory markers."""
        clean_query = query.strip()
        lower_query = clean_query.lower()

        detected_sections = []
        domain_scores = {d: 0.0 for d in self.DOMAIN_LEXICON}
        matched_keywords = []

        # 1. Regex Match for Explicit Statutes & Articles
        for pattern, domain, act_name in self.STATUTE_PATTERNS:
            match = re.search(pattern, lower_query)
            if match:
                sec_val = match.group(1).upper()
                detected_sections.append({"act": act_name, "section": sec_val})
                domain_scores[domain] += 6.0
                matched_keywords.append(f"{act_name} {sec_val}")

        # Check for bare sections (e.g. "Section 420", "Section 302") without act name
        bare_sec = re.search(r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\b", lower_query)
        if bare_sec and not detected_sections:
            sec_num = bare_sec.group(1)
            # Check if it matches known IPC core sections
            core_ipc = {"420", "302", "300", "299", "304", "304A", "304B", "307", "378", "379", "383", "390", "391", "403", "405", "415", "416", "417", "498A", "499", "503", "511"}
            if sec_num in core_ipc:
                detected_sections.append({"act": "IPC", "section": sec_num})
                domain_scores["criminal_law"] += 5.0
                matched_keywords.append(f"Section {sec_num} (IPC inferred)")
            elif sec_num in {"154", "41", "161", "436A", "437", "438", "439"}:
                detected_sections.append({"act": "CrPC", "section": sec_num})
                domain_scores["procedural_law"] += 5.0
                matched_keywords.append(f"Section {sec_num} (CrPC inferred)")

        # Fallback concept to statute resolution if no explicit sections detected
        if not detected_sections:
            for pat, acts_and_secs in self.CONCEPT_STATUTE_MAPPINGS:
                if re.search(pat, lower_query):
                    for a, s in acts_and_secs:
                        detected_sections.append({"act": a, "section": s})
                    break

        # 2. Keyword & Multi-word phrase matching
        for domain, lexicon in self.DOMAIN_LEXICON.items():
            for kw, weight in lexicon.items():
                # Word boundary check for keywords
                pattern = r"\b" + re.escape(kw) + r"\b"
                if re.search(pattern, lower_query):
                    domain_scores[domain] += weight
                    matched_keywords.append(kw)

        # 3. Determine Primary & Secondary Domains
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_score = sorted_domains[0]

        if top_score == 0.0:
            primary = "general_legal_qa"
            confidence = 0.50
            secondaries = []
        else:
            primary = top_domain
            # Normalized confidence score
            confidence = min(0.98, max(0.65, top_score / (top_score + 2.0)))
            secondaries = [d for d, s in sorted_domains[1:] if s >= 2.5]

        # Determine target source types
        target_source_types = ["statute", "qa"]
        if primary in {"criminal_law", "constitutional_law", "procedural_law", "law_of_evidence"}:
            if detected_sections:
                target_source_types = ["statute", "qa"]
            else:
                target_source_types = ["statute", "qa"]
        elif primary == "tax_law":
            target_source_types = ["case_law", "qa", "statute"]
        elif primary == "tenancy_law":
            target_source_types = ["statute", "qa"]

        return QueryClassification(
            query=clean_query,
            primary_domain=primary,
            confidence=confidence,
            secondary_domains=secondaries,
            detected_sections=detected_sections,
            keywords=list(set(matched_keywords)),
            target_source_types=target_source_types,
        )


# Global instance
classifier = LegalQueryClassifier()


def classify_query(query: str) -> QueryClassification:
    """Convenience functional interface."""
    return classifier.classify(query)
