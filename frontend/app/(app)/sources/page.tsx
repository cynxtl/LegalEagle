"use client"

import { useEffect, useState } from "react"
import { BookMarked, Search, Filter, Star, Sparkles } from "lucide-react"
import Link from "next/link"
import { SourceCard } from "@/components/legal/source-card"
import { CategoryChips } from "@/components/legal/category-chips"
import { EmptyState } from "@/components/legal/empty-state"
import { categories } from "@/lib/legal-data"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import type { Source } from "@/lib/legal-data"

export default function SourcesPage() {
  const [sources, setSources] = useState<Source[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")

  const fetchSources = async () => {
    try {
      setIsLoading(true)
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
      const res = await fetch(`${API_URL}/api/v1/sources`)
      if (res.ok) {
        const data = await res.json()
        setSources(
          data.map((s: any) => ({
            id: s.id,
            title: s.title || "Retrieved Document",
            citation: s.citation || "",
            jurisdiction: s.jurisdiction || "",
            year: s.year || 0,
            excerpt: s.excerpt || "",
            url: s.url,
            type: s.type || "retrieved_chunk",
            is_starred: s.is_starred || false,
          }))
        )
      }
    } catch (e) {
      console.error("Failed to fetch sources:", e)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchSources()
  }, [])

  const [selectedCategory, setSelectedCategory] = useState<any>(null)

  const filteredSources = sources.filter((s) => {
    const queryMatch =
      s.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      s.excerpt.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (s.citation && s.citation.toLowerCase().includes(searchQuery.toLowerCase()))

    if (!queryMatch) return false

    if (selectedCategory) {
      const text = `${s.title} ${s.citation || ""} ${s.excerpt}`.toLowerCase()
      if (selectedCategory === "Criminal Law") {
        return text.includes("criminal") || text.includes("ipc") || text.includes("bns") || text.includes("penal") || text.includes("murder") || text.includes("cheating")
      }
      if (selectedCategory === "Constitution") {
        return text.includes("constitution") || text.includes("article") || text.includes("fundamental")
      }
      if (selectedCategory === "Procedure") {
        return text.includes("procedure") || text.includes("crpc") || text.includes("bnss") || text.includes("bail") || text.includes("fir")
      }
      if (selectedCategory === "Tax") {
        return text.includes("tax") || text.includes("cit") || text.includes("income")
      }
      if (selectedCategory === "Property") {
        return text.includes("property") || text.includes("tenant") || text.includes("rent") || text.includes("lease")
      }
      return text.includes(String(selectedCategory).toLowerCase())
    }

    return true
  })

  const caseSources = filteredSources.filter((s) => s.type === "case")
  const statuteSources = filteredSources.filter(
    (s) => s.type === "statute" || s.type === "regulation" || s.type === "retrieved_chunk"
  )
  const starredSources = filteredSources.filter((s: any) => s.is_starred)

  return (
    <main className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-6xl px-4 py-8 lg:px-8 lg:py-10">
        <header className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
              Library
            </span>
            <h1 className="mt-1 font-serif text-3xl tracking-tight md:text-4xl">
              Saved sources & citations.
            </h1>
            <p className="mt-1.5 max-w-xl text-sm text-muted-foreground">
              Every case, statute, and judgment retrieved during consultations.
              Searchable, verified against FAISS legal embeddings.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search citations..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="h-9 w-64 rounded-full border-border bg-card/50 pl-9 text-sm"
              />
            </div>
          </div>
        </header>

        <div className="mt-6">
          <CategoryChips
            categories={categories}
            value={selectedCategory}
            onChange={setSelectedCategory}
          />
        </div>

        <Tabs defaultValue="all" className="mt-8">
          <TabsList className="bg-muted/40">
            <TabsTrigger value="all" className="gap-1.5 text-xs">
              All
              <span className="font-mono text-[10px] text-muted-foreground">
                {filteredSources.length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="cases" className="gap-1.5 text-xs">
              Cases
              <span className="font-mono text-[10px] text-muted-foreground">
                {caseSources.length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="statutes" className="gap-1.5 text-xs">
              Statutes / Chunks
              <span className="font-mono text-[10px] text-muted-foreground">
                {statuteSources.length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="starred" className="gap-1.5 text-xs">
              <Star className="size-3" />
              Starred
              <span className="font-mono text-[10px] text-muted-foreground">
                {starredSources.length}
              </span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-6">
            {filteredSources.length === 0 && !isLoading ? (
              <EmptyState
                icon={BookMarked}
                title="No citations grounded yet"
                description="Consultations in chat automatically extract and index citations into this library."
                action={
                  <Button asChild className="gap-1.5">
                    <Link href="/chat">
                      <Sparkles className="size-4" />
                      Start a consultation
                    </Link>
                  </Button>
                }
              />
            ) : (
              <div className="grid gap-3 md:grid-cols-2">
                {filteredSources.map((s, i) => (
                  <SourceCard key={s.id || i} source={s} index={i} />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="cases" className="mt-6">
            {caseSources.length === 0 ? (
              <EmptyState
                icon={BookMarked}
                title="No case citations found"
                description="Case citations will appear here when retrieved in consultations."
              />
            ) : (
              <div className="grid gap-3 md:grid-cols-2">
                {caseSources.map((s, i) => (
                  <SourceCard key={s.id || i} source={s} index={i} />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="statutes" className="mt-6">
            {statuteSources.length === 0 ? (
              <EmptyState
                icon={BookMarked}
                title="No statute passages found"
                description="Statutory chunks will appear here when retrieved in consultations."
              />
            ) : (
              <div className="grid gap-3 md:grid-cols-2">
                {statuteSources.map((s, i) => (
                  <SourceCard key={s.id || i} source={s} index={i} />
                ))}
              </div>
            )}
          </TabsContent>

          <TabsContent value="starred" className="mt-6">
            {starredSources.length === 0 ? (
              <EmptyState
                icon={BookMarked}
                title="No starred sources yet"
                description="Star sources in any chat to keep your most-referenced citations one click away."
                action={
                  <Button asChild className="gap-1.5">
                    <Link href="/chat">Start a research session</Link>
                  </Button>
                }
              />
            ) : (
              <div className="grid gap-3 md:grid-cols-2">
                {starredSources.map((s, i) => (
                  <SourceCard key={s.id || i} source={s} index={i} />
                ))}
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}
