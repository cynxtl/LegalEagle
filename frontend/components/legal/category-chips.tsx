"use client"

import * as React from "react"
import type { LegalCategory } from "@/lib/legal-data"
import { cn } from "@/lib/utils"

export function CategoryChips({
  categories,
  value,
  onChange,
  className,
}: {
  categories: readonly LegalCategory[]
  value?: LegalCategory | null
  onChange?: (cat: LegalCategory | null) => void
  className?: string
}) {
  const [internal, setInternal] = React.useState<LegalCategory | null>(
    value ?? null
  )
  const selected = value !== undefined ? value : internal

  const toggle = (cat: LegalCategory) => {
    const next = selected === cat ? null : cat
    setInternal(next)
    onChange?.(next)
  }

  return (
    <div className={cn("flex flex-wrap gap-1.5", className)}>
      {categories.map((cat) => {
        const active = selected === cat
        return (
          <button
            key={cat}
            type="button"
            onClick={() => toggle(cat)}
            className={cn(
              "rounded-full border px-3 py-1 text-xs font-medium transition-colors",
              active
                ? "border-primary/30 bg-primary/10 text-primary"
                : "border-border bg-card/50 text-muted-foreground hover:border-primary/20 hover:bg-primary/5 hover:text-foreground"
            )}
          >
            {cat}
          </button>
        )
      })}
    </div>
  )
}

export function CategoryTag({
  category,
  className,
}: {
  category: LegalCategory
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-md border border-border bg-muted/50 px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-muted-foreground",
        className
      )}
    >
      {category}
    </span>
  )
}
