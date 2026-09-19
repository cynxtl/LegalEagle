"use client"

import {
  FileText,
  Search,
  CheckCircle2,
  Clock,
  AlertCircle,
  Sparkles,
  ListChecks,
  ShieldAlert,
  Trash2,
  RefreshCw,
  Eye,
} from "lucide-react"
import { useState } from "react"
import Link from "next/link"
import { DocumentUploadCard } from "@/components/legal/document-upload-card"
import { CategoryTag } from "@/components/legal/category-chips"
import { ConfidenceBadge } from "@/components/legal/confidence-badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog"
import { cn } from "@/lib/utils"
import { useDocumentUpload } from "@/hooks/use-document-upload"
import type { UploadedDoc } from "@/lib/legal-data"

export default function DocumentsPage() {
  const [searchQuery, setSearchQuery] = useState("")
  const { files, removeFile, fetchDocuments } = useDocumentUpload([])
  const [selectedDocId, setSelectedDocId] = useState<string | null>(null)
  const [viewingDoc, setViewingDoc] = useState<UploadedDoc | null>(null)
  const [isRefreshing, setIsRefreshing] = useState(false)

  const selectedDoc = files.find((f) => f.id === selectedDocId) || files[0] || null

  const handleRefresh = async () => {
    setIsRefreshing(true)
    await fetchDocuments()
    setTimeout(() => setIsRefreshing(false), 500)
  }

  const filteredDocs = files.filter(
    (doc) =>
      doc.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      doc.category.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <main className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-6xl px-4 py-8 lg:px-8 lg:py-10">
        <PageHeader
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
        />

        <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_360px]">
          <div className="space-y-6">
            <DocumentUploadCard onUploadSuccess={fetchDocuments} />
            <DocList
              docs={filteredDocs}
              selectedId={selectedDoc?.id || null}
              onSelectDoc={(doc) => setSelectedDocId(doc.id)}
              onViewDoc={(doc) => setViewingDoc(doc)}
              onRemoveDoc={removeFile}
            />
          </div>
          <div className="space-y-6">
            <ActiveDocAnalysis
              doc={selectedDoc}
              onViewDetails={() => setViewingDoc(selectedDoc)}
            />
          </div>
        </div>
      </div>

      {/* Document View Details Modal */}
      <Dialog open={Boolean(viewingDoc)} onOpenChange={(open) => !open && setViewingDoc(null)}>
        <DialogContent className="max-w-xl">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 font-serif text-lg">
              <FileText className="size-5 text-primary" />
              {viewingDoc?.name}
            </DialogTitle>
            <DialogDescription className="font-mono text-xs text-muted-foreground">
              Document ID: {viewingDoc?.id} · {viewingDoc?.uploadedAt}
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="rounded-lg border border-border bg-card/60 p-3">
                <span className="text-muted-foreground">Category</span>
                <p className="mt-1 font-medium">{viewingDoc?.category || "General Legal"}</p>
              </div>
              <div className="rounded-lg border border-border bg-card/60 p-3">
                <span className="text-muted-foreground">File Size</span>
                <p className="mt-1 font-medium">{viewingDoc?.size}</p>
              </div>
              <div className="rounded-lg border border-border bg-card/60 p-3">
                <span className="text-muted-foreground">Status</span>
                <p className="mt-1 font-medium text-emerald-500 uppercase font-mono text-[10px]">
                  {viewingDoc?.status || "Indexed"}
                </p>
              </div>
              <div className="rounded-lg border border-border bg-card/60 p-3">
                <span className="text-muted-foreground">Pages / Scope</span>
                <p className="mt-1 font-medium">{viewingDoc?.pages || 1} pages</p>
              </div>
            </div>

            <div className="rounded-xl border border-border bg-background/50 p-4">
              <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                Corpus Indexing Summary
              </span>
              <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                This document has been tokenized, split using recursive chunking with 100-character overlap, and embedded into the local FAISS index using <code className="text-primary font-mono text-[11px]">law-ai/InLegalBERT</code> (768 dimensions). Its passages are immediately eligible for similarity retrieval during legal consultations.
              </p>
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <Button variant="outline" size="sm" onClick={() => setViewingDoc(null)}>
                Close
              </Button>
              <Button asChild size="sm" className="gap-1.5">
                <Link href="/chat">
                  <Sparkles className="size-3.5" />
                  Query in Consultation
                </Link>
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </main>
  )
}

function PageHeader({
  searchQuery,
  onSearchChange,
  onRefresh,
  isRefreshing,
}: {
  searchQuery: string
  onSearchChange: (query: string) => void
  onRefresh: () => void
  isRefreshing: boolean
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
          Upload contracts, judgments, and statutory filings. LegalEagle indexes them
          privately into FAISS and answers questions grounded in your documents.
        </p>
      </div>
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={onRefresh}
          disabled={isRefreshing}
          className="h-9 gap-1.5 rounded-full border-border bg-card/50 text-xs"
        >
          <RefreshCw className={cn("size-3.5", isRefreshing && "animate-spin")} />
          Refresh
        </Button>
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
  selectedId,
  onSelectDoc,
  onViewDoc,
  onRemoveDoc,
}: {
  docs: UploadedDoc[]
  selectedId: string | null
  onSelectDoc: (doc: UploadedDoc) => void
  onViewDoc: (doc: UploadedDoc) => void
  onRemoveDoc: (id: string) => void
}) {
  return (
    <section className="rounded-2xl border border-border bg-card/40">
      <div className="flex items-center justify-between border-b border-border/60 px-5 py-3.5">
        <div>
          <h2 className="font-serif text-base tracking-tight">
            Indexed documents
          </h2>
          <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            {docs.length} files in SQLite vector corpus
          </p>
        </div>
      </div>

      {docs.length === 0 ? (
        <div className="px-6 py-12 text-center">
          <FileText className="mx-auto size-8 text-muted-foreground/50" />
          <p className="mt-2 text-sm font-medium">No documents uploaded yet</p>
          <p className="mt-1 text-xs text-muted-foreground">
            Upload PDF, DOCX, or TXT files above to add them to your private FAISS vector store.
          </p>
        </div>
      ) : (
        <ul className="divide-y divide-border/60">
          {docs.map((doc) => {
            const cfg = statusConfig[doc.status as keyof typeof statusConfig] || statusConfig.indexed
            const Icon = cfg.Icon
            const isSelected = doc.id === selectedId
            return (
              <li
                key={doc.id}
                onClick={() => onSelectDoc(doc)}
                className={cn(
                  "group flex cursor-pointer items-center gap-4 px-5 py-3.5 transition-colors hover:bg-muted/30",
                  isSelected && "bg-muted/40"
                )}
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
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onViewDoc(doc)
                    }}
                    aria-label="View document details"
                    className="size-8 flex items-center justify-center rounded-md text-muted-foreground hover:bg-muted hover:text-foreground"
                  >
                    <Eye className="size-3.5" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      onRemoveDoc(doc.id)
                    }}
                    aria-label="Delete document"
                    className="size-8 flex items-center justify-center rounded-md text-muted-foreground hover:bg-destructive/10 hover:text-destructive"
                  >
                    <Trash2 className="size-3.5" />
                  </button>
                </div>
              </li>
            )
          })}
        </ul>
      )}
    </section>
  )
}

function ActiveDocAnalysis({
  doc,
  onViewDetails,
}: {
  doc: UploadedDoc | null
  onViewDetails?: () => void
}) {
  if (!doc) {
    return (
      <section className="rounded-2xl border border-border bg-card/60 p-6 text-center">
        <p className="text-xs text-muted-foreground">
          Select or upload a document to view indexed details and corpus grounding.
        </p>
      </section>
    )
  }

  return (
    <section className="rounded-2xl border border-border bg-card/60 p-5">
      <div className="flex items-center gap-2">
        <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
          Active Document
        </span>
        <div className="h-px flex-1 bg-border" />
      </div>

      <div className="mt-3 flex items-start gap-3">
        <div className="flex size-10 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
          <FileText className="size-4" />
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium">{doc.name}</p>
          <p className="font-mono text-[10px] text-muted-foreground">
            {doc.pages} pages · {doc.size} · {doc.uploadedAt}
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        <SummaryRow
          icon={Sparkles}
          label="Corpus Status"
          value="Indexed in FAISS vector store. Text chunks are available for semantic similarity retrieval in consultations."
          confidence="high"
        />
        <SummaryRow
          icon={ListChecks}
          label="Document Classification"
          value={`Categorized under ${doc.category || "General Legal"}. Chunks extracted with 1000-char window and 100-char overlap.`}
        />
        <SummaryRow
          icon={ShieldAlert}
          label="Privacy Guarantee"
          value="Stored locally on this server. Document chunks are processed strictly offline by local InLegalBERT embeddings."
          confidence="high"
        />
      </div>

      <div className="mt-5 flex gap-2">
        <Button
          variant="outline"
          size="sm"
          className="gap-1.5"
          onClick={onViewDetails}
        >
          <Eye className="size-3.5" />
          View Details
        </Button>
        <Button asChild size="sm" className="flex-1 gap-1.5">
          <Link href={`/chat?prompt=${encodeURIComponent(`Analyze the key legal implications and provisions in ${doc.name}`)}`}>
            <Sparkles className="size-3.5" />
            Query this document
          </Link>
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
    <div className="rounded-xl border border-border/70 bg-background/50 p-3">
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-1.5 text-muted-foreground">
          <Icon className="size-3.5 text-primary" />
          <span className="font-mono text-[10px] uppercase tracking-wider">
            {label}
          </span>
        </div>
        {confidence && <ConfidenceBadge level={confidence} />}
      </div>
      <p className="mt-1.5 text-xs leading-relaxed text-foreground">{value}</p>
    </div>
  )
}
