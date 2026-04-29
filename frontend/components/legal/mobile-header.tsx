"use client"

import Link from "next/link"
import { Menu, Plus } from "lucide-react"
import { Logo } from "./logo"
import { Sheet, SheetContent, SheetTrigger, SheetTitle } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { sampleThreads } from "@/lib/legal-data"
import { MessageSquare, BookMarked, Settings, Upload, Sparkles } from "lucide-react"

const quickLinks = [
  { href: "/chat", label: "Ask a Question", icon: Sparkles },
  { href: "/documents", label: "Upload a File", icon: Upload },
  { href: "/sources", label: "Saved Sources", icon: BookMarked },
  { href: "/settings", label: "Settings", icon: Settings },
]

export function MobileHeader() {
  return (
    <header className="sticky top-0 z-30 flex items-center justify-between border-b border-border bg-background/80 px-4 py-3 backdrop-blur lg:hidden">
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" aria-label="Open navigation">
            <Menu className="size-5" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-80 bg-sidebar p-0">
          <SheetTitle className="sr-only">Navigation</SheetTitle>
          <div className="px-4 py-4">
            <Logo />
          </div>
          <div className="px-3">
            <Button asChild className="w-full justify-start gap-2 bg-primary/10 text-primary ring-1 ring-primary/20 hover:bg-primary/15">
              <Link href="/chat">
                <Plus className="size-4" />
                New consultation
              </Link>
            </Button>
          </div>
          <nav className="mt-4 px-3">
            <span className="mb-2 block px-2 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              Recent
            </span>
            <ul className="space-y-0.5">
              {sampleThreads.slice(0, 4).map((t) => (
                <li key={t.id}>
                  <Link
                    href="/chat"
                    className="flex items-start gap-2 rounded-md px-2 py-2 hover:bg-sidebar-accent"
                  >
                    <MessageSquare className="mt-0.5 size-3.5 text-muted-foreground" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-xs font-medium">{t.title}</p>
                      <p className="font-mono text-[10px] text-muted-foreground">
                        {t.updatedAt}
                      </p>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
            <span className="mb-2 mt-5 block px-2 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              Menu
            </span>
            <ul className="space-y-0.5">
              {quickLinks.map((l) => {
                const Icon = l.icon
                return (
                  <li key={l.href}>
                    <Link
                      href={l.href}
                      className="flex items-center gap-2.5 rounded-md px-2 py-2 text-sm text-muted-foreground hover:bg-sidebar-accent hover:text-foreground"
                    >
                      <Icon className="size-3.5" />
                      {l.label}
                    </Link>
                  </li>
                )
              })}
            </ul>
          </nav>
        </SheetContent>
      </Sheet>
      <Link href="/" aria-label="Home">
        <Logo />
      </Link>
      <Button asChild size="icon" variant="ghost" aria-label="New chat">
        <Link href="/chat">
          <Plus className="size-5" />
        </Link>
      </Button>
    </header>
  )
}
