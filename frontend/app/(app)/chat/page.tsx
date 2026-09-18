"use client"

import { Sparkles, ChevronDown, Globe2, Filter, MessageSquare } from "lucide-react"
import { useEffect, Suspense } from "react"
import { useSearchParams } from "next/navigation"
import { ChatMessage } from "@/components/legal/chat-message"
import { ChatInput } from "@/components/legal/chat-input"
import { RightPanel } from "@/components/legal/right-panel"
import { DisclaimerBanner } from "@/components/legal/disclaimer-banner"
import { MessageSkeleton } from "@/components/legal/loading-skeleton"
import { CategoryTag } from "@/components/legal/category-chips"
import { Button } from "@/components/ui/button"
import { useChat } from "@/hooks/use-chat"

function ChatContent() {
  const searchParams = useSearchParams()
  const threadIdParam = searchParams.get("thread")
  const chat = useChat([])

  useEffect(() => {
    if (threadIdParam) {
      chat.loadThread(threadIdParam)
    } else {
      chat.clearMessages()
    }
  }, [threadIdParam])

  useEffect(() => {
    chat.scrollToBottom()
  }, [chat.messages.length, chat.scrollToBottom])

  const handleSendMessage = async (content: string) => {
    const result = await chat.sendMessage(content, "General", threadIdParam)
    if (!result.success) {
      console.error("Failed to send message:", result.error)
    }
  }

  const latestConfidence = chat.messages.length > 0
    ? chat.messages.filter((m) => m.role === "assistant").slice(-1)[0]?.confidence || "medium"
    : "medium"

  return (
    <div className="flex min-w-0 flex-1">
      <main className="flex min-w-0 flex-1 flex-col xl:mr-[360px]">
        <ChatHeader threadId={threadIdParam || chat.currentThreadId} />
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-3xl px-4 py-6 lg:px-8 lg:py-8">
            <DisclaimerBanner className="mb-6" />

            {chat.messages.length === 0 && !chat.isLoading ? (
              <div className="my-12 text-center">
                <div className="mx-auto mb-4 flex size-12 items-center justify-center rounded-2xl bg-primary/10 text-primary">
                  <Sparkles className="size-6" />
                </div>
                <h2 className="font-serif text-2xl font-medium tracking-tight">
                  How can LegalEagle assist you today?
                </h2>
                <p className="mx-auto mt-2 max-w-md text-sm text-muted-foreground">
                  Ask any question about Indian statutes, IPC/CrPC, constitutional rights, or corporate law.
                </p>

                <div className="mt-8 grid grid-cols-1 gap-2.5 sm:grid-cols-2 text-left">
                  {[
                    "What is Section 420 IPC and its essential ingredients?",
                    "What is the punishment for murder under Section 302 IPC?",
                    "Explain tenant rights under the Rent Control Act",
                    "What constitutes criminal breach of trust under Section 405 IPC?",
                  ].map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => handleSendMessage(prompt)}
                      className="rounded-xl border border-border bg-card/40 p-3.5 text-xs text-muted-foreground transition hover:border-primary/40 hover:bg-card hover:text-foreground"
                    >
                      <div className="flex items-center gap-2 font-medium text-foreground">
                        <MessageSquare className="size-3.5 text-primary" />
                        <span>Legal Query</span>
                      </div>
                      <p className="mt-1.5 leading-relaxed">{prompt}</p>
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-7">
                {chat.messages.map((m) => (
                  <ChatMessage key={m.id} message={m} />
                ))}
                {chat.isLoading && <MessageSkeleton />}
              </div>
            )}

            <div ref={chat.messagesEndRef} />
          </div>
        </div>

        <div className="sticky bottom-0 border-t border-border bg-background/90 backdrop-blur">
          <div className="mx-auto max-w-3xl px-4 py-4 lg:px-8">
            <ChatInput
              onClear={chat.clearMessages}
              onSubmit={handleSendMessage}
              disabled={chat.isLoading}
            />
            {chat.error && (
              <div className="mt-2 rounded-lg border border-destructive/30 bg-destructive/5 p-2 text-xs text-destructive">
                {chat.error}
              </div>
            )}
            <p className="mt-2 text-center font-mono text-[10px] text-muted-foreground">
              LegalEagle can make mistakes. Always verify citations before use.
            </p>
          </div>
        </div>
      </main>

      <RightPanel
        sources={chat.latestSources}
        confidence={latestConfidence}
      />
    </div>
  )
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-sm text-muted-foreground">Loading consultation...</div>}>
      <ChatContent />
    </Suspense>
  )
}

function ChatHeader({ threadId }: { threadId: string | null }) {
  return (
    <header className="border-b border-border bg-background/90 backdrop-blur">
      <div className="mx-auto max-w-3xl px-4 py-4 lg:px-8">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <CategoryTag category="Constitution" />
              {threadId && (
                <span className="font-mono text-[10px] text-muted-foreground">
                  Thread #{threadId}
                </span>
              )}
            </div>
            <h1 className="mt-1.5 truncate font-serif text-xl tracking-tight md:text-2xl">
              Legal Research Consultation
            </h1>
            <p className="text-xs text-muted-foreground">
              AI assistant grounded in verified FAISS legal knowledge base.
            </p>
          </div>
          <div className="flex shrink-0 items-center gap-1.5">
            <Button
              variant="outline"
              size="sm"
              className="hidden h-8 gap-1.5 rounded-full border-border bg-card/50 text-xs sm:inline-flex"
            >
              <Globe2 className="size-3.5" />
              India
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
