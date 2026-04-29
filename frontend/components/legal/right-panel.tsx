import {
  Landmark,
  Gavel,
  FileText,
  AlertTriangle,
  ListChecks,
} from "lucide-react"
import { sampleSources } from "@/lib/legal-data"
import { SourceCard } from "./source-card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"

export function RightPanel({ className }: { className?: string }) {
  return (
    <aside
      className={cn(
        "fixed right-0 top-0 hidden h-svh w-[360px] flex-col border-l border-border bg-card/30 xl:flex",
        className
      )}
    >
      <div className="border-b border-border px-5 py-4">
        <div>
          <h2 className="font-serif text-base tracking-tight">
            Research panel
          </h2>
          <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            Live citations · current thread
          </p>
        </div>
      </div>

      <Tabs defaultValue="sources" className="flex flex-1 flex-col overflow-hidden">
        <TabsList className="mx-5 grid h-9 grid-cols-3 bg-muted/40">
          <TabsTrigger value="sources" className="text-xs">
            Sources
          </TabsTrigger>
          <TabsTrigger value="acts" className="text-xs">
            Acts
          </TabsTrigger>
          <TabsTrigger value="summary" className="text-xs">
            Summary
          </TabsTrigger>
        </TabsList>

        <div className="flex-1 overflow-y-auto">
          <TabsContent
            value="sources"
            className="px-5 py-4"
          >
            <SectionHeader
              icon={Gavel}
              label="Sources used"
              count={sampleSources.length}
            />
            <div className="space-y-2.5">
              {sampleSources.slice(0, 3).map((src, i) => (
                <SourceCard key={src.id} source={src} index={i} />
              ))}
            </div>

            <div className="mt-6">
              <SectionHeader icon={FileText} label="Case references" count={2} />
              <ul className="space-y-1.5">
                {[
                  {
                    title: "Olga Tellis v. Bombay Municipal Corp.",
                    cite: "(1985) 3 SCC 545",
                  },
                  {
                    title: "K.S. Puttaswamy v. Union of India",
                    cite: "(2017) 10 SCC 1",
                  },
                ].map((c) => (
                  <li
                    key={c.cite}
                    className="rounded-lg border border-border bg-card/40 px-3 py-2"
                  >
                    <p className="text-xs font-medium leading-tight">
                      {c.title}
                    </p>
                    <p className="font-mono text-[10px] text-muted-foreground">
                      {c.cite}
                    </p>
                  </li>
                ))}
              </ul>
            </div>
          </TabsContent>

          <TabsContent value="acts" className="px-5 py-4">
            <SectionHeader icon={Landmark} label="Relevant acts & sections" />
            <ul className="space-y-2">
              {[
                {
                  act: "Rent Control Act, 1958",
                  section: "§ 14(1)(a)",
                  desc: "Grounds for eviction — non-payment of rent",
                },
                {
                  act: "Transfer of Property Act, 1882",
                  section: "§ 106",
                  desc: "Notice requirements for tenancy termination",
                },
                {
                  act: "Code of Civil Procedure, 1908",
                  section: "Order XV-A",
                  desc: "Procedure for eviction suits",
                },
                {
                  act: "Constitution of India",
                  section: "Art. 21",
                  desc: "Right to shelter as part of right to life",
                },
              ].map((a) => (
                <li
                  key={a.section}
                  className="rounded-lg border border-border bg-card/40 p-3"
                >
                  <div className="flex items-baseline justify-between gap-2">
                    <p className="text-xs font-medium leading-tight">{a.act}</p>
                    <span className="shrink-0 font-mono text-[10px] text-accent">
                      {a.section}
                    </span>
                  </div>
                  <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                    {a.desc}
                  </p>
                </li>
              ))}
            </ul>
          </TabsContent>

          <TabsContent
            value="summary"
            className="px-5 py-4"
          >
            <SectionHeader icon={ListChecks} label="Answer summary" />
            <div className="rounded-xl border border-border bg-card/40 p-4">
              <ul className="space-y-2 text-xs leading-relaxed">
                {[
                  "Statutory notice (15–30 days) is mandatory before eviction.",
                  "Petition must be filed before the Rent Controller.",
                  "Tenant may deposit arrears with interest to avoid eviction.",
                  "Self-help eviction is illegal and criminally actionable.",
                ].map((s, i) => (
                  <li key={i} className="flex gap-2">
                    <span className="mt-1.5 size-1 shrink-0 rounded-full bg-primary" />
                    <span>{s}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="mt-4">
              <SectionHeader icon={AlertTriangle} label="Risk & confidence notes" />
              <div className="space-y-2">
                <div className="rounded-lg border border-accent/30 bg-accent/5 p-3">
                  <p className="text-[11px] font-medium text-accent-foreground">
                    Jurisdictional variance
                  </p>
                  <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                    Rent Control Acts vary by state. Verify provisions for your
                    specific jurisdiction.
                  </p>
                </div>
                <div className="rounded-lg border border-border bg-card/40 p-3">
                  <p className="text-[11px] font-medium">Recency</p>
                  <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                    Cited cases are current as of 2024. Newer rulings may not yet
                    be indexed.
                  </p>
                </div>
              </div>
            </div>
          </TabsContent>
        </div>
      </Tabs>
    </aside>
  )
}

function SectionHeader({
  icon: Icon,
  label,
  count,
}: {
  icon: typeof Gavel
  label: string
  count?: number
}) {
  return (
    <div className="mb-3 mt-4 flex items-center gap-2">
      <Icon className="size-3.5 text-primary" />
      <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
        {label}
      </span>
      {count !== undefined && (
        <span className="font-mono text-[10px] text-muted-foreground">
          · {count}
        </span>
      )}
      <div className="h-px flex-1 bg-border" />
    </div>
  )
}
