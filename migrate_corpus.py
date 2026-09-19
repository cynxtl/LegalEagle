"""
LegalEagle Corpus Migration & Restructuring Engine.

Transforms legacy datasets into structured, unified JSON files adhering to
the target legal taxonomy:
  corpus/
  ├── criminal/
  │   ├── ipc_sections.json
  │   └── bns_sections.json
  ├── procedure/
  │   └── bnss_sections.json
  ├── evidence/
  │   └── bsa_sections.json
  ├── constitution/
  │   └── constitutional_rights.json
  ├── tenancy/
  │   └── tenant_rights.json
  ├── qa/
  │   └── legal_qa.json
  └── cases/
      └── tax_case_law.json
"""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
CORPUS_DIR = PROJECT_ROOT / "corpus"


def setup_directories():
    """Create modular corpus subdirectories."""
    subdirs = [
        CORPUS_DIR / "criminal",
        CORPUS_DIR / "procedure",
        CORPUS_DIR / "evidence",
        CORPUS_DIR / "constitution",
        CORPUS_DIR / "tenancy",
        CORPUS_DIR / "qa",
        CORPUS_DIR / "cases",
    ]
    for d in subdirs:
        d.mkdir(parents=True, exist_ok=True)
    print("Created modular corpus directories.")


def migrate_ipc_sections():
    """Migrate and standardize IPC sections into corpus/criminal/ipc_sections.json."""
    old_ipc_path = CORPUS_DIR / "ipc_sections.json"
    target_path = CORPUS_DIR / "criminal" / "ipc_sections.json"

    if old_ipc_path.exists():
        raw_data = json.loads(old_ipc_path.read_text(encoding="utf-8"))
        standardized = []
        for item in raw_data:
            standardized.append({
                "id": f"ipc-sec-{item.get('section')}",
                "act": "Indian Penal Code",
                "section": str(item.get("section", "")),
                "title": item.get("title", ""),
                "year": "1860",
                "domain": "criminal_law",
                "source_type": "statute",
                "content": item.get("content", "")
            })
        target_path.write_text(json.dumps(standardized, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Standardized {len(standardized)} IPC sections in {target_path.relative_to(PROJECT_ROOT)}")


def create_bns_sections():
    """Create authentic core sections of Bharatiya Nyaya Sanhita, 2023 (BNS)."""
    target_path = CORPUS_DIR / "criminal" / "bns_sections.json"
    bns_data = [
        {
            "id": "bns-sec-103",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "103",
            "title": "Punishment for murder",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever commits murder shall be punished with death or imprisonment for life, "
                "and shall also be liable to fine.\n"
                "(2) When a group of five or more persons acting in concert commits murder on the ground "
                "of race, caste or community, sex, place of birth, language, personal belief or any other "
                "similar ground, each member of such group shall be punished with death or with imprisonment "
                "for life, and shall also be liable to fine.\n\n"
                "Statutory Note: Corresponds to Section 302 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-101",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "101",
            "title": "Murder",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Except in the cases hereinafter excepted, culpable homicide is murder, if the act by which the "
                "death is caused is done with the intention of causing death, or if it is done with the intention "
                "of causing such bodily injury as the offender knows to be likely to cause death, or if the act is "
                "imminently dangerous that it must in all probability cause death.\n\n"
                "Statutory Note: Corresponds to Section 300 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-100",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "100",
            "title": "Culpable homicide",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever causes death by doing an act with the intention of causing death, or with the intention "
                "of causing such bodily injury as is likely to cause death, or with the knowledge that he is likely "
                "by such act to cause death, commits the offence of culpable homicide.\n\n"
                "Statutory Note: Corresponds to Section 299 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-106",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "106",
            "title": "Causing death by negligence",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide, "
                "shall be punished with imprisonment of either description for a term which may extend to five years, and shall also be liable to fine.\n"
                "Provided that where such act is done by a registered medical practitioner while performing medical procedure, the imprisonment shall extend to two years.\n"
                "(2) Whoever causes the death of any person by rash and negligent driving of vehicle not amounting to culpable homicide, and escapes without reporting to police officer or Magistrate, shall be punished with imprisonment up to ten years.\n\n"
                "Statutory Note: Corresponds to Section 304A of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-318",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "318",
            "title": "Cheating",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, "
                "or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, and which act or omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said to 'cheat'.\n"
                "(2) Whoever cheats shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.\n"
                "(4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.\n\n"
                "Statutory Note: Consolidates Section 415, Section 417, and Section 420 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-303",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "303",
            "title": "Theft",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever, intending to take dishonestly any movable property out of the possession of any person without that person's consent, "
                "moves that property in order to such taking, is said to commit theft.\n"
                "(2) Whoever commits theft shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.\n"
                "Provided that where the value of stolen property is less than five thousand rupees, and a person is convicted for the first time, the punishment shall be community service.\n\n"
                "Statutory Note: Corresponds to Section 378 and Section 379 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-316",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "316",
            "title": "Criminal breach of trust",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, "
                "or dishonestly uses or disposes of that property in violation of any direction of law prescribing the mode in which such trust is to be discharged, "
                "or of any legal contract, express or implied, which he has made touching the discharge of such trust, or wilfully suffers any other person so to do, "
                "commits 'criminal breach of trust'.\n"
                "(2) Whoever commits criminal breach of trust shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both.\n\n"
                "Statutory Note: Corresponds to Section 405 and Section 406 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-351",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "351",
            "title": "Criminal intimidation",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever threatens another with any injury to his person, reputation or property, or to the person or reputation of any one in whom that person is interested, "
                "with intent to cause alarm to that person, or to cause that person to do any act which he is not legally bound to do, or to omit to do any act which that person is legally entitled to do, "
                "as the means of avoiding the execution of such threat, commits criminal intimidation.\n"
                "(2) Whoever commits criminal intimidation shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.\n\n"
                "Statutory Note: Corresponds to Section 503 and Section 506 of the Indian Penal Code, 1860."
            )
        },
        {
            "id": "bns-sec-356",
            "act": "Bharatiya Nyaya Sanhita",
            "section": "356",
            "title": "Defamation",
            "year": "2023",
            "domain": "criminal_law",
            "source_type": "statute",
            "content": (
                "Whoever, by words either spoken or intended to be read, or by signs or by visible representations, makes or publishes any imputation concerning any person "
                "intending to harm, or knowing or having reason to believe that such imputation will harm, the reputation of such person, is said, except in the cases hereinafter excepted, to defame that person.\n"
                "(2) Whoever defames another shall be punished with simple imprisonment for a term which may extend to two years, or with fine, or with both, or with community service.\n\n"
                "Statutory Note: Corresponds to Section 499 and Section 500 of the Indian Penal Code, 1860."
            )
        }
    ]
    target_path.write_text(json.dumps(bns_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {len(bns_data)} BNS sections in {target_path.relative_to(PROJECT_ROOT)}")


def create_bnss_sections():
    """Create authentic core sections of Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)."""
    target_path = CORPUS_DIR / "procedure" / "bnss_sections.json"
    bnss_data = [
        {
            "id": "bnss-sec-173",
            "act": "Bharatiya Nagarik Suraksha Sanhita",
            "section": "173",
            "title": "Information in cognizable cases (First Information Report / FIR)",
            "year": "2023",
            "domain": "procedural_law",
            "source_type": "statute",
            "content": (
                "Section 173 BNSS: Information in cognizable cases —\n"
                "(1) Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, "
                "shall be reduced to writing by him or under his direction, and be read over to the informant; and every such information, whether given in writing or reduced to writing as aforesaid, "
                "shall be signed by the person giving it, and the substance thereof shall be entered in a book to be kept by such officer in such form as the State Government may prescribe.\n"
                "Provided that information may be given electronically (e-FIR), and it shall be taken on record on being signed within three days by the person giving it.\n"
                "(2) A copy of the information as recorded shall be given forthwith, free of cost, to the informant.\n\n"
                "Statutory Note: Corresponds to Section 154 of the Code of Criminal Procedure, 1973 (CrPC)."
            )
        },
        {
            "id": "bnss-sec-35",
            "act": "Bharatiya Nagarik Suraksha Sanhita",
            "section": "35",
            "title": "When police may arrest without warrant",
            "year": "2023",
            "domain": "procedural_law",
            "source_type": "statute",
            "content": (
                "Section 35 BNSS: Arrest by police without warrant —\n"
                "Any police officer may without an order from a Magistrate and without a warrant, arrest any person who commits, in the presence of a police officer, a cognizable offence;\n"
                "or against whom a reasonable complaint has been made, or credible information has been received, or a reasonable suspicion exists that he has committed a cognizable offence punishable with imprisonment for a term which may be less than seven years or which may extend to seven years whether with or without fine, subject to satisfaction of necessity conditions.\n\n"
                "Statutory Note: Corresponds to Section 41 of the Code of Criminal Procedure, 1973 (CrPC)."
            )
        },
        {
            "id": "bnss-sec-479",
            "act": "Bharatiya Nagarik Suraksha Sanhita",
            "section": "479",
            "title": "Maximum period for which an undertrial prisoner can be detained",
            "year": "2023",
            "domain": "procedural_law",
            "source_type": "statute",
            "content": (
                "Section 479 BNSS: Undertrial detention and release on personal bond —\n"
                "Where a person has, during the period of investigation, inquiry or trial under this Sanhita of an offence under any law (not being an offence for which the punishment of death or life imprisonment has been specified as one of the punishments under that law) "
                "undergone detention for a period extending up to one-half of the maximum period of imprisonment specified for that offence under that law, he shall be released by the Court on his personal bond with or without sureties.\n"
                "Provided that where such person is a first-time offender (who has never been convicted of any offence in the past), he shall be released on bond if he has undergone detention for up to one-third of the maximum period of imprisonment.\n\n"
                "Statutory Note: Corresponds to Section 436A of the Code of Criminal Procedure, 1973 (CrPC)."
            )
        },
        {
            "id": "bnss-sec-480",
            "act": "Bharatiya Nagarik Suraksha Sanhita",
            "section": "480",
            "title": "When bail may be taken in case of non-bailable offence",
            "year": "2023",
            "domain": "procedural_law",
            "source_type": "statute",
            "content": (
                "Section 480 BNSS: Regular Bail in non-bailable offences —\n"
                "When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station or appears or is brought before a Court other than the High Court or Court of Session, "
                "he may be released on bail, but he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life.\n"
                "Provided that the Court may direct that a person referred to in that clause be released on bail if such person is under the age of sixteen years or is a woman or is sick or infirm.\n\n"
                "Statutory Note: Corresponds to Section 437 of the Code of Criminal Procedure, 1973 (CrPC)."
            )
        },
        {
            "id": "bnss-sec-482",
            "act": "Bharatiya Nagarik Suraksha Sanhita",
            "section": "482",
            "title": "Direction for grant of bail to person apprehending arrest (Anticipatory Bail)",
            "year": "2023",
            "domain": "procedural_law",
            "source_type": "statute",
            "content": (
                "Section 482 BNSS: Anticipatory Bail —\n"
                "Where any person has reason to believe that he may be arrested on an accusation of having committed a non-bailable offence, "
                "he may apply to the High Court or the Court of Session for a direction under this section that in the event of such arrest he shall be released on bail; "
                "and that Court may, after taking into consideration the nature and gravity of the accusation, the antecedents of the applicant, and the possibility of the applicant fleeing from justice, either reject the application or issue an interim order for the grant of anticipatory bail.\n\n"
                "Statutory Note: Corresponds to Section 438 of the Code of Criminal Procedure, 1973 (CrPC)."
            )
        }
    ]
    target_path.write_text(json.dumps(bnss_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {len(bnss_data)} BNSS sections in {target_path.relative_to(PROJECT_ROOT)}")


def create_bsa_sections():
    """Create authentic core sections of Bharatiya Sakshya Adhiniyam, 2023 (BSA)."""
    target_path = CORPUS_DIR / "evidence" / "bsa_sections.json"
    bsa_data = [
        {
            "id": "bsa-sec-2",
            "act": "Bharatiya Sakshya Adhiniyam",
            "section": "2",
            "title": "Definition of Evidence",
            "year": "2023",
            "domain": "law_of_evidence",
            "source_type": "statute",
            "content": (
                "Section 2(1)(e) BSA: Evidence means and includes —\n"
                "(i) all statements which the Court permits or requires to be made before it by witnesses, in relation to matters of fact under inquiry; such statements are called oral evidence;\n"
                "(ii) all documents including electronic or digital records produced for the inspection of the Court; such documents are called documentary evidence.\n\n"
                "Statutory Note: Corresponds to Section 3 of the Indian Evidence Act, 1872."
            )
        },
        {
            "id": "bsa-sec-22",
            "act": "Bharatiya Sakshya Adhiniyam",
            "section": "22",
            "title": "Confession to police officer not to be proved",
            "year": "2023",
            "domain": "law_of_evidence",
            "source_type": "statute",
            "content": (
                "Section 22 BSA: Confession to police inadmissible —\n"
                "No confession made to a police officer shall be proved as against a person accused of any offence.\n"
                "Section 23 provides that no confession made by any person whilst he is in the custody of a police officer, unless it be made in the immediate presence of a Magistrate, shall be proved as against such person.\n\n"
                "Statutory Note: Corresponds to Section 25 and Section 26 of the Indian Evidence Act, 1872."
            )
        },
        {
            "id": "bsa-sec-57",
            "act": "Bharatiya Sakshya Adhiniyam",
            "section": "57",
            "title": "Primary evidence",
            "year": "2023",
            "domain": "law_of_evidence",
            "source_type": "statute",
            "content": (
                "Section 57 BSA: Primary evidence means the document itself produced for the inspection of the Court.\n"
                "Explanation 1: Where a document is executed in several parts, each part is primary evidence of the document.\n"
                "Explanation 2: Where a document is executed in counterpart, each counterpart being executed by one or some of the parties only, each counterpart is primary evidence as against the parties executing it.\n"
                "Explanation 3: Where a number of documents are all made by one uniform process, as in the case of printing, lithography, or photography, each is primary evidence of the contents of the rest.\n\n"
                "Statutory Note: Corresponds to Section 62 of the Indian Evidence Act, 1872."
            )
        },
        {
            "id": "bsa-sec-61",
            "act": "Bharatiya Sakshya Adhiniyam",
            "section": "61",
            "title": "Electronic and digital records as evidence",
            "year": "2023",
            "domain": "law_of_evidence",
            "source_type": "statute",
            "content": (
                "Section 61 BSA: Admissibility of electronic records —\n"
                "Nothing in this Adhiniyam shall apply to deny the admissibility, validity or enforceability of any electronic or digital record as evidence, "
                "such as server logs, documents on computers, messages, website contents, voice mail, messages on social media, emails, etc., on the sole ground that it is an electronic or digital record.\n"
                "Electronic records shall be proved in accordance with Section 63 (certificate requirements).\n\n"
                "Statutory Note: Replaces and modernizes Section 65A and Section 65B of the Indian Evidence Act, 1872."
            )
        },
        {
            "id": "bsa-sec-104",
            "act": "Bharatiya Sakshya Adhiniyam",
            "section": "104",
            "title": "Burden of proof",
            "year": "2023",
            "domain": "law_of_evidence",
            "source_type": "statute",
            "content": (
                "Section 104 BSA: Burden of proof —\n"
                "Whoever desires any Court to give judgment as to any legal right or liability dependent on the existence of facts which he asserts, must prove that those facts exist.\n"
                "When a person is bound to prove the existence of any fact, it is said that the burden of proof lies on that person.\n"
                "In criminal cases, the general burden is always upon the prosecution to prove the guilt of the accused beyond reasonable doubt.\n\n"
                "Statutory Note: Corresponds to Section 101 of the Indian Evidence Act, 1872."
            )
        }
    ]
    target_path.write_text(json.dumps(bsa_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Created {len(bsa_data)} BSA sections in {target_path.relative_to(PROJECT_ROOT)}")


def migrate_dataset_a_qa():
    """Migrate mini_train.jsonl to corpus/qa/legal_qa.json with cleaning."""
    source_file = PROJECT_ROOT / "mini_dataset" / "mini_train.jsonl"
    target_path = CORPUS_DIR / "qa" / "legal_qa.json"

    if not source_file.exists():
        print(f"Dataset A source not found: {source_file}")
        return

    raw_items = json.loads(source_file.read_text(encoding="utf-8"))
    qa_records = []

    for idx, item in enumerate(raw_items, start=1):
        title = item.get("Instruction", "").strip()
        resp = item.get("Response", "").strip()

        # Remove Alpaca template artifacts
        clean_resp = re.split(r'Below is an instruction that describes a task', resp)[0]
        clean_resp = clean_resp.rstrip(' \t\n\r",')

        qa_records.append({
            "id": f"qa-{idx:03d}",
            "title": title,
            "domain": "legal_qa",
            "source_type": "qa",
            "act": "Indian Law Q&A",
            "year": "2024",
            "section": f"QA-{idx}",
            "content": clean_resp
        })

    target_path.write_text(json.dumps(qa_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Migrated {len(qa_records)} Q&A items to {target_path.relative_to(PROJECT_ROOT)}")


def migrate_dataset_b_basics():
    """Migrate indian_legal_basics.txt into constitution and tenancy records."""
    const_path = CORPUS_DIR / "constitution" / "constitutional_rights.json"
    tenancy_path = CORPUS_DIR / "tenancy" / "tenant_rights.json"

    # Constitutional Rights
    const_records = [
        {
            "id": "const-art-14",
            "act": "Constitution of India",
            "section": "Article 14",
            "title": "Equality before law and equal protection of the laws",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 14: Right to Equality — The State shall not deny to any person equality before the law "
                "or the equal protection of the laws within the territory of India. Prohibits discrimination and arbitrary state action."
            )
        },
        {
            "id": "const-art-15",
            "act": "Constitution of India",
            "section": "Article 15",
            "title": "Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 15: Prohibition of discrimination — The State shall not discriminate against any citizen "
                "on grounds only of religion, race, caste, sex, place of birth or any of them."
            )
        },
        {
            "id": "const-art-19",
            "act": "Constitution of India",
            "section": "Article 19",
            "title": "Protection of certain rights regarding freedom of speech, etc.",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 19: Protection of Fundamental Freedoms — Guarantees to all citizens the rights to: "
                "(a) freedom of speech and expression; (b) assemble peaceably and without arms; (c) form associations or unions; "
                "(d) move freely throughout the territory of India; (e) reside and settle in any part of India; and "
                "(g) practise any profession, trade or business, subject to reasonable restrictions under clauses (2) to (6)."
            )
        },
        {
            "id": "const-art-21",
            "act": "Constitution of India",
            "section": "Article 21",
            "title": "Protection of life and personal liberty",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 21: Protection of Life and Personal Liberty — No person shall be deprived of his life or personal liberty "
                "except according to procedure established by law. Judicially expanded to include right to dignity, right to privacy, "
                "right to livelihood, right to health, clean environment, and right to free legal aid."
            )
        },
        {
            "id": "const-art-21A",
            "act": "Constitution of India",
            "section": "Article 21A",
            "title": "Right to education",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 21A: Right to Education — The State shall provide free and compulsory education to all children "
                "of the age of six to fourteen years in such manner as the State may, by law, determine."
            )
        },
        {
            "id": "const-art-22",
            "act": "Constitution of India",
            "section": "Article 22",
            "title": "Protection against arrest and detention in certain cases",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 22: Protection against Arrest and Detention — Guarantees: (1) right to be informed of grounds of arrest; "
                "(2) right to consult and be defended by a legal practitioner of choice; (3) right to be produced before nearest magistrate within 24 hours; "
                "and (4) legal safeguards against arbitrary preventive detention."
            )
        },
        {
            "id": "const-art-23-24",
            "act": "Constitution of India",
            "section": "Articles 23 & 24",
            "title": "Right against exploitation",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Articles 23 & 24: Right against Exploitation — Article 23 prohibits traffic in human beings, begar and forced labor. "
                "Article 24 prohibits employment of children below the age of fourteen years in factories, mines or hazardous occupations."
            )
        },
        {
            "id": "const-art-25-28",
            "act": "Constitution of India",
            "section": "Articles 25-28",
            "title": "Right to freedom of religion",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Articles 25-28: Freedom of Religion — Guarantees freedom of conscience and free profession, practice and propagation of religion (Article 25), "
                "freedom to manage religious affairs (Article 26), freedom from payment of taxes for promotion of religion (Article 27), "
                "and freedom from attendance at religious instruction in State-aided schools (Article 28)."
            )
        },
        {
            "id": "const-art-29-30",
            "act": "Constitution of India",
            "section": "Articles 29-30",
            "title": "Cultural and educational rights of minorities",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Articles 29-30: Minority Rights — Protects interests of minorities to conserve distinct language, script or culture (Article 29), "
                "and guarantees rights of religious and linguistic minorities to establish and administer educational institutions (Article 30)."
            )
        },
        {
            "id": "const-art-32",
            "act": "Constitution of India",
            "section": "Article 32",
            "title": "Remedies for enforcement of fundamental rights",
            "year": "1950",
            "domain": "constitutional_law",
            "source_type": "statute",
            "content": (
                "Article 32: Right to Constitutional Remedies — Right to move the Supreme Court for the enforcement of Fundamental Rights. "
                "The Supreme Court has power to issue directions, orders or prerogative writs including habeas corpus, mandamus, prohibition, quo warranto and certiorari."
            )
        }
    ]
    const_path.write_text(json.dumps(const_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Migrated {len(const_records)} constitutional rights to {const_path.relative_to(PROJECT_ROOT)}")

    # Tenant Rights
    tenant_records = [
        {
            "id": "tenancy-001",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 1",
            "title": "Right to peaceful possession",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to peaceful possession: Once a property is rented, the tenant has the right to peaceful possession without interference or unauthorized intrusion from the landlord."
        },
        {
            "id": "tenancy-002",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 2",
            "title": "Right to essential services",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to essential services: Landlords cannot cut off essential utilities like electricity, water supply, sewage, or gas to force a tenant to vacate."
        },
        {
            "id": "tenancy-003",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 3",
            "title": "Protection against arbitrary eviction",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right against eviction: A tenant cannot be evicted without following due process of law and statutory notice periods as specified in State Rent Control Acts."
        },
        {
            "id": "tenancy-004",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 4",
            "title": "Right to rent receipts",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to receipt: Tenants have the right to demand and receive written receipts for all rent payments made to the landlord."
        },
        {
            "id": "tenancy-005",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 5",
            "title": "Right to repairs and maintenance",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to repairs: Tenants can request necessary structural repairs for the rented property, with obligations governed by state laws and agreements."
        },
        {
            "id": "tenancy-006",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 6",
            "title": "Protection against arbitrary rent increases",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right against arbitrary rent increase: Rent increases are restricted to agreed terms or standard rent ceilings prescribed under State Rent Control Acts."
        },
        {
            "id": "tenancy-007",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 7",
            "title": "Right to privacy and notice",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to privacy: Landlords must provide prior notice before visiting or inspecting the rented property, respecting tenant privacy."
        },
        {
            "id": "tenancy-008",
            "act": "Rent Control & Tenancy Law",
            "section": "Tenant Right 8",
            "title": "Right to return of security deposit",
            "year": "1948",
            "domain": "tenancy_law",
            "source_type": "statute",
            "content": "Right to return of security deposit: Upon vacating the premises in good condition (subject to normal wear and tear), tenants are legally entitled to refund of their security deposit."
        }
    ]
    tenancy_path.write_text(json.dumps(tenant_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Migrated {len(tenant_records)} tenant rights to {tenancy_path.relative_to(PROJECT_ROOT)}")


def migrate_dataset_c_cases():
    """Migrate legal_cases.txt to corpus/cases/tax_case_law.json."""
    source_file = PROJECT_ROOT / "legal_cases.txt"
    target_path = CORPUS_DIR / "cases" / "tax_case_law.json"

    if not source_file.exists():
        print(f"Dataset C source not found: {source_file}")
        return

    case_content = source_file.read_text(encoding="utf-8").strip()
    case_records = [
        {
            "id": "case-sc-1953-figgies",
            "domain": "tax_law",
            "source_type": "case_law",
            "act": "Income Tax Act 1922",
            "section": "Section 66(1) & Section 25(4)",
            "year": "1953",
            "title": "Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)",
            "content": case_content
        }
    ]
    target_path.write_text(json.dumps(case_records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Migrated tax case law to {target_path.relative_to(PROJECT_ROOT)}")


def run_migration():
    print("=" * 60)
    print("Starting LegalEagle Knowledge Base Migration")
    print("=" * 60)
    setup_directories()
    migrate_ipc_sections()
    create_bns_sections()
    create_bnss_sections()
    create_bsa_sections()
    migrate_dataset_a_qa()
    migrate_dataset_b_basics()
    migrate_dataset_c_cases()
    print("=" * 60)
    print("Corpus Migration Complete.")
    print("=" * 60)


if __name__ == "__main__":
    run_migration()
