"use client"

import { useEffect, useState } from "react"

// API Configuration
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000"

export const apiClient = {
  // Chat endpoints
  chat: {
    sendMessage: async (message: string, category: string, threadId?: string) => {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, category, threadId }),
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    getThreads: async () => {
      const response = await fetch(`${API_BASE}/api/chat/threads`)
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    getThread: async (id: string) => {
      const response = await fetch(`${API_BASE}/api/chat/threads/${id}`)
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },
  },

  // Documents endpoints
  documents: {
    upload: async (file: File, category: string) => {
      const formData = new FormData()
      formData.append("file", file)
      formData.append("category", category)

      const response = await fetch(`${API_BASE}/api/documents/upload`, {
        method: "POST",
        body: formData,
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    list: async () => {
      const response = await fetch(`${API_BASE}/api/documents`)
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    delete: async (id: string) => {
      const response = await fetch(`${API_BASE}/api/documents/${id}`, {
        method: "DELETE",
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },
  },

  // Settings endpoints
  settings: {
    get: async () => {
      const response = await fetch(`${API_BASE}/api/settings`)
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    update: async (settings: Record<string, any>) => {
      const response = await fetch(`${API_BASE}/api/settings`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },
  },

  // Sources endpoints
  sources: {
    list: async () => {
      const response = await fetch(`${API_BASE}/api/sources`)
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    save: async (sourceId: string) => {
      const response = await fetch(`${API_BASE}/api/sources/${sourceId}`, {
        method: "POST",
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },

    unsave: async (sourceId: string) => {
      const response = await fetch(`${API_BASE}/api/sources/${sourceId}`, {
        method: "DELETE",
      })
      if (!response.ok) throw new Error(`API error: ${response.status}`)
      return response.json()
    },
  },
}

// Hook for API calls with error handling
export function useApi<T>(
  apiFn: () => Promise<T>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const result = await apiFn()
        setData(result)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error")
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
  }, dependencies)

  return { data, isLoading, error }
}
