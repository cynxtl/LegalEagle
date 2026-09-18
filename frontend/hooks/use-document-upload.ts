"use client"

import { useCallback, useEffect, useState } from "react"
import type { UploadedDoc } from "@/lib/legal-data"

export interface UploadState {
  files: UploadedDoc[]
  isUploading: boolean
  uploadProgress: number
  error: string | null
}

export function useDocumentUpload(initialFiles: UploadedDoc[] = []) {
  const [state, setState] = useState<UploadState>({
    files: initialFiles,
    isUploading: false,
    uploadProgress: 0,
    error: null,
  })

  const fetchDocuments = useCallback(async () => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/documents`)
      if (res.ok) {
        const data = await res.json()
        const mapped: UploadedDoc[] = data.map((d: any) => ({
          id: d.id,
          name: d.name,
          size: d.size,
          pages: d.pages,
          uploadedAt: d.uploaded_at,
          status: d.status,
          category: d.category || "General",
        }))
        setState((prev) => ({ ...prev, files: mapped }))
      }
    } catch (e) {
      console.error("Failed to fetch documents:", e)
    }
  }, [])

  useEffect(() => {
    fetchDocuments()
  }, [fetchDocuments])

  const uploadFile = useCallback(
    async (file: File): Promise<{ success: boolean; error?: string }> => {
      if (!file) {
        return { success: false, error: "No file selected" }
      }

      const supportedExts = [".pdf", ".docx", ".doc", ".txt"]
      const fileNameLower = file.name.toLowerCase()
      const isExtSupported = supportedExts.some((ext) => fileNameLower.endsWith(ext))

      if (!isExtSupported) {
        return {
          success: false,
          error: "File type not supported. Please upload PDF, DOCX, or TXT.",
        }
      }

      const maxSize = 25 * 1024 * 1024 // 25 MB
      if (file.size > maxSize) {
        return {
          success: false,
          error: "File size exceeds 25 MB limit.",
        }
      }

      try {
        setState((prev) => ({
          ...prev,
          isUploading: true,
          error: null,
          uploadProgress: 20,
        }))

        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
        const formData = new FormData()
        formData.append("file", file)

        setState((prev) => ({ ...prev, uploadProgress: 50 }))

        const response = await fetch(`${API_URL}/upload`, {
          method: "POST",
          body: formData,
        })

        setState((prev) => ({ ...prev, uploadProgress: 80 }))

        if (!response.ok) {
          const errorData = await response.json().catch(() => null)
          throw new Error(
            errorData?.detail || `Upload failed: ${response.status} ${response.statusText}`
          )
        }

        const data = await response.json()

        const newDoc: UploadedDoc = {
          id: data.id || `doc-${Date.now()}`,
          name: data.name || file.name,
          size: data.size || `${(file.size / 1024 / 1024).toFixed(1)} MB`,
          pages: data.pages || 1,
          uploadedAt: data.uploaded_at || new Date().toLocaleString(),
          status: data.status || "indexed",
          category: data.category || "General",
        }

        setState((prev) => ({
          ...prev,
          files: [newDoc, ...prev.files.filter((f) => f.id !== newDoc.id)],
          uploadProgress: 0,
          isUploading: false,
        }))

        return { success: true }
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Upload failed"
        setState((prev) => ({
          ...prev,
          error: errorMessage,
          isUploading: false,
          uploadProgress: 0,
        }))
        return { success: false, error: errorMessage }
      }
    },
    []
  )

  const removeFile = useCallback(async (fileId: string) => {
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      await fetch(`${API_URL}/api/v1/documents/${fileId}`, {
        method: "DELETE",
      })
      setState((prev) => ({
        ...prev,
        files: prev.files.filter((f) => f.id !== fileId),
      }))
    } catch (e) {
      console.error("Failed to delete document:", e)
    }
  }, [])

  const clearError = useCallback(() => {
    setState((prev) => ({
      ...prev,
      error: null,
    }))
  }, [])

  return {
    ...state,
    uploadFile,
    removeFile,
    fetchDocuments,
    clearError,
  }
}
