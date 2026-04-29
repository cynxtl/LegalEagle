import { Scale } from "lucide-react"
import { cn } from "@/lib/utils"

export function DisclaimerBanner({
  className,
  variant = "default",
}: {
  className?: string
  variant?: "default" | "compact"
}) {
  if (variant === "compact") {
    return (
      <div
        className={cn(
          "flex items-center gap-2 rounded-md border border-accent/20 bg-accent/5 px-3 py-1.5 text-xs text-muted-foreground",
          className
        )}
      >
        <Scale className="size-3.5 shrink-0 text-accent" />
        <span>
          Informational only · Not legal advice · Always verify with a qualified
          lawyer
        </span>
      </div>
    )
  }

  return (
    <div
      role="note"
      className={cn(
        "flex items-start gap-3 rounded-xl border border-accent/20 bg-accent/[0.06] px-4 py-3",
        className
      )}
    >
      <div className="flex size-7 shrink-0 items-center justify-center rounded-md bg-accent/15">
        <Scale className="size-4 text-accent" />
      </div>
      <div className="space-y-0.5">
        <p className="text-sm font-medium">For informational purposes only</p>
        <p className="text-xs leading-relaxed text-muted-foreground">
          LegalEagle provides AI-assisted research with cited sources. It is not
          a substitute for legal advice from a licensed attorney in your
          jurisdiction.
        </p>
      </div>
    </div>
  )
}
