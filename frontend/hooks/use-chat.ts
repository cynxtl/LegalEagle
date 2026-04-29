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

        // Simulate API delay
        await new Promise((resolve) => setTimeout(resolve, 1500))

        // Mock assistant response
        const assistantMessage: Message = {
          id: `msg-${Date.now() + 1}`,
          role: "assistant",
          content: `This is a response to: "${content.substring(0, 50)}..."\n\nConnect your backend API when ready.`,
          timestamp: new Date().toLocaleTimeString("en-US", {
            hour: "2-digit",
            minute: "2-digit",
          }),
          confidence: "medium",
          category: category as any,
          sources: [],
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
