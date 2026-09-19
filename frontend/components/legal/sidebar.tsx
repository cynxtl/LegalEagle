"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import {
  Plus,
  MessageSquare,
  FileText,
  BookMarked,
  Settings,
  Sparkles,
  Upload,
  Search,
  Trash2,
  Pencil,
} from "lucide-react"
import { Logo } from "./logo"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog"
import { DocumentUploadCard } from "./document-upload-card"
import { ThemeToggle } from "./theme-toggle"
import { cn } from "@/lib/utils"

export interface ThreadItem {
  id: string
  title: string
  category: string
  updated_at: string
  message_count: number
  preview?: string
}

const quickLinks = [
  { href: "/chat", label: "Ask a Question", icon: Sparkles },
  { href: "/documents", label: "Upload a File", icon: Upload },
  { href: "/sources", label: "Saved Sources", icon: BookMarked },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function LegalSidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const [threads, setThreads] = useState<ThreadItem[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [editingThread, setEditingThread] = useState<{ id: string; title: string } | null>(null)
  const [newTitle, setNewTitle] = useState("")
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [searchFilter, setSearchFilter] = useState("")

  const fetchThreads = async () => {
    try {
      setIsLoading(true)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/threads`)
      if (res.ok) {
        const data = await res.json()
        setThreads(data)
      }
    } catch (e) {
      console.error("Failed to fetch threads:", e)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchThreads()
    const interval = setInterval(fetchThreads, 10000)
    return () => clearInterval(interval)
  }, [])

  const handleDeleteThread = async (e: React.MouseEvent, threadId: string) => {
    e.preventDefault()
    e.stopPropagation()
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/threads/${threadId}`, {
        method: "DELETE",
      })
      if (res.ok) {
        setThreads((prev) => prev.filter((t) => t.id !== threadId))
        router.push("/chat")
      }
    } catch (err) {
      console.error("Failed to delete thread:", err)
    }
  }

  const handleStartRename = (e: React.MouseEvent, thread: ThreadItem) => {
    e.preventDefault()
    e.stopPropagation()
    setEditingThread({ id: thread.id, title: thread.title })
    setNewTitle(thread.title)
  }

  const handleSaveRename = async () => {
    if (!editingThread || !newTitle.trim()) return
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/threads/${editingThread.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: newTitle.trim() }),
      })
      if (res.ok) {
        setThreads((prev) =>
          prev.map((t) => (t.id === editingThread.id ? { ...t, title: newTitle.trim() } : t))
        )
      }
    } catch (err) {
      console.error("Failed to rename thread:", err)
    } finally {
      setEditingThread(null)
    }
  }

  const filteredSearchThreads = threads.filter((t) =>
    t.title.toLowerCase().includes(searchFilter.toLowerCase())
  )

  return (
    <aside className="fixed left-0 top-0 hidden h-svh w-72 flex-col border-r border-sidebar-border bg-sidebar lg:flex">
      <div className="flex items-center justify-between border-b border-sidebar-border px-4 py-4">
        <Link href="/" aria-label="LegalEagle home">
          <Logo />
        </Link>
        <button
          aria-label="Search consultations"
          title="Search consultations"
          onClick={() => {
            setSearchFilter("")
            setIsSearchOpen(true)
          }}
          className="flex size-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
        >
          <Search className="size-4" />
        </button>
      </div>

      <div className="border-b border-sidebar-border px-3 py-2">
        <Button
          onClick={() => {
            router.push("/chat")
          }}
          className="w-full justify-start gap-2 rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20 hover:bg-primary/15"
        >
          <Plus className="size-4" />
          New consultation
        </Button>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <div className="mb-2 flex items-center justify-between px-2">
          <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            Recent threads
          </span>
          <span className="font-mono text-[10px] text-muted-foreground">
            {threads.length}
          </span>
        </div>

        {threads.length === 0 && !isLoading ? (
          <div className="px-2 py-4 text-center">
            <p className="text-xs text-muted-foreground">No recent consultations</p>
          </div>
        ) : (
          <ul className="space-y-0.5">
            {threads.map((thread) => (
              <li key={thread.id}>
                <Link
                  href={`/chat?thread=${thread.id}`}
                  className="group flex items-start justify-between gap-2 rounded-md px-2 py-2 text-sm transition-colors hover:bg-sidebar-accent"
                >
                  <div className="flex items-start gap-2 min-w-0 flex-1">
                    <MessageSquare className="mt-0.5 size-3.5 shrink-0 text-muted-foreground" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-xs font-medium leading-tight">
                        {thread.title}
                      </p>
                      <div className="mt-0.5 flex items-center gap-1.5">
                        <span className="truncate text-[10px] text-muted-foreground">
                          {thread.category || "General"}
                        </span>
                        <span className="size-0.5 rounded-full bg-muted-foreground/40" />
                        <span className="font-mono text-[10px] text-muted-foreground">
                          {thread.message_count} msgs
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={(e) => handleStartRename(e, thread)}
                      aria-label="Rename thread"
                      className="p-1 text-muted-foreground hover:text-foreground"
                    >
                      <Pencil className="size-3" />
                    </button>
                    <button
                      onClick={(e) => handleDeleteThread(e, thread.id)}
                      aria-label="Delete thread"
                      className="p-1 text-muted-foreground hover:text-destructive"
                    >
                      <Trash2 className="size-3" />
                    </button>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        )}

        <div className="mt-6 px-2">
          <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            Quick actions
          </span>
        </div>
        <ul className="mt-2 space-y-0.5">
          {quickLinks.map((link) => {
            const active = pathname === link.href
            const Icon = link.icon
            return (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={cn(
                    "flex items-center gap-2.5 rounded-md px-2 py-2 text-sm transition-colors",
                    active
                      ? "bg-sidebar-accent text-foreground"
                      : "text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
                  )}
                >
                  <Icon className="size-3.5" />
                  {link.label}
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="border-t border-sidebar-border p-3">
        <DocumentUploadCard variant="compact" onUploadSuccess={fetchThreads} />
        <div className="mt-3 flex items-center gap-2 rounded-lg bg-sidebar-accent/60 p-2.5">
          <div className="flex size-7 items-center justify-center rounded-full bg-primary/15 text-primary">
            <FileText className="size-3.5" />
          </div>
          <div className="min-w-0 flex-1">
            <p className="truncate text-xs font-medium">Pro plan</p>
            <p className="truncate text-[10px] text-muted-foreground">
              Unlimited research · 50 docs/mo
            </p>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between gap-2 border-t border-sidebar-border/60 pt-3">
          <span className="text-xs text-muted-foreground">Theme</span>
          <ThemeToggle />
        </div>
      </div>

      {/* Rename Thread Dialog */}
      <Dialog open={Boolean(editingThread)} onOpenChange={(open) => !open && setEditingThread(null)}>
        <DialogContent className="max-w-sm">
          <DialogHeader>
            <DialogTitle className="font-serif text-base">Rename Consultation</DialogTitle>
            <DialogDescription className="text-xs text-muted-foreground">
              Update the title for this legal consultation thread.
            </DialogDescription>
          </DialogHeader>
          <div className="py-2">
            <Input
              value={newTitle}
              onChange={(e) => setNewTitle(e.target.value)}
              placeholder="Consultation title..."
              className="text-sm"
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSaveRename()
                }
              }}
            />
          </div>
          <DialogFooter className="gap-2">
            <Button variant="outline" size="sm" onClick={() => setEditingThread(null)}>
              Cancel
            </Button>
            <Button size="sm" onClick={handleSaveRename}>
              Save
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Quick Search Dialog */}
      <Dialog open={isSearchOpen} onOpenChange={setIsSearchOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="font-serif text-base flex items-center gap-2">
              <Search className="size-4 text-primary" />
              Search Consultations
            </DialogTitle>
            <DialogDescription className="text-xs text-muted-foreground">
              Quickly find past research threads and legal consultations.
            </DialogDescription>
          </DialogHeader>
          <div className="py-2">
            <Input
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search by topic, statute, or keyword..."
              className="text-sm"
              autoFocus
            />
          </div>
          <div className="max-h-60 overflow-y-auto space-y-1">
            {filteredSearchThreads.length === 0 ? (
              <p className="py-4 text-center text-xs text-muted-foreground">
                No consultations match your search.
              </p>
            ) : (
              filteredSearchThreads.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => {
                    setIsSearchOpen(false)
                    router.push(`/chat?thread=${t.id}`)
                  }}
                  className="w-full text-left rounded-lg p-2 hover:bg-muted transition text-xs"
                >
                  <p className="font-medium text-foreground truncate">{t.title}</p>
                  <p className="font-mono text-[10px] text-muted-foreground">{t.category} · {t.updated_at}</p>
                </button>
              ))
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" size="sm" onClick={() => setIsSearchOpen(false)}>
              Close
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </aside>
  )
}
