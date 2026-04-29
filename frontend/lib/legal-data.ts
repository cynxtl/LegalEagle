export type LegalCategory =
  | "Criminal Law"
  | "Family Law"
  | "Property"
  | "Constitution"
  | "Procedure"
  | "Contract"
  | "Tax"
  | "Employment"

export type Confidence = "high" | "medium" | "low"

export type Source = {
  id: string
  title: string
  citation: string
  jurisdiction: string
  year: number
  excerpt: string
  url?: string
  type: "case" | "statute" | "regulation" | "commentary"
}

export type Message = {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: string
  sources?: Source[]
  confidence?: Confidence
  category?: LegalCategory
}

export type ChatThread = {
  id: string
  title: string
  category: LegalCategory
  updatedAt: string
  preview: string
}

export type UploadedDoc = {
  id: string
  name: string
  size: string
  pages: number
  uploadedAt: string
  status: "indexed" | "processing" | "failed"
  category: LegalCategory
}

export const categories: LegalCategory[] = [
  "Criminal Law",
  "Family Law",
  "Property",
  "Constitution",
  "Procedure",
  "Contract",
  "Tax",
  "Employment",
]

export const sampleSources: Source[] = [
  {
    id: "src-1",
    type: "case",
    title: "Maneka Gandhi v. Union of India",
    citation: "(1978) 1 SCC 248",
    jurisdiction: "Supreme Court of India",
    year: 1978,
    excerpt:
      "The procedure prescribed by law for depriving a person of his life or personal liberty must be 'right, just and fair' and not arbitrary, fanciful or oppressive.",
  },
  {
    id: "src-2",
    type: "statute",
    title: "Article 21, Constitution of India",
    citation: "Const. of India, art. 21",
    jurisdiction: "Constituent Assembly",
    year: 1950,
    excerpt:
      "No person shall be deprived of his life or personal liberty except according to procedure established by law.",
  },
  {
    id: "src-3",
    type: "case",
    title: "Kesavananda Bharati v. State of Kerala",
    citation: "(1973) 4 SCC 225",
    jurisdiction: "Supreme Court of India",
    year: 1973,
    excerpt:
      "Parliament has wide powers to amend the Constitution but cannot alter its 'basic structure'.",
  },
  {
    id: "src-4",
    type: "statute",
    title: "Section 498A, Indian Penal Code",
    citation: "IPC § 498A",
    jurisdiction: "Parliament of India",
    year: 1983,
    excerpt:
      "Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years.",
  },
]

export const sampleThreads: ChatThread[] = [
  {
    id: "t-1",
    title: "Tenant rights under Rent Control Act",
    category: "Property",
    updatedAt: "2 min ago",
    preview: "Can a landlord evict a tenant without notice if rent is...",
  },
  {
    id: "t-2",
    title: "Section 498A — false complaint defense",
    category: "Criminal Law",
    updatedAt: "1 hr ago",
    preview: "What precedents exist for quashing of FIR under...",
  },
  {
    id: "t-3",
    title: "GST input credit on capital goods",
    category: "Tax",
    updatedAt: "Yesterday",
    preview: "Eligibility criteria under CGST Act, 2017 for...",
  },
  {
    id: "t-4",
    title: "Custody dispute — welfare principle",
    category: "Family Law",
    updatedAt: "2 days ago",
    preview: "Recent Supreme Court guidelines on child custody...",
  },
  {
    id: "t-5",
    title: "Force majeure in commercial leases",
    category: "Contract",
    updatedAt: "Last week",
    preview: "Post-pandemic interpretation of frustration of contract...",
  },
  {
    id: "t-6",
    title: "Article 14 — reasonable classification",
    category: "Constitution",
    updatedAt: "Last week",
    preview: "Twin-test for equal protection challenges...",
  },
]

export const sampleMessages: Message[] = [
  {
    id: "m-1",
    role: "user",
    content:
      "If a landlord wants to evict a tenant for non-payment of rent, what is the legal procedure under the Rent Control Act?",
    timestamp: "10:42 AM",
    category: "Property",
  },
  {
    id: "m-2",
    role: "assistant",
    timestamp: "10:42 AM",
    confidence: "high",
    category: "Property",
    content:
      "Under most state Rent Control Acts, a landlord cannot evict a tenant without due process. The general procedure involves three stages:\n\n1. **Statutory notice** — A written demand for arrears must be served, typically giving 15–30 days to cure the default.\n2. **Filing a petition** — If unpaid, the landlord must file an eviction petition before the Rent Controller, not a civil court.\n3. **Adjudication** — The tenant has a right to deposit arrears with interest before final order. Eviction is granted only if the tenant fails to pay or contest validly.\n\nKey safeguards apply: tenants who deposit arrears within the prescribed time are typically protected from eviction (the 'protection from eviction' principle). Self-help eviction — changing locks, cutting utilities — is illegal and can attract criminal liability.",
    sources: [sampleSources[0], sampleSources[1]],
  },
  {
    id: "m-3",
    role: "user",
    content:
      "What if the tenant has been there for 20 years? Does adverse possession apply?",
    timestamp: "10:44 AM",
    category: "Property",
  },
  {
    id: "m-4",
    role: "assistant",
    timestamp: "10:44 AM",
    confidence: "medium",
    category: "Property",
    content:
      "Adverse possession does **not** apply to a tenant in possession with the landlord's permission. The Supreme Court has consistently held that possession must be 'hostile, open, and continuous' against the true owner — a tenancy is by definition permissive.\n\nHowever, long-term tenants may acquire stronger statutory protections under specific Rent Control Acts (e.g., heritable tenancy rights, restrictions on grounds of eviction). The exact entitlements depend on your jurisdiction and whether the property is residential or commercial.",
    sources: [sampleSources[2]],
  },
]

export const sampleDocs: UploadedDoc[] = [
  {
    id: "d-1",
    name: "Lease_Agreement_2024.pdf",
    size: "2.4 MB",
    pages: 18,
    uploadedAt: "Today, 9:12 AM",
    status: "indexed",
    category: "Property",
  },
  {
    id: "d-2",
    name: "Employment_Contract_Draft_v3.docx",
    size: "412 KB",
    pages: 7,
    uploadedAt: "Yesterday",
    status: "indexed",
    category: "Employment",
  },
  {
    id: "d-3",
    name: "FIR_Copy_Section498A.pdf",
    size: "1.1 MB",
    pages: 4,
    uploadedAt: "3 days ago",
    status: "indexed",
    category: "Criminal Law",
  },
  {
    id: "d-4",
    name: "Partnership_Deed_FY24.pdf",
    size: "3.7 MB",
    pages: 22,
    uploadedAt: "Last week",
    status: "processing",
    category: "Contract",
  },
]
