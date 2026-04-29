"use client"

import * as React from "react"
import { Paperclip, ArrowUp, Trash2, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const suggestions = [
  "Summarize this contract",
  "Find precedents for...",
  "Explain Section 498A",
  "Draft a legal notice",
]

export function ChatInput({
  className,
  onClear,
  onSubmit,
  disabled = false,
}: {
  className?: string
  onClear?: () => void
  onSubmit?: (message: string) => Promise<void> | void
  disabled?: boolean
}) {
  const [value, setValue] = React.useState("")
  const [isSubmitting, setIsSubmitting] = React.useState(false)
  const ref = React.useRef<HTMLTextAreaElement>(null)

  React.useEffect(() => {
    if (ref.current) {
      ref.current.style.height = "auto"
      ref.current.style.height = Math.min(ref.current.scrollHeight, 180) + "px"
    }
  }, [value])

  const handleSubmit = async () => {
    if (!value.trim() || isSubmitting || disabled) return

    setIsSubmitting(true)
    try {
      await onSubmit?.(value)
      setValue("")
      if (ref.current) {
        ref.current.style.height = "auto"
      }
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className={cn("space-y-2", className)}>
      <div className="flex flex-wrap gap-1.5">
        {suggestions.map((s) => (
          <button
            key={s}
            type="button"
            onClick={() => setValue(s)}
            className="inline-flex items-center gap-1 rounded-full border border-border bg-card/50 px-2.5 py-1 text-[11px] text-muted-foreground transition-colors hover:border-primary/30 hover:bg-primary/5 hover:text-foreground"
          >
            <Sparkles className="size-2.5 text-accent" />
            {s}
          </button>
        ))}
      </div>

      <div className="rounded-2xl border border-border bg-card/80 shadow-sm transition-colors focus-within:border-primary/40 focus-within:ring-1 focus-within:ring-primary/20">
        <textarea
          ref={ref}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder="Ask a legal question, paste a clause, or describe a situation..."
          className="block w-full resize-none border-0 bg-transparent px-4 py-3.5 text-sm leading-relaxed placeholder:text-muted-foreground/70 focus:outline-none disabled:opacity-50"
          disabled={isSubmitting || disabled}
        />
        <div className="flex items-center justify-between gap-2 border-t border-border/60 px-2 py-2">
          <div className="flex items-center gap-0.5">
            <button
              type="button"
              aria-label="Attach file"
              className="inline-flex size-8 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground disabled:opacity-50"
              disabled={isSubmitting || disabled}
            >
              <Paperclip className="size-4" />
            </button>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClear}
              className="h-8 gap-1.5 px-2 text-xs text-muted-foreground hover:text-destructive disabled:opacity-50"
              disabled={isSubmitting || disabled}
            >
              <Trash2 className="size-3.5" />
              Clear
            </Button>
          </div>
          <div className="flex items-center gap-2">
            <span className="hidden font-mono text-[10px] text-muted-foreground sm:inline">
              Enter to send
            </span>
            <Button
              type="button"
              size="sm"
              onClick={handleSubmit}
              disabled={!value.trim() || isSubmitting || disabled}
              className="h-8 gap-1.5 rounded-lg px-3"
            >
              {isSubmitting ? "Sending..." : "Send"}
              <ArrowUp className="size-3.5" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
