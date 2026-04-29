import { ArrowUpRight, BookOpen, Gavel, Landmark, Scroll } from "lucide-react"
import type { Source } from "@/lib/legal-data"
import { cn } from "@/lib/utils"

const typeConfig = {
  case: { label: "Case Law", Icon: Gavel },
  statute: { label: "Statute", Icon: Landmark },
  regulation: { label: "Regulation", Icon: Scroll },
  commentary: { label: "Commentary", Icon: BookOpen },
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
  const cfg = typeConfig[source.type]
  const Icon = cfg.Icon

  if (variant === "compact") {
    return (
      <a
        href={source.url ?? "#"}
        className={cn(
          "group flex items-start gap-2.5 rounded-lg border border-border bg-card/40 px-3 py-2.5 transition-colors hover:border-primary/30 hover:bg-card",
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
            {source.citation}
          </p>
        </div>
        <ArrowUpRight className="size-3.5 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
      </a>
    )
  }

  return (
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
        {index !== undefined && (
          <span className="font-mono text-[10px] text-muted-foreground">
            [{index + 1}]
          </span>
        )}
      </div>

      <h4 className="mt-3 font-serif text-base leading-tight tracking-tight text-balance">
        {source.title}
      </h4>

      <p className="mt-1 font-mono text-[11px] text-muted-foreground">
        {source.citation} · {source.jurisdiction} · {source.year}
      </p>

      <blockquote className="mt-3 border-l-2 border-accent/40 pl-3 text-xs leading-relaxed text-muted-foreground">
        &ldquo;{source.excerpt}&rdquo;
      </blockquote>

      <div className="mt-4 flex items-center justify-between border-t border-border/60 pt-3">
        <a
          href={source.url ?? "#"}
          className="inline-flex items-center gap-1 text-xs font-medium text-primary hover:underline"
        >
          View source
          <ArrowUpRight className="size-3" />
        </a>
        <button
          type="button"
          className="text-[11px] text-muted-foreground hover:text-foreground"
        >
          Cite this
        </button>
      </div>
    </article>
  )
}
