"use client"

import { Sparkles, ChevronDown, Globe2, Filter } from "lucide-react"
import { useEffect } from "react"
import { ChatMessage } from "@/components/legal/chat-message"
import { ChatInput } from "@/components/legal/chat-input"
import { RightPanel } from "@/components/legal/right-panel"
import { DisclaimerBanner } from "@/components/legal/disclaimer-banner"
import { MessageSkeleton } from "@/components/legal/loading-skeleton"
import { CategoryTag } from "@/components/legal/category-chips"
import { sampleMessages } from "@/lib/legal-data"
import { Button } from "@/components/ui/button"
import { useChat } from "@/hooks/use-chat"

export default function ChatPage() {
  const chat = useChat(sampleMessages)

  useEffect(() => {
    chat.scrollToBottom()
  }, [chat.messages.length, chat.scrollToBottom])

  const handleSendMessage = async (content: string) => {
    const result = await chat.sendMessage(content, "Property")
    if (!result.success) {
      console.error("Failed to send message:", result.error)
    }
  }

  return (
    <div className="flex min-w-0 flex-1">
      <main className="flex min-w-0 flex-1 flex-col xl:mr-[360px]">
        <ChatHeader />
        <div className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-3xl px-4 py-6 lg:px-8 lg:py-8">
            <DisclaimerBanner className="mb-6" />
            <div className="space-y-7">
              {chat.messages.map((m) => (
                <ChatMessage key={m.id} message={m} />
              ))}
              {chat.isLoading && <MessageSkeleton />}
            </div>
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
      <RightPanel />
    </div>
  )
}

function ChatHeader() {
  return (
    <header className="border-b border-border bg-background/90 backdrop-blur">
      <div className="mx-auto max-w-3xl px-4 py-4 lg:px-8">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <CategoryTag category="Property" />
              <span className="font-mono text-[10px] text-muted-foreground">
                Thread #t-1 · Updated 2 min ago
              </span>
            </div>
            <h1 className="mt-1.5 truncate font-serif text-xl tracking-tight md:text-2xl">
              Tenant rights under Rent Control Act
            </h1>
            <p className="text-xs text-muted-foreground">
              Researching jurisdiction-aware eviction procedure for residential
              tenancies.
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
              <ChevronDown className="size-3" />
            </Button>
            <Button
              variant="outline"
              size="sm"
              className="h-8 gap-1.5 rounded-full border-border bg-card/50 text-xs"
            >
              <Filter className="size-3.5" />
              <span className="hidden sm:inline">Filters</span>
            </Button>
            <Button
              size="sm"
              className="h-8 gap-1.5 rounded-full bg-primary/10 text-primary ring-1 ring-primary/20 hover:bg-primary/15"
            >
              <Sparkles className="size-3.5" />
              <span className="hidden sm:inline">Suggest follow-ups</span>
              <span className="sm:hidden">AI</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}
