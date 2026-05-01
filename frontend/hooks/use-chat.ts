"use client"

import { useCallback, useRef, useState } from "react"
import type { Message, Source } from "@/lib/legal-data"

export interface ChatState {
  messages: Message[]
  isLoading: boolean
  error: string | null
}

export function useChat(initialMessages: Message[] = []) {
  const [state, setState] = useState<ChatState>({
    messages: initialMessages,
    isLoading: false,
    error: null,
  })

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [])

  const addMessage = useCallback((message: Message) => {
    setState((prev) => ({
      ...prev,
      messages: [...prev.messages, message],
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

  const sendMessage = useCallback(
    async (
      content: string,
      category?: string
    ): Promise<{ success: boolean; error?: string }> => {
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

        // Build chat history from existing messages for stateless backend
        const chatHistory = state.messages
          .concat(userMessage)
          .map((m) => ({ role: m.role, content: m.content }))

        // Call the FastAPI backend
        const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
        const response = await fetch(`${API_URL}/chat`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            message: content,
            category: category || null,
            chat_history: chatHistory,
          }),
        })

        if (!response.ok) {
          const errorData = await response.json().catch(() => null)
          throw new Error(
            errorData?.detail || `Backend error: ${response.status} ${response.statusText}`
          )
        }

        const data = await response.json()

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
          sources: (data.sources || []).map((src: any) => ({
            id: src.id,
            title: src.title || "Retrieved Document",
            citation: src.citation || "",
            jurisdiction: src.jurisdiction || "",
            year: src.year || 0,
            excerpt: src.excerpt || "",
            url: src.url,
            type: src.type || "retrieved_chunk",
          })),
        }

        addMessage(assistantMessage)
        return { success: true }
      } catch (error) {
        const errorMessage =
          error instanceof Error ? error.message : "Failed to send message"
        setError(errorMessage)
        return { success: false, error: errorMessage }
      } finally {
        setLoading(false)
      }
    },
    [addMessage, setLoading, setError]
  )

  const clearMessages = useCallback(() => {
    setState((prev) => ({
      ...prev,
      messages: [],
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
    setLoading,
    setError,
    clearError,
    clearMessages,
    messagesEndRef,
    scrollToBottom,
  }
}
