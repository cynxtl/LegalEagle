# LegalEagle v2 — Semantic Retrieval Evaluation Report
**Date**: September 18, 2026  
**Embedding Engine**: `law-ai/InLegalBERT` (768-dim)  
**Total Chunks in Index**: 668 vectors across 6 domains  
**Phase**: Phase 7 — Retrieval Evaluation

---
## Evaluation Summary
| Domain | Test Query | Top Match Title | Top Source Type | L2 Score | Assessment |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Criminal Law** | What is Section 420 IPC? | Cheating | `statute` | `37.9117` | ✓ Highly Relevant |
| **Criminal Law** | What is Section 302 IPC? | Definition of criminal conspiracy | `statute` | `39.4108` | ✓ Highly Relevant |
| **Criminal Law** | What is cheating? | What are the different types of wri | `qa` | `36.0277` | ✓ Highly Relevant |
| **Criminal Law** | What is murder? | Causing death by negligence | `statute` | `45.6647` | ✓ Relevant |
| **Criminal Law** | What is theft? | What are the reports or statements  | `qa` | `47.1794` | ✓ Relevant |
| **Criminal Law** | What is criminal intimidation? | What are some common types of Inter | `qa` | `39.8075` | ✓ Highly Relevant |
| **Constitutional Law** | What is Article 21? | Article 12 of Indian Constitution | `qa` | `48.2746` | ✓ Relevant |
| **Constitutional Law** | What are Fundamental Rights? | What are the different types of wri | `qa` | `52.6087` | ✓ Relevant |
| **Tenant Law** | What rights do tenants have? | What happens if a party fails to fi | `qa` | `41.4945` | ✓ Highly Relevant |
| **Tax Law** | Summarize CIT v A.W. Figgies. | Commissioner of Income Tax, West Be | `case_law` | `23.0463` | ✓ Highly Relevant |
| **Evidence & Procedure** | What is evidence? | What is examination-in-chief? | `qa` | `46.3216` | ✓ Relevant |
| **Evidence & Procedure** | What is bail? | What is a bail application? | `qa` | `41.8072` | ✓ Highly Relevant |

---

## Detailed Query Benchmarks

### Criminal Law: "What is Section 420 IPC?"
#### Rank 1 — L2 Distance: `37.9117`
- **Title**: Cheating
- **Act**: Bharatiya Nyaya Sanhita
- **Section / Provision**: 318
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 2023

```text
Act: Bharatiya Nyaya Sanhita
Section 318: Cheating

Statutory Note: Consolidates Section 415, Section 417, and Section 420 of the Indian Penal Code, 1860.
```
#### Rank 2 — L2 Distance: `39.0492`
- **Title**: What is a bail application?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-57
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What is a bail application?

A bail application is a petition filed by an accused person requesting release from custody during the pendency of legal proceedings. It is filed in the court where the case is pending trial or appeal. The court has discretion to grant or deny bail based on criteria like flight risktampering with evidenceprevious criminal record etc.
```
#### Rank 3 — L2 Distance: `39.1416`
- **Title**: Punishment for cheating
- **Act**: Indian Penal Code
- **Section / Provision**: 417
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 417: Punishment for cheating

Whoever cheats shall be punished with imprisonment of either description for a term which may extend to one year, or with fine, or with both.
Simple cheating under Section 417 applies where there is deception without the aggravated inducement to deliver property or alter valuable securities (which is covered under Section 420).
```

### Criminal Law: "What is Section 302 IPC?"
#### Rank 1 — L2 Distance: `39.4108`
- **Title**: Definition of criminal conspiracy
- **Act**: Indian Penal Code
- **Section / Provision**: 120A
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 120A: Definition of criminal conspiracy

Punishment under Section 120B: Same punishment as for abetment of the offence if offence is punishable with death, life imprisonment, or rigorous imprisonment of 2+ years; in other cases, imprisonment up to six months or fine or both.
```
#### Rank 2 — L2 Distance: `39.6645`
- **Title**: What are the different types of writs?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-63
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the different types of writs?

. LastlyCertiorari is used to quash arbitrary orders or judgments and direct certification of records.
```
#### Rank 3 — L2 Distance: `39.7180`
- **Title**: Cheating
- **Act**: Bharatiya Nyaya Sanhita
- **Section / Provision**: 318
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 2023

```text
Act: Bharatiya Nyaya Sanhita
Section 318: Cheating

Statutory Note: Consolidates Section 415, Section 417, and Section 420 of the Indian Penal Code, 1860.
```

### Criminal Law: "What is cheating?"
#### Rank 1 — L2 Distance: `36.0277`
- **Title**: What are the different types of writs?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-63
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the different types of writs?

. LastlyCertiorari is used to quash arbitrary orders or judgments and direct certification of records.
```
#### Rank 2 — L2 Distance: `36.3367`
- **Title**: Cheating by personation
- **Act**: Indian Penal Code
- **Section / Provision**: 416
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 416: Cheating by personation

A person is said to 'cheat by personation' if he cheats by pretending to be some other person, or by knowingly substituting one person for another, or representing that he or any other person is a person other than he or such other person really is.

Explanation: The offence is committed whether the individual personated is a real or imaginary person.
```
#### Rank 3 — L2 Distance: `36.6321`
- **Title**: What happens if someone disobeys a court order?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-55
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What happens if someone disobeys a court order?

Contempt of court - The judge may issue a contempt of court orderwhich can result in fines or jail time.
Fines - Monetary penalties may be imposed for violating orders.
Arrest and detention - Police can arrest and detain someone for ignoring a court order like an arrest warrant or subpoena.
Lawsuits - The injured party may sue someone who doesn't follow a court order like honoring a contract.
Loss of the case - Judges can rule against parties who don't follow orders.
Jail time - Continued refusal to comply can result in jail time to coerce compliance.
```

### Criminal Law: "What is murder?"
#### Rank 1 — L2 Distance: `45.6647`
- **Title**: Causing death by negligence
- **Act**: Bharatiya Nyaya Sanhita
- **Section / Provision**: 106
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 2023

```text
Act: Bharatiya Nyaya Sanhita
Section 106: Causing death by negligence

(2) Whoever causes the death of any person by rash and negligent driving of vehicle not amounting to culpable homicide, and escapes without reporting to police officer or Magistrate, shall be punished with imprisonment up to ten years.
```
#### Rank 2 — L2 Distance: `46.8804`
- **Title**: Culpable homicide
- **Act**: Indian Penal Code
- **Section / Provision**: 299
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 299: Culpable homicide

Explanation 1: A person who causes bodily injury to another who is laboring under a disorder, disease or bodily infirmity, and thereby accelerates the death of that other, shall be deemed to have caused his death.
Explanation 2: Where death is caused by bodily injury, the person who causes such bodily injury shall be deemed to have caused the death, although by resorting to proper remedies and skillful treatment the death might have been prevented.
```
#### Rank 3 — L2 Distance: `47.3842`
- **Title**: Causing death by negligence
- **Act**: Indian Penal Code
- **Section / Provision**: 304A
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 304A: Causing death by negligence

Whoever causes the death of any person by doing any rash or negligent act not amounting to culpable homicide, shall be punished with imprisonment of either description for a term which may extend to two years, or with fine, or with both.
Essential Ingredients:
1. Death of a human being.
2. The accused caused the death.
3. The act was rash or negligent, but did not amount to culpable homicide (absence of intention and knowledge to cause death).
```

### Criminal Law: "What is theft?"
#### Rank 1 — L2 Distance: `47.1794`
- **Title**: What are the reports or statements which do not amount to be an FIR?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-51
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the reports or statements which do not amount to be an FIR?

-Information to the Magistrate or police officer on phone.
-Information received at police station prior to the lodging of an F.LR.
```
#### Rank 2 — L2 Distance: `47.6533`
- **Title**: Causing death by negligence
- **Act**: Bharatiya Nyaya Sanhita
- **Section / Provision**: 106
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 2023

```text
Act: Bharatiya Nyaya Sanhita
Section 106: Causing death by negligence

(2) Whoever causes the death of any person by rash and negligent driving of vehicle not amounting to culpable homicide, and escapes without reporting to police officer or Magistrate, shall be punished with imprisonment up to ten years.
```
#### Rank 3 — L2 Distance: `47.6628`
- **Title**: What happens if a party fails to file pleadings in India within the prescribed time?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-25
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What happens if a party fails to file pleadings in India within the prescribed time?

. It's crucial for parties to adhere to the prescribed timelines for filing pleadings to avoid adverse consequences.
```

### Criminal Law: "What is criminal intimidation?"
#### Rank 1 — L2 Distance: `39.8075`
- **Title**: What are some common types of Interlocutory Applications filed in Indian courts?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-42
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are some common types of Interlocutory Applications filed in Indian courts?

. Release of Property: Filed to seek the release of seized or attached property during the litigation.
```
#### Rank 2 — L2 Distance: `40.0123`
- **Title**: What are the different types of writs?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-63
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the different types of writs?

. LastlyCertiorari is used to quash arbitrary orders or judgments and direct certification of records.
```
#### Rank 3 — L2 Distance: `40.1437`
- **Title**: Punishment for cheating
- **Act**: Indian Penal Code
- **Section / Provision**: 417
- **Domain**: `criminal_law`
- **Source Type**: `statute`
- **Year**: 1860

```text
Act: Indian Penal Code
Section 417: Punishment for cheating

Whoever cheats shall be punished with imprisonment of either description for a term which may extend to one year, or with fine, or with both.
Simple cheating under Section 417 applies where there is deception without the aggravated inducement to deliver property or alter valuable securities (which is covered under Section 420).
```

### Constitutional Law: "What is Article 21?"
#### Rank 1 — L2 Distance: `48.2746`
- **Title**: Article 12 of Indian Constitution
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-110
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: Article 12 of Indian Constitution

(4) Nothing in this article shall apply to any amendment of this Constitution made under Article 368 Right of Equality
```
#### Rank 2 — L2 Distance: `48.3385`
- **Title**: Article 29 of Indian Constitution
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-127
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: Article 29 of Indian Constitution

(2) The state shall not, in granting aid to educational institutions, discriminate against any educational institution on the ground that it is under the management of a minority, whether based on religion or language
```
#### Rank 3 — L2 Distance: `48.5036`
- **Title**: Article 16 of Indian Constitution
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-114
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: Article 16 of Indian Constitution

Equality of opportunity in matters of public employment
(1) There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State
(2) No citizen shall, on grounds only of religion, race, caste, sex, descent, place of birth, residence or any of them, be ineligible for, or discriminated against in respect or, any employment or office under the State
```

### Constitutional Law: "What are Fundamental Rights?"
#### Rank 1 — L2 Distance: `52.6087`
- **Title**: What are the different types of writs?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-63
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the different types of writs?

. LastlyCertiorari is used to quash arbitrary orders or judgments and direct certification of records.
```
#### Rank 2 — L2 Distance: `54.6027`
- **Title**: Article 16 of Indian Constitution
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-114
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: Article 16 of Indian Constitution

Equality of opportunity in matters of public employment
(1) There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State
(2) No citizen shall, on grounds only of religion, race, caste, sex, descent, place of birth, residence or any of them, be ineligible for, or discriminated against in respect or, any employment or office under the State
```
#### Rank 3 — L2 Distance: `55.2014`
- **Title**: Article 15 of Indian Constitution
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-113
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: Article 15 of Indian Constitution

Article 16 of Indian Constitution,"Equality of opportunity in matters of public employment
(1) There shall be equality of opportunity for all citizens in matters relating to employment or appointment to any office under the State
(2) No citizen shall, on grounds only of religion, race, caste, sex, descent, place of birth, residence or any of them, be ineligible for, or discriminated against in respect or, any employment or office under the State
```

### Tenant Law: "What rights do tenants have?"
#### Rank 1 — L2 Distance: `41.4945`
- **Title**: What happens if a party fails to file pleadings in India within the prescribed time?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-25
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What happens if a party fails to file pleadings in India within the prescribed time?

. It's crucial for parties to adhere to the prescribed timelines for filing pleadings to avoid adverse consequences.
```
#### Rank 2 — L2 Distance: `42.3170`
- **Title**: What are the reports or statements which do not amount to be an FIR?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-51
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are the reports or statements which do not amount to be an FIR?

-Information to the Magistrate or police officer on phone.
-Information received at police station prior to the lodging of an F.LR.
```
#### Rank 3 — L2 Distance: `42.6657`
- **Title**: Right to essential services
- **Act**: Rent Control & Tenancy Law
- **Section / Provision**: Tenant Right 2
- **Domain**: `tenancy_law`
- **Source Type**: `statute`
- **Year**: 1948

```text
Act: Rent Control & Tenancy Law
Section Tenant Right 2: Right to essential services

Right to essential services: Landlords cannot cut off essential utilities like electricity, water supply, sewage, or gas to force a tenant to vacate.
```

### Tax Law: "Summarize CIT v A.W. Figgies."
#### Rank 1 — L2 Distance: `23.0463`
- **Title**: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
- **Act**: Income Tax Act 1922
- **Section / Provision**: Section 66(1) & Section 25(4)
- **Domain**: `tax_law`
- **Source Type**: `case_law`
- **Year**: 1953

```text
Case Law: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
Act: Income Tax Act 1922

Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others
Supreme Court of India
```
#### Rank 2 — L2 Distance: `23.6893`
- **Title**: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
- **Act**: Income Tax Act 1922
- **Section / Provision**: Section 66(1) & Section 25(4)
- **Domain**: `tax_law`
- **Source Type**: `case_law`
- **Year**: 1953

```text
Case Law: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
Act: Income Tax Act 1922

. To all intents and purposes the firm as reconstituted was not a different unit but it remained the same unit in spite of the change in its constitution.
```
#### Rank 3 — L2 Distance: `24.6788`
- **Title**: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
- **Act**: Income Tax Act 1922
- **Section / Provision**: Section 66(1) & Section 25(4)
- **Domain**: `tax_law`
- **Source Type**: `case_law`
- **Year**: 1953

```text
Case Law: Commissioner of Income Tax, West Bengal v A. W. Figgies and Company, and Others (1953 AIR 455)
Act: Income Tax Act 1922

2. The assessee is a partnership concern. When income-tax was paid under the Act of 1918, the partnership concern consisted of three partners, Mathews, Figgies and Notley. The name of the firm was A. W. Figgies & Co., and its' business was that of tea brokers. There were several changes in the constitution of the firm resulting in a change in the shares of the partners. In 1924, Mathews went out and his share was taken over by Figgies and Notley. In 1926 another partner Squire was introduced. In 1932 Figgies went out, and from 1932 to 1939 the partnership consisted only of Notley and Squire
```

### Evidence & Procedure: "What is evidence?"
#### Rank 1 — L2 Distance: `46.3216`
- **Title**: What is examination-in-chief?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-95
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What is examination-in-chief?

Examination-in-chief refers to the first stage of leading questions put to a witness by the party who calls the witnessto bring out the desired facts to establish its case. It is governed by the Indian Evidence Act1872. Leading questions are permissible at this stage. It helps bring out the witness’ account of relevant events before testing by opposite party.
```
#### Rank 2 — L2 Distance: `46.8632`
- **Title**: What happens if a party fails to file pleadings in India within the prescribed time?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-25
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What happens if a party fails to file pleadings in India within the prescribed time?

. It's crucial for parties to adhere to the prescribed timelines for filing pleadings to avoid adverse consequences.
```
#### Rank 3 — L2 Distance: `47.3151`
- **Title**: What happens if a witness list is not filed?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-94
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What happens if a witness list is not filed?

If a party does not submit the list of witnessesthen as per Order XVI Rule 1 of CPCno evidence shall be recorded of witnesses not mentioned in the list. Howeverexemption may be allowed if sufficient cause is shown like witnesses becoming suddenly available. Courts have discretion to allow unlisted witnesses to ensure fair and proper trial.
```

### Evidence & Procedure: "What is bail?"
#### Rank 1 — L2 Distance: `41.8072`
- **Title**: What is a bail application?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-57
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What is a bail application?

A bail application is a petition filed by an accused person requesting release from custody during the pendency of legal proceedings. It is filed in the court where the case is pending trial or appeal. The court has discretion to grant or deny bail based on criteria like flight risktampering with evidenceprevious criminal record etc.
```
#### Rank 2 — L2 Distance: `43.1993`
- **Title**: What is the procedure for filing a writ petition?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-66
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What is the procedure for filing a writ petition?

. Interim orders may be given for immediate relief. The entire process usually takes a few months from start to the final disposal through judgment.
```
#### Rank 3 — L2 Distance: `43.4317`
- **Title**: What are some common types of Interlocutory Applications filed in Indian courts?
- **Act**: Indian Law Q&A
- **Section / Provision**: QA-42
- **Domain**: `legal_qa`
- **Source Type**: `qa`
- **Year**: 2024

```text
Domain: Legal Q&A
Topic: What are some common types of Interlocutory Applications filed in Indian courts?

. Release of Property: Filed to seek the release of seized or attached property during the litigation.
```
