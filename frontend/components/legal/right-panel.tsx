"use client"

import {
  Landmark,
  Gavel,
  FileText,
  AlertTriangle,
  ListChecks,
} from "lucide-react"
import type { Source } from "@/lib/legal-data"
import { SourceCard } from "./source-card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"

export function RightPanel({
  sources = [],
  confidence = "medium",
  className,
}: {
  sources?: Source[]
  confidence?: string
  className?: string
}) {
  const displaySources = sources

  return (
    <aside
      className={cn(
        "fixed right-0 top-0 hidden h-svh w-[360px] flex-col border-l border-border bg-card/30 xl:flex",
        className
      )}
    >
      <div className="border-b border-border px-5 py-4">
        <div>
          <h2 className="font-serif text-base tracking-tight">
            Research panel
          </h2>
          <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            Live citations · current query
          </p>
        </div>
      </div>

      <Tabs defaultValue="sources" className="flex flex-1 flex-col overflow-hidden">
        <TabsList className="mx-5 grid h-9 grid-cols-3 bg-muted/40">
          <TabsTrigger value="sources" className="text-xs">
            Sources
          </TabsTrigger>
          <TabsTrigger value="acts" className="text-xs">
            Confidence
          </TabsTrigger>
          <TabsTrigger value="summary" className="text-xs">
            Notes
          </TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-y-auto">
          <TabsContent
            value="sources"
            className="px-5 py-4"
          >
            <SectionHeader
              icon={Gavel}
              label="Retrieved Citations"
              count={displaySources.length}
            />

            {displaySources.length === 0 ? (
              <div className="rounded-xl border border-border bg-card/40 p-6 text-center">
                <p className="text-xs text-muted-foreground">
                  No citations yet. Ask a legal question to retrieve verified source passages from the FAISS legal database.
                </p>
              </div>
            ) : (
              <div className="space-y-2.5">
                {displaySources.map((src, i) => (
                  <SourceCard key={src.id || i} source={src} index={i} />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="acts" className="px-5 py-4">
            <SectionHeader icon={Landmark} label="Retrieval Confidence" />
            <div className="rounded-xl border border-border bg-card/40 p-4">
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium">Model Confidence</span>
                <span
                  className={cn(
                    "rounded px-2 py-0.5 font-mono text-xs font-semibold capitalize",
                    confidence === "high"
                      ? "bg-emerald-500/10 text-emerald-500"
                      : confidence === "medium"
                      ? "bg-amber-500/10 text-amber-500"
                      : "bg-rose-500/10 text-rose-500"
                  )}
                >
                  {confidence}
                </span>
              </div>
              <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
                Confidence is derived from vector embedding cosine/L2 distances between your query and indexed legal corpus chunks.
              </p>
            </div>
          </TabsContent>

          <TabsContent
            value="summary"
            className="px-5 py-4"
          >
            <SectionHeader icon={AlertTriangle} label="Statutory Caution" />
            <div className="space-y-2">
              <div className="rounded-lg border border-accent/30 bg-accent/5 p-3">
                <p className="text-[11px] font-medium text-accent-foreground">
                  Indian Legal Corpus
                </p>
                <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                  Responses are strictly grounded in retrieved FAISS passages from Indian statutes, court judgments, and legal precedents.
                </p>
              </div>
              <div className="rounded-lg border border-border bg-card/40 p-3">
                <p className="text-[11px] font-medium">Verification Mandatory</p>
                <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                  Always verify cited sections and precedents before drafting court submissions or advisory opinions.
                </p>
              </div>
            </div>
          </TabsContent>
        </div>
      </Tabs>
    </aside>
  )
}

function SectionHeader({
  icon: Icon,
  label,
  count,
}: {
  icon: typeof Gavel
  label: string
  count?: number
}) {
  return (
    <div className="mb-3 mt-4 flex items-center gap-2">
      <Icon className="size-3.5 text-primary" />
      <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
        {label}
      </span>
      {count !== undefined && (
        <span className="font-mono text-[10px] text-muted-foreground">
          · {count}
        </span>
      )}
      <div className="h-px flex-1 bg-border" />
    </div>
  )
}
