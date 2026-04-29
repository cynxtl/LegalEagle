import { Sparkles, User, Copy, ThumbsUp, ThumbsDown, Bookmark } from "lucide-react"
import type { Message } from "@/lib/legal-data"
import { ConfidenceBadge } from "./confidence-badge"
import { SourceCard } from "./source-card"
import { CategoryTag } from "./category-chips"
import { cn } from "@/lib/utils"

function formatContent(content: string) {
  // Simple markdown-ish rendering for **bold** and numbered lists
  const lines = content.split("\n")
  return lines.map((line, i) => {
    if (line.trim() === "") return <div key={i} className="h-2" />
    const parts = line.split(/(\*\*[^*]+\*\*)/g)
    const rendered = parts.map((part, j) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={j} className="font-semibold text-foreground">
            {part.slice(2, -2)}
          </strong>
        )
      }
      return <span key={j}>{part}</span>
    })
    return (
      <p key={i} className="leading-relaxed">
        {rendered}
      </p>
    )
  })
}

export function ChatMessage({ message }: { message: Message }) {
  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="flex max-w-[85%] items-start gap-3">
          <div className="rounded-2xl rounded-tr-md border border-border bg-card px-4 py-3 shadow-sm">
            <div className="mb-1 flex items-center gap-2 text-[10px] text-muted-foreground">
              {message.category && <CategoryTag category={message.category} />}
              <span className="font-mono">{message.timestamp}</span>
            </div>
            <p className="text-sm leading-relaxed">{message.content}</p>
          </div>
          <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-secondary ring-1 ring-border">
            <User className="size-3.5" />
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-3">
      <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20">
        <Sparkles className="size-3.5 text-primary" />
      </div>
      <div className="min-w-0 flex-1 space-y-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-medium">LegalEagle</span>
          <span className="font-mono text-[10px] text-muted-foreground">
            {message.timestamp}
          </span>
          {message.confidence && (
            <ConfidenceBadge level={message.confidence} />
          )}
          {message.category && <CategoryTag category={message.category} />}
        </div>

        <div className="prose prose-sm max-w-none space-y-2 text-sm text-foreground/90">
          {formatContent(message.content)}
        </div>

        {message.sources && message.sources.length > 0 && (
          <div className="space-y-2 pt-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                Cited sources
              </span>
              <div className="h-px flex-1 bg-border" />
            </div>
            <div className="grid gap-2 sm:grid-cols-2">
              {message.sources.map((src, i) => (
                <SourceCard
                  key={src.id}
                  source={src}
                  index={i}
                  variant="compact"
                />
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-1 pt-1">
          <MessageAction icon={Copy} label="Copy" />
          <MessageAction icon={Bookmark} label="Save" />
          <div className="mx-1 h-4 w-px bg-border" />
          <MessageAction icon={ThumbsUp} label="Helpful" />
          <MessageAction icon={ThumbsDown} label="Not helpful" />
        </div>
      </div>
    </div>
  )
}

function MessageAction({
  icon: Icon,
  label,
}: {
  icon: typeof Copy
  label: string
}) {
  return (
    <button
      type="button"
      aria-label={label}
      className={cn(
        "inline-flex size-7 items-center justify-center rounded-md text-muted-foreground transition-colors",
        "hover:bg-muted hover:text-foreground"
      )}
    >
      <Icon className="size-3.5" />
    </button>
  )
}
