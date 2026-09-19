"use client"

import * as React from "react"
import { Upload, FileText, Lock, Loader2, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"
import { useDocumentUpload } from "@/hooks/use-document-upload"

export function DocumentUploadCard({
  className,
  variant = "default",
  onUploadSuccess,
}: {
  className?: string
  variant?: "default" | "compact"
  onUploadSuccess?: () => void
}) {
  const [dragActive, setDragActive] = React.useState(false)
  const [uploadSuccess, setUploadSuccess] = React.useState(false)
  const inputRef = React.useRef<HTMLInputElement>(null)
  const { uploadFile, isUploading, uploadProgress, error } = useDocumentUpload()

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") setDragActive(true)
    else if (e.type === "dragleave") setDragActive(false)
  }

  const processFile = async (file: File) => {
    setUploadSuccess(false)
    const result = await uploadFile(file)
    if (result.success) {
      setUploadSuccess(true)
      setTimeout(() => setUploadSuccess(false), 3000)
      if (onUploadSuccess) {
        onUploadSuccess()
      }
    }
    if (inputRef.current) {
      inputRef.current.value = ""
    }
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      await processFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      await processFile(e.target.files[0])
    }
  }

  if (variant === "compact") {
    return (
      <div className={className}>
        <label
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          className={cn(
            "flex cursor-pointer flex-col items-center gap-1.5 rounded-lg border border-dashed border-border bg-card/30 px-3 py-4 text-center transition-colors hover:border-primary/40 hover:bg-primary/5",
            dragActive && "border-primary/50 bg-primary/10",
            isUploading && "pointer-events-none opacity-60"
          )}
        >
          {isUploading ? (
            <Loader2 className="size-4 animate-spin text-primary" />
          ) : uploadSuccess ? (
            <CheckCircle2 className="size-4 text-emerald-500" />
          ) : (
            <Upload className="size-4 text-muted-foreground" />
          )}
          <span className="text-xs font-medium">
            {isUploading
              ? `Uploading (${uploadProgress}%)...`
              : uploadSuccess
              ? "Indexed in FAISS!"
              : "Upload document"}
          </span>
          <span className="text-[10px] text-muted-foreground">
            PDF, DOCX · Max 25 MB
          </span>
          <input
            ref={inputRef}
            type="file"
            className="sr-only"
            accept=".pdf,.docx,.doc,.txt"
            onChange={handleFileChange}
            disabled={isUploading}
          />
        </label>
        {error && (
          <p className="mt-1 text-center text-[10px] text-destructive">{error}</p>
        )}
      </div>
    )
  }

  return (
    <div className={className}>
      <label
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={cn(
          "group relative flex cursor-pointer flex-col items-center gap-3 rounded-2xl border border-dashed border-border bg-card/40 px-6 py-10 text-center transition-all hover:border-primary/40 hover:bg-primary/5",
          dragActive && "scale-[1.01] border-primary/50 bg-primary/10",
          isUploading && "pointer-events-none opacity-60"
        )}
      >
        <div className="relative">
          <div className="flex size-14 items-center justify-center rounded-xl bg-primary/10 ring-1 ring-primary/20 transition-transform group-hover:scale-105">
            {isUploading ? (
              <Loader2 className="size-6 animate-spin text-primary" />
            ) : uploadSuccess ? (
              <CheckCircle2 className="size-6 text-emerald-500" />
            ) : (
              <FileText className="size-6 text-primary" />
            )}
          </div>
          <div className="absolute -bottom-1 -right-1 flex size-6 items-center justify-center rounded-full bg-accent text-accent-foreground ring-2 ring-card">
            <Upload className="size-3" />
          </div>
        </div>

        <div className="space-y-1">
          <p className="font-serif text-base tracking-tight">
            {isUploading
              ? `Processing & indexing document (${uploadProgress}%)...`
              : uploadSuccess
              ? "Document indexed successfully into FAISS!"
              : "Drop your legal documents here"}
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
          Encrypted in transit · Processed locally with InLegalBERT
        </div>

        <input
          ref={inputRef}
          type="file"
          className="sr-only"
          accept=".pdf,.docx,.doc,.txt"
          onChange={handleFileChange}
          disabled={isUploading}
        />
      </label>
      {error && (
        <div className="mt-2 rounded-lg border border-destructive/30 bg-destructive/5 p-2 text-center text-xs text-destructive">
          {error}
        </div>
      )}
    </div>
  )
}
