"use client"

import {
  FileText,
  Search,
  MoreHorizontal,
  CheckCircle2,
  Clock,
  AlertCircle,
  Sparkles,
  Highlighter,
  ListChecks,
  ShieldAlert,
} from "lucide-react"
import { useState } from "react"
import { DocumentUploadCard } from "@/components/legal/document-upload-card"
import { DisclaimerBanner } from "@/components/legal/disclaimer-banner"
import { CategoryTag } from "@/components/legal/category-chips"
import { ConfidenceBadge } from "@/components/legal/confidence-badge"
import { sampleDocs } from "@/lib/legal-data"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { useDocumentUpload } from "@/hooks/use-document-upload"

export default function DocumentsPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedDoc, setSelectedDoc] = useState(sampleDocs[0])
  const { files, removeFile } = useDocumentUpload(sampleDocs)

  const filteredDocs = files.filter(
    (doc) =>
      doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.category.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <main className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-6xl px-4 py-8 lg:px-8 lg:py-10">
        <PageHeader searchQuery={searchQuery} onSearchChange={setSearchQuery} />

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_360px]">
          <div className="space-y-6">
            <DocumentUploadCard />
            <DocList docs={filteredDocs} onSelectDoc={setSelectedDoc} onRemoveDoc={removeFile} />
          </div>
          <div className="space-y-6">
            <ActiveDocAnalysis doc={selectedDoc} />
            <ExtractedClauses />
          </div>
        </div>
      </div>
    </main>
  )
}

function PageHeader({
  searchQuery,
  onSearchChange,
}: {
  searchQuery: string
  onSearchChange: (query: string) => void
}) {
  return (
    <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
          Document analysis
        </span>
        <h1 className="mt-1 font-serif text-3xl tracking-tight md:text-4xl">
          Your private legal corpus.
        </h1>
        <p className="mt-1.5 max-w-xl text-sm text-muted-foreground">
          Upload contracts, judgments, and filings. LegalEagle indexes them
          privately and answers questions grounded in your documents.
        </p>
      </div>
      <div className="flex gap-2">
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search documents..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="h-9 w-64 rounded-full border-border bg-card/50 pl-9 text-sm"
          />
        </div>
      </div>
    </div>
  )
}

const statusConfig = {
  indexed: {
    label: "Indexed",
    Icon: CheckCircle2,
    color: "text-primary",
    bg: "bg-primary/10",
  },
  processing: {
    label: "Processing",
    Icon: Clock,
    color: "text-accent",
    bg: "bg-accent/10",
  },
  failed: {
    label: "Failed",
    Icon: AlertCircle,
    color: "text-destructive",
    bg: "bg-destructive/10",
  },
} as const

function DocList({
  docs,
  onSelectDoc,
  onRemoveDoc,
}: {
  docs: typeof sampleDocs
  onSelectDoc: (doc: typeof sampleDocs[0]) => void
  onRemoveDoc: (id: string) => void
}) {
  return (
    <section className="rounded-2xl border border-border bg-card/40">
      <div className="flex items-center justify-between border-b border-border/60 px-5 py-3.5">
        <div>
          <h2 className="font-serif text-base tracking-tight">
            Uploaded documents
          </h2>
          <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            {docs.length} files · 7.6 MB total
          </p>
        </div>
        <Button variant="ghost" size="sm" className="h-8 text-xs">
          Sort: Recent
        </Button>
      </div>
      <ul className="divide-y divide-border/60">
        {docs.map((doc) => {
          const cfg = statusConfig[doc.status]
          const Icon = cfg.Icon
          return (
            <li
              key={doc.id}
              onClick={() => onSelectDoc(doc)}
              className="group flex cursor-pointer items-center gap-4 px-5 py-3.5 transition-colors hover:bg-muted/30"
            >
              <div className="flex size-10 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
                <FileText className="size-4" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <p className="truncate text-sm font-medium">{doc.name}</p>
                  <CategoryTag category={doc.category} />
                </div>
                <p className="mt-0.5 font-mono text-[10px] text-muted-foreground">
                  {doc.size} · {doc.pages} pages · {doc.uploadedAt}
                </p>
              </div>
              <div
                className={cn(
                  "inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[10px] font-medium",
                  cfg.bg,
                  cfg.color
                )}
              >
                <Icon className="size-3" />
                {cfg.label}
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  onRemoveDoc(doc.id)
                }}
                aria-label="Delete document"
                className="hidden size-8 items-center justify-center rounded-md text-muted-foreground hover:bg-destructive/10 hover:text-destructive sm:flex"
              >
                <MoreHorizontal className="size-4" />
              </button>
            </li>
          )
        })}
      </ul>
    </section>
  )
}

function ActiveDocAnalysis({
  doc,
}: {
  doc: typeof sampleDocs[0]
}) {
  return (
    <section className="rounded-2xl border border-border bg-card/60 p-5">
      <div className="flex items-center gap-2">
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
          Now analyzing
        </span>
        <div className="h-px flex-1 bg-border" />
      </div>

      <div className="mt-3 flex items-start gap-3">
        <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
          <FileText className="size-4" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium">
            {doc.name}
          </p>
          <p className="font-mono text-[10px] text-muted-foreground">
            18 pages · indexed 9:12 AM
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        <SummaryRow
          icon={Sparkles}
          label="AI summary"
          value="Standard residential lease with 11-month term, 2-month security deposit, and break clause after 6 months."
          confidence="high"
        />
        <SummaryRow
          icon={ListChecks}
          label="Key parties"
          value="Lessor: Mehta Properties LLP · Lessee: Anjali Verma · Witnesses: 2"
        />
        <SummaryRow
          icon={ShieldAlert}
          label="Risk flags"
          value="Section 7.3 (rent escalation) lacks an upper bound. Consider negotiation."
          confidence="medium"
        />
      </div>

      <div className="mt-5 flex gap-2">
        <Button size="sm" className="flex-1 gap-1.5">
          <Sparkles className="size-3.5" />
          Ask about this doc
        </Button>
        <Button size="sm" variant="outline" className="bg-card/50">
          Export
        </Button>
      </div>
    </section>
  )
}

function SummaryRow({
  icon: Icon,
  label,
  value,
  confidence,
}: {
  icon: typeof Sparkles
  label: string
  value: string
  confidence?: "high" | "medium" | "low"
}) {
  return (
    <div className="rounded-lg border border-border bg-background/40 p-3">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5">
          <Icon className="size-3.5 text-primary" />
          <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            {label}
          </span>
        </div>
        {confidence && <ConfidenceBadge level={confidence} />}
      </div>
      <p className="mt-2 text-xs leading-relaxed text-foreground/90">
        {value}
      </p>
    </div>
  )
}

function ExtractedClauses() {
  const clauses = [
    {
      title: "Termination",
      section: "§ 9",
      excerpt:
        "Either party may terminate with 60 days written notice after the initial 6-month lock-in.",
    },
    {
      title: "Rent escalation",
      section: "§ 7.3",
      excerpt:
        "Annual rent increase as mutually agreed; no statutory cap specified.",
      flag: true,
    },
    {
      title: "Security deposit",
      section: "§ 4",
      excerpt:
        "Refundable within 30 days of vacating, less reasonable deductions.",
    },
  ]

  return (
    <section className="rounded-2xl border border-border bg-card/60 p-5">
      <div className="mb-4 flex items-center gap-2">
        <Highlighter className="size-3.5 text-accent" />
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
          Extracted clauses
        </span>
      </div>
      <ul className="space-y-2.5">
        {clauses.map((c) => (
          <li
            key={c.section}
            className={cn(
              "rounded-lg border bg-background/40 p-3",
              c.flag ? "border-accent/30" : "border-border"
            )}
          >
            <div className="flex items-baseline justify-between gap-2">
              <p className="text-xs font-medium">{c.title}</p>
              <span className="font-mono text-[10px] text-accent">
                {c.section}
              </span>
            </div>
            <p className="mt-1.5 text-[11px] leading-relaxed text-muted-foreground">
              {c.excerpt}
            </p>
          </li>
        ))}
      </ul>

      <div className="mt-4">
        <DisclaimerBanner variant="compact" />
      </div>
    </section>
  )
}
