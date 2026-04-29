"use client"

import { useCallback, useState } from "react"
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

  const uploadFile = useCallback(
    async (file: File): Promise<{ success: boolean; error?: string }> => {
      if (!file) {
        return { success: false, error: "No file selected" }
      }

      const supportedTypes = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"]
      if (!supportedTypes.includes(file.type)) {
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
          uploadProgress: 0,
        }))

        // Placeholder for API call
        // const formData = new FormData()
        // formData.append("file", file)
        // const response = await fetch("/api/documents/upload", {
        //   method: "POST",
        //   body: formData,
        // })
        // const data = await response.json()

        // Simulate upload progress
        for (let i = 0; i <= 100; i += 10) {
          setState((prev) => ({
            ...prev,
            uploadProgress: i,
          }))
          await new Promise((resolve) => setTimeout(resolve, 100))
        }

        // Create mock uploaded doc
        const newDoc: UploadedDoc = {
          id: `doc-${Date.now()}`,
          name: file.name,
          size: `${(file.size / 1024 / 1024).toFixed(1)} MB`,
          pages: Math.ceil(file.size / 10000), // Mock page count
          uploadedAt: new Date().toLocaleString(),
          status: "processing",
          category: "Contract",
        }

        setState((prev) => ({
          ...prev,
          files: [...prev.files, newDoc],
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

  const removeFile = useCallback((fileId: string) => {
    setState((prev) => ({
      ...prev,
      files: prev.files.filter((f) => f.id !== fileId),
    }))
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
    clearError,
  }
}
