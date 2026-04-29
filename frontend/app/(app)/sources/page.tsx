import { BookMarked, Search, Filter, Star } from "lucide-react"
import { SourceCard } from "@/components/legal/source-card"
import { CategoryChips } from "@/components/legal/category-chips"
import { EmptyState } from "@/components/legal/empty-state"
import { categories, sampleSources } from "@/lib/legal-data"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const allSources = [
  ...sampleSources,
  {
    id: "src-5",
    type: "case" as const,
    title: "Olga Tellis v. Bombay Municipal Corp.",
    citation: "(1985) 3 SCC 545",
    jurisdiction: "Supreme Court of India",
    year: 1985,
    excerpt:
      "Right to life under Article 21 includes the right to livelihood; pavement dwellers cannot be evicted without due process.",
  },
  {
    id: "src-6",
    type: "case" as const,
    title: "K.S. Puttaswamy v. Union of India",
    citation: "(2017) 10 SCC 1",
    jurisdiction: "Supreme Court of India",
    year: 2017,
    excerpt:
      "The right to privacy is a fundamental right under Articles 14, 19 and 21 of the Constitution.",
  },
  {
    id: "src-7",
    type: "regulation" as const,
    title: "RBI Master Direction on KYC",
    citation: "RBI/2016-17/29 DBR.AML.BC.No.81/14.01.001/2015-16",
    jurisdiction: "Reserve Bank of India",
    year: 2016,
    excerpt:
      "All regulated entities shall undertake Customer Due Diligence as per the prescribed norms before establishing an account-based relationship.",
  },
]

export default function SourcesPage() {
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
              Every case, statute, and commentary you&apos;ve cited or starred.
              Searchable, exportable, always accessible.
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <div className="relative">
              <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search citations..."
                className="h-9 w-64 rounded-full border-border bg-card/50 pl-9 text-sm"
              />
            </div>
            <Button
              variant="outline"
              size="sm"
              className="h-9 gap-1.5 rounded-full border-border bg-card/50"
            >
              <Filter className="size-3.5" />
              Filter
            </Button>
          </div>
        </header>

        <div className="mt-6">
          <CategoryChips categories={categories} />
        </div>

        <Tabs defaultValue="all" className="mt-8">
          <TabsList className="bg-muted/40">
            <TabsTrigger value="all" className="gap-1.5 text-xs">
              All
              <span className="font-mono text-[10px] text-muted-foreground">
                {allSources.length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="cases" className="gap-1.5 text-xs">
              Cases
              <span className="font-mono text-[10px] text-muted-foreground">
                {allSources.filter((s) => s.type === "case").length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="statutes" className="gap-1.5 text-xs">
              Statutes
              <span className="font-mono text-[10px] text-muted-foreground">
                {allSources.filter((s) => s.type === "statute").length}
              </span>
            </TabsTrigger>
            <TabsTrigger value="starred" className="gap-1.5 text-xs">
              <Star className="size-3" />
              Starred
            </TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-6">
            <div className="grid gap-3 md:grid-cols-2">
              {allSources.map((s, i) => (
                <SourceCard key={s.id} source={s} index={i} />
              ))}
            </div>
          </TabsContent>

          <TabsContent value="cases" className="mt-6">
            <div className="grid gap-3 md:grid-cols-2">
              {allSources
                .filter((s) => s.type === "case")
                .map((s, i) => (
                  <SourceCard key={s.id} source={s} index={i} />
                ))}
            </div>
          </TabsContent>

          <TabsContent value="statutes" className="mt-6">
            <div className="grid gap-3 md:grid-cols-2">
              {allSources
                .filter((s) => s.type === "statute")
                .map((s, i) => (
                  <SourceCard key={s.id} source={s} index={i} />
                ))}
            </div>
          </TabsContent>

          <TabsContent value="starred" className="mt-6">
            <EmptyState
              icon={BookMarked}
              title="No starred sources yet"
              description="Star sources in any chat to keep your most-referenced citations one click away."
              action={
                <Button asChild className="gap-1.5">
                  <a href="/chat">Start a research session</a>
                </Button>
              }
            />
          </TabsContent>
        </Tabs>
      </div>
    </main>
  )
}
