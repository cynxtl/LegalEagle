import { Skeleton } from "@/components/ui/skeleton"
import { cn } from "@/lib/utils"
import { Sparkles } from "lucide-react"

export function MessageSkeleton({ className }: { className?: string }) {
  return (
    <div className={cn("flex gap-3", className)}>
      <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/10">
        <Sparkles className="size-3.5 animate-pulse text-primary" />
      </div>
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-medium">LegalEagle</span>
          <span className="inline-flex items-center gap-1 text-[10px] text-muted-foreground">
            <span className="size-1 animate-pulse rounded-full bg-primary" />
            Searching case law
          </span>
        </div>
        <Skeleton className="h-3 w-[80%] rounded-md" />
        <Skeleton className="h-3 w-[92%] rounded-md" />
        <Skeleton className="h-3 w-[65%] rounded-md" />
        <div className="flex gap-2 pt-1">
          <Skeleton className="h-12 w-32 rounded-lg" />
          <Skeleton className="h-12 w-32 rounded-lg" />
        </div>
      </div>
    </div>
  )
}

export function SourceSkeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card/40 p-4",
        className
      )}
    >
      <div className="flex items-center gap-2">
        <Skeleton className="size-7 rounded-md" />
        <Skeleton className="h-2.5 w-16 rounded" />
      </div>
      <Skeleton className="mt-3 h-4 w-[80%] rounded" />
      <Skeleton className="mt-1.5 h-3 w-[60%] rounded" />
      <Skeleton className="mt-3 h-12 w-full rounded" />
    </div>
  )
}

export function ThreadSkeleton() {
  return (
    <div className="space-y-1.5">
      {[0, 1, 2].map((i) => (
        <div key={i} className="rounded-md p-2">
          <Skeleton className="h-3 w-[85%] rounded" />
          <Skeleton className="mt-1.5 h-2.5 w-[60%] rounded" />
        </div>
      ))}
    </div>
  )
}
