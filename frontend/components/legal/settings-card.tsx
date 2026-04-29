import type { LucideIcon } from "lucide-react"
import { cn } from "@/lib/utils"

export function SettingsCard({
  icon: Icon,
  title,
  description,
  children,
  className,
}: {
  icon?: LucideIcon
  title: string
  description?: string
  children: React.ReactNode
  className?: string
}) {
  return (
    <section
      className={cn(
        "rounded-2xl border border-border bg-card/60 p-6",
        className
      )}
    >
      <div className="flex items-start gap-3">
        {Icon && (
          <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20">
            <Icon className="size-4" />
          </div>
        )}
        <div className="min-w-0 flex-1">
          <h2 className="font-serif text-lg tracking-tight">{title}</h2>
          {description && (
            <p className="mt-0.5 text-sm leading-relaxed text-muted-foreground">
              {description}
            </p>
          )}
        </div>
      </div>
      <div className="mt-5 space-y-4">{children}</div>
    </section>
  )
}

export function SettingsRow({
  label,
  description,
  control,
  className,
}: {
  label: string
  description?: string
  control: React.ReactNode
  className?: string
}) {
  return (
    <div
      className={cn(
        "flex items-center justify-between gap-4 border-t border-border/60 py-3 first:border-t-0 first:pt-0",
        className
      )}
    >
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium">{label}</p>
        {description && (
          <p className="text-xs leading-relaxed text-muted-foreground">
            {description}
          </p>
        )}
      </div>
      <div className="shrink-0">{control}</div>
    </div>
  )
}
