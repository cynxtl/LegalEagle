"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  Plus,
  MessageSquare,
  FileText,
  BookMarked,
  Settings,
  Sparkles,
  Upload,
  Search,
  ChevronRight,
} from "lucide-react"
import { Logo } from "./logo"
import { sampleThreads } from "@/lib/legal-data"
import { Button } from "@/components/ui/button"
import { DocumentUploadCard } from "./document-upload-card"
import { ThemeToggle } from "./theme-toggle"
import { cn } from "@/lib/utils"

const quickLinks = [
  { href: "/chat", label: "Ask a Question", icon: Sparkles },
  { href: "/documents", label: "Upload a File", icon: Upload },
  { href: "/sources", label: "Saved Sources", icon: BookMarked },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function LegalSidebar() {
  const pathname = usePathname()

  return (
    <aside className="fixed left-0 top-0 hidden h-svh w-72 flex-col border-r border-sidebar-border bg-sidebar lg:flex">
      <div className="flex items-center justify-between border-b border-sidebar-border px-4 py-4">
        <Link href="/" aria-label="LegalEagle home">
          <Logo />
        </Link>
        <button
          aria-label="Search"
          className="flex size-8 items-center justify-center rounded-lg text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
        >
          <Search className="size-4" />
        </button>
      </div>

      <div className="border-b border-sidebar-border px-3 py-2">
        <Button
          asChild
          className="w-full justify-start gap-2 rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20 hover:bg-primary/15"
        >
          <Link href="/chat">
            <Plus className="size-4" />
            New consultation
          </Link>
        </Button>
      </div>

      <nav className="flex-1 overflow-y-auto px-3 py-4">
        <div className="mb-2 flex items-center justify-between px-2">
          <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            Recent threads
          </span>
          <span className="font-mono text-[10px] text-muted-foreground">
            {sampleThreads.length}
          </span>
        </div>
        <ul className="space-y-0.5">
          {sampleThreads.map((thread) => (
            <li key={thread.id}>
              <Link
                href={`/chat?thread=${thread.id}`}
                className="group flex items-start gap-2 rounded-md px-2 py-2 text-sm transition-colors hover:bg-sidebar-accent"
              >
                <MessageSquare className="mt-0.5 size-3.5 shrink-0 text-muted-foreground" />
                <div className="min-w-0 flex-1">
                  <p className="truncate text-xs font-medium leading-tight">
                    {thread.title}
                  </p>
                  <div className="mt-0.5 flex items-center gap-1.5">
                    <span className="font-mono text-[10px] text-muted-foreground">
                      {thread.updatedAt}
                    </span>
                    <span className="size-0.5 rounded-full bg-muted-foreground/40" />
                    <span className="truncate text-[10px] text-muted-foreground">
                      {thread.category}
                    </span>
                  </div>
                </div>
                <ChevronRight className="mt-0.5 size-3 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
              </Link>
            </li>
          ))}
        </ul>

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
        <DocumentUploadCard variant="compact" />
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
    </aside>
  )
}
