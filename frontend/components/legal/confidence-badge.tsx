import type { Confidence } from "@/lib/legal-data"
import { cn } from "@/lib/utils"

const config = {
  high: {
    label: "High confidence",
    dots: 3,
    tone: "text-primary",
    bg: "bg-primary/10",
    ring: "ring-primary/20",
    dotColor: "bg-primary",
  },
  medium: {
    label: "Medium confidence",
    dots: 2,
    tone: "text-accent",
    bg: "bg-accent/10",
    ring: "ring-accent/20",
    dotColor: "bg-accent",
  },
  low: {
    label: "Low confidence",
    dots: 1,
    tone: "text-destructive",
    bg: "bg-destructive/10",
    ring: "ring-destructive/20",
    dotColor: "bg-destructive",
  },
} as const

export function ConfidenceBadge({
  level,
  className,
}: {
  level: Confidence
  className?: string
}) {
  const c = config[level]
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-[11px] font-medium ring-1",
        c.bg,
        c.ring,
        c.tone,
        className
      )}
    >
      <span className="flex items-center gap-0.5">
        {[0, 1, 2].map((i) => (
          <span
            key={i}
            className={cn(
              "size-1.5 rounded-full",
              i < c.dots ? c.dotColor : "bg-current opacity-20"
            )}
          />
        ))}
      </span>
      {c.label}
    </span>
  )
}
