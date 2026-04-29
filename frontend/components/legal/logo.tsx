import { cn } from "@/lib/utils"

export function Logo({
  className,
  showWordmark = true,
}: {
  className?: string
  showWordmark?: boolean
}) {
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      <div className="relative flex size-8 items-center justify-center rounded-lg bg-primary/10 ring-1 ring-primary/20">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          aria-hidden="true"
          className="size-5 text-primary"
        >
          <path
            d="M12 2L4 6v6c0 5 3.5 9.5 8 10 4.5-.5 8-5 8-10V6l-8-4z"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinejoin="round"
          />
          <path
            d="M9 12l2 2 4-4"
            stroke="currentColor"
            strokeWidth="1.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
        <span className="absolute -right-0.5 -top-0.5 size-1.5 rounded-full bg-accent ring-2 ring-sidebar" />
      </div>
      {showWordmark && (
        <div className="flex flex-col leading-none">
          <span className="font-serif text-lg tracking-tight">LegalEagle</span>
          <span className="font-mono text-[9px] uppercase tracking-[0.18em] text-muted-foreground">
            v2 · counsel ai
          </span>
        </div>
      )}
    </div>
  )
}
