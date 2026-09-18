"use client"

import { useCallback, useRef, useState } from "react"
import type { Message, Source } from "@/lib/legal-data"

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
  currentThreadId: string | null
  latestSources: Source[]
}

export function useChat(initialMessages: Message[] = []) {
  const [state, setState] = useState<ChatState>({
    messages: initialMessages,
    isLoading: false,
    error: null,
    currentThreadId: null,
    latestSources: [],
  })

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [])

  const addMessage = useCallback((message: Message) => {
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, message],
      latestSources: message.sources && message.sources.length > 0 ? message.sources : prev.latestSources,
    }))
    setTimeout(scrollToBottom, 100)
  }, [scrollToBottom])

  const setLoading = useCallback((loading: boolean) => {
    setState((prev) => ({
      ...prev,
      isLoading: loading,
    }))
  }, [])

  const setError = useCallback((error: string | null) => {
    setState((prev) => ({
      ...prev,
      error,
    }))
  }, [])

  const setThreadId = useCallback((threadId: string | null) => {
    setState((prev) => ({
      ...prev,
      currentThreadId: threadId,
    }))
  }, [])

  const loadThread = useCallback(async (threadId: string) => {
    try {
      setLoading(true)
      setError(null)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/threads/${threadId}`)
      if (!res.ok) {
        throw new Error(`Failed to load thread: ${res.statusText}`)
      }
      const data = await res.json()
      const mappedMessages: Message[] = (data.messages || []).map((m: any) => ({
        id: m.id,
        role: m.role,
        content: m.content,
        timestamp: new Date(m.created_at).toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
        }),
        confidence: m.confidence || "medium",
        category: m.category || "General",
        sources: (m.sources || []).map((s: any) => ({
          id: s.id,
          title: s.title || "Retrieved Document",
          citation: s.citation || "",
          jurisdiction: s.jurisdiction || "",
          year: s.year || 0,
          excerpt: s.excerpt || "",
          url: s.url,
          type: s.type || "retrieved_chunk",
        })),
      }))

      const allSources = mappedMessages
        .flatMap((m) => m.sources || [])
        .filter((s) => Boolean(s.id))

      setState((prev) => ({
        ...prev,
        messages: mappedMessages,
        currentThreadId: threadId,
        latestSources: allSources,
      }))
      setTimeout(scrollToBottom, 100)
    } catch (err: any) {
      setError(err.message || "Failed to load thread")
    } finally {
      setLoading(false)
    }
  }, [setLoading, setError, scrollToBottom])

  const sendMessage = useCallback(
    async (
      content: string,
      category?: string,
      threadIdOverride?: string | null
    ): Promise<{ success: boolean; threadId?: string; error?: string }> => {
      if (!content.trim()) {
        return { success: false, error: "Message cannot be empty" }
      }

      try {
        setError(null)
        setLoading(true)

        const userMessage: Message = {
          id: `msg-${Date.now()}`,
          role: "user",
          content,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          }),
          category: category as any,
        }

        addMessage(userMessage)

        const activeThreadId = threadIdOverride || state.currentThreadId

        // Call the FastAPI backend
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
        const response = await fetch(`${API_URL}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: content,
            category: category || null,
            thread_id: activeThreadId,
          }),
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => null)
          throw new Error(
            errorData?.detail || `Backend error: ${response.status} ${response.statusText}`
          )
        }

        const data = await response.json()
        const retThreadId = data.thread_id || activeThreadId

        const mappedSources: Source[] = (data.sources || []).map((src: any) => ({
          id: src.id,
          title: src.title || "Retrieved Document",
          citation: src.citation || "",
          jurisdiction: src.jurisdiction || "",
          year: src.year || 0,
          excerpt: src.excerpt || "",
          url: src.url,
          type: src.type || "retrieved_chunk",
        }))

        // Map backend response to frontend Message type
        const assistantMessage: Message = {
          id: `msg-${Date.now() + 1}`,
          role: "assistant",
          content: data.answer,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          }),
          confidence: data.confidence || "medium",
          category: category as any,
          sources: mappedSources,
        }

        setState((prev) => ({
          ...prev,
          currentThreadId: retThreadId,
          latestSources: mappedSources,
        }))

        addMessage(assistantMessage)
        return { success: true, threadId: retThreadId }
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Failed to send message"
        setError(errorMessage)
        return { success: false, error: errorMessage }
      } finally {
        setLoading(false)
      }
    },
    [addMessage, setLoading, setError, state.currentThreadId]
  )

  const clearMessages = useCallback(() => {
    setState((prev) => ({
      ...prev,
      messages: [],
      currentThreadId: null,
      latestSources: [],
      error: null,
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
    addMessage,
    sendMessage,
    loadThread,
    setThreadId,
    setLoading,
    setError,
    clearError,
    clearMessages,
    messagesEndRef,
    scrollToBottom,
  }
}
