"use client"

import * as React from "react"
import { ArrowUpRight, BookOpen, Gavel, Landmark, Scroll, Check, Star } from "lucide-react"
import type { Source } from "@/lib/legal-data"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const typeConfig = {
  case: { label: "Case Law", Icon: Gavel },
  statute: { label: "Statute", Icon: Landmark },
  regulation: { label: "Regulation", Icon: Scroll },
  commentary: { label: "Commentary", Icon: BookOpen },
  retrieved_chunk: { label: "Corpus Chunk", Icon: BookOpen },
} as const

export function SourceCard({
  source,
  index,
  className,
  variant = "default",
}: {
  source: Source
  index?: number
  className?: string
  variant?: "default" | "compact"
}) {
  const [showModal, setShowModal] = React.useState(false)
  const [copied, setCopied] = React.useState(false)
  const [isStarred, setIsStarred] = React.useState(Boolean((source as any).is_starred))

  const cfg = typeConfig[source.type] || typeConfig.statute
  const Icon = cfg.Icon

  const handleCopyCitation = (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    const citationText = source.citation
      ? `${source.title} (${source.citation}, ${source.year || 1950})`
      : `${source.title} (${source.jurisdiction || "Supreme Court of India"})`
    navigator.clipboard.writeText(citationText)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleToggleStar = async (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()
    const nextVal = !isStarred
    setIsStarred(nextVal)
    try {
      if (source.id) {
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
        await fetch(`${API_URL}/api/v1/sources/${source.id}/star`, {
          method: "POST",
        })
      }
    } catch (err) {
      console.error("Failed to toggle star:", err)
    }
  }

  if (variant === "compact") {
    return (
      <>
        <div
          onClick={() => setShowModal(true)}
          className={cn(
            "group flex cursor-pointer items-start gap-2.5 rounded-lg border border-border bg-card/40 px-3 py-2.5 transition-colors hover:border-primary/30 hover:bg-card",
            className
          )}
        >
          <div className="mt-0.5 flex size-6 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
            <Icon className="size-3" />
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-1.5">
              {index !== undefined && (
                <span className="font-mono text-[10px] text-muted-foreground">
                  [{index + 1}]
                </span>
              )}
              <p className="truncate text-xs font-medium">{source.title}</p>
            </div>
            <p className="truncate font-mono text-[10px] text-muted-foreground">
              {source.citation || source.jurisdiction}
            </p>
          </div>
          <ArrowUpRight className="size-3.5 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
        </div>

        <SourceDetailModal
          open={showModal}
          onOpenChange={setShowModal}
          source={source}
          index={index}
          onCopy={handleCopyCitation}
          copied={copied}
        />
      </>
    )
  }

  return (
    <>
      <article
        className={cn(
          "group rounded-xl border border-border bg-card/60 p-4 transition-all hover:border-primary/30 hover:shadow-sm",
          className
        )}
      >
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="flex size-7 items-center justify-center rounded-md bg-primary/10 text-primary">
              <Icon className="size-3.5" />
            </div>
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              {cfg.label}
            </span>
          </div>
          <div className="flex items-center gap-1.5">
            <button
              onClick={handleToggleStar}
              aria-label="Star citation"
              className={cn(
                "p-1 text-muted-foreground hover:text-amber-400 transition-colors",
                isStarred && "text-amber-400"
              )}
            >
              <Star className="size-3.5" fill={isStarred ? "currentColor" : "none"} />
            </button>
            {index !== undefined && (
              <span className="font-mono text-[10px] text-muted-foreground">
                [{index + 1}]
              </span>
            )}
          </div>
        </div>

        <h4 className="mt-3 font-serif text-base leading-tight tracking-tight text-balance">
          {source.title}
        </h4>

        <p className="mt-1 font-mono text-[11px] text-muted-foreground">
          {source.citation} · {source.jurisdiction} · {source.year || 1950}
        </p>

        <blockquote className="mt-3 border-l-2 border-accent/40 pl-3 text-xs leading-relaxed text-muted-foreground line-clamp-3">
          &ldquo;{source.excerpt}&rdquo;
        </blockquote>

        <div className="mt-4 flex items-center justify-between border-t border-border/60 pt-3">
          <button
            type="button"
            onClick={() => setShowModal(true)}
            className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
          >
            View source
            <ArrowUpRight className="size-3" />
          </button>
          <button
            type="button"
            onClick={handleCopyCitation}
            className="inline-flex items-center gap-1 text-[11px] text-muted-foreground hover:text-foreground"
          >
            {copied ? (
              <>
                <Check className="size-3 text-emerald-500" />
                <span className="text-emerald-500 font-medium">Copied!</span>
              </>
            ) : (
              "Cite this"
            )}
          </button>
        </div>
      </article>

      <SourceDetailModal
        open={showModal}
        onOpenChange={setShowModal}
        source={source}
        index={index}
        onCopy={handleCopyCitation}
        copied={copied}
      />
    </>
  )
}

function SourceDetailModal({
  open,
  onOpenChange,
  source,
  index,
  onCopy,
  copied,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
  source: Source
  index?: number
  onCopy: (e: React.MouseEvent) => void
  copied: boolean
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <div className="flex items-center gap-2">
            <span className="font-mono text-[10px] uppercase tracking-wider text-primary">
              Citation Provenance
            </span>
            {index !== undefined && (
              <span className="font-mono text-[10px] text-muted-foreground">
                Source #{index + 1}
              </span>
            )}
          </div>
          <DialogTitle className="font-serif text-lg leading-snug">
            {source.title}
          </DialogTitle>
          <DialogDescription className="font-mono text-xs text-muted-foreground">
            {source.citation} · {source.jurisdiction} · {source.year || 1950}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4 py-2">
          <div className="rounded-xl border border-border bg-card/60 p-4">
            <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              Statutory Passage / Retrieved Excerpt
            </span>
            <div className="mt-2 max-h-60 overflow-y-auto rounded-lg bg-background/80 p-3 font-mono text-xs leading-relaxed text-foreground/90 whitespace-pre-wrap">
              {source.excerpt}
            </div>
          </div>

          <div className="flex items-center justify-between pt-2">
            <Button
              variant="outline"
              size="sm"
              onClick={onCopy}
              className="gap-1.5 text-xs"
            >
              {copied ? (
                <>
                  <Check className="size-3.5 text-emerald-500" />
                  Copied Citation
                </>
              ) : (
                "Copy Legal Citation"
              )}
            </Button>
            <Button size="sm" onClick={() => onOpenChange(false)}>
              Close
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
