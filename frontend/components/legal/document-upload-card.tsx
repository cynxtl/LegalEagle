"use client"

import * as React from "react"
import { Upload, FileText, Lock } from "lucide-react"
import { cn } from "@/lib/utils"

export function DocumentUploadCard({
  className,
  variant = "default",
}: {
  className?: string
  variant?: "default" | "compact"
}) {
  const [dragActive, setDragActive] = React.useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true)
    else if (e.type === "dragleave") setDragActive(false)
  }

  if (variant === "compact") {
    return (
      <label
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={(e) => {
          handleDrag(e)
          setDragActive(false)
        }}
        className={cn(
          "flex cursor-pointer flex-col items-center gap-1.5 rounded-lg border border-dashed border-border bg-card/30 px-3 py-4 text-center transition-colors hover:border-primary/40 hover:bg-primary/5",
          dragActive && "border-primary/50 bg-primary/10",
          className
        )}
      >
        <Upload className="size-4 text-muted-foreground" />
        <span className="text-xs font-medium">Upload document</span>
        <span className="text-[10px] text-muted-foreground">
          PDF, DOCX · Max 25 MB
        </span>
        <input type="file" className="sr-only" accept=".pdf,.docx,.doc,.txt" />
      </label>
    )
  }

  return (
    <label
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={(e) => {
        handleDrag(e)
        setDragActive(false)
      }}
      className={cn(
        "group relative flex cursor-pointer flex-col items-center gap-3 rounded-2xl border border-dashed border-border bg-card/40 px-6 py-10 text-center transition-all hover:border-primary/40 hover:bg-primary/5",
        dragActive && "scale-[1.01] border-primary/50 bg-primary/10",
        className
      )}
    >
      <div className="relative">
        <div className="flex size-14 items-center justify-center rounded-xl bg-primary/10 ring-1 ring-primary/20 transition-transform group-hover:scale-105">
          <FileText className="size-6 text-primary" />
        </div>
        <div className="absolute -bottom-1 -right-1 flex size-6 items-center justify-center rounded-full bg-accent text-accent-foreground ring-2 ring-card">
          <Upload className="size-3" />
        </div>
      </div>

      <div className="space-y-1">
        <p className="font-serif text-base tracking-tight">
          Drop your legal documents here
        </p>
        <p className="text-xs text-muted-foreground">
          or{" "}
          <span className="font-medium text-primary underline-offset-2 group-hover:underline">
            browse files
          </span>{" "}
          · PDF, DOCX, TXT up to 25 MB
        </p>
      </div>

      <div className="mt-1 inline-flex items-center gap-1.5 rounded-full border border-border bg-background/50 px-2.5 py-1 text-[10px] text-muted-foreground">
        <Lock className="size-3 text-primary" />
        Encrypted in transit · Never used for training
      </div>

      <input type="file" className="sr-only" accept=".pdf,.docx,.doc,.txt" />
    </label>
  )
}
