import Link from "next/link"
import {
  ArrowRight,
  Sparkles,
  Gavel,
  FileSearch,
  ShieldCheck,
  BookOpen,
  Quote,
  CheckCircle2,
  Scale,
} from "lucide-react"
import { Logo } from "@/components/legal/logo"
import { DisclaimerBanner } from "@/components/legal/disclaimer-banner"
import { ConfidenceBadge } from "@/components/legal/confidence-badge"
import { CategoryChips } from "@/components/legal/category-chips"
import { categories, sampleSources } from "@/lib/legal-data"
import { SourceCard } from "@/components/legal/source-card"
import { Button } from "@/components/ui/button"

export default function LandingPage() {
  return (
    <div className="min-h-svh bg-background">
      <SiteHeader />
      <main>
        <Hero />
        <SocialProof />
        <FeatureGrid />
        <CitationShowcase />
        <UseCases />
        <TestimonialBand />
        <CTA />
      </main>
      <SiteFooter />
    </div>
  )
}

function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 lg:px-8">
        <Link href="/" aria-label="LegalEagle home">
          <Logo />
        </Link>
        <nav className="hidden items-center gap-7 md:flex">
          {[
            { label: "Product", href: "#features" },
            { label: "Citations", href: "#citations" },
            { label: "Use cases", href: "#use-cases" },
            { label: "Pricing", href: "#" },
          ].map((l) => (
            <Link
              key={l.label}
              href={l.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {l.label}
            </Link>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Button variant="ghost" asChild className="hidden sm:inline-flex">
            <Link href="/chat">Sign in</Link>
          </Button>
          <Button asChild className="gap-1.5">
            <Link href="/chat">
              Open app
              <ArrowRight className="size-3.5" />
            </Link>
          </Button>
        </div>
      </div>
    </header>
  )
}

function Hero() {
  return (
    <section className="relative overflow-hidden border-b border-border/60">
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 bg-grain opacity-60"
      />
      <div
        aria-hidden
        className="pointer-events-none absolute -top-40 left-1/2 size-[600px] -translate-x-1/2 rounded-full bg-primary/10 blur-3xl"
      />

      <div className="relative mx-auto max-w-7xl px-4 pb-20 pt-16 lg:px-8 lg:pt-24">
        <div className="mx-auto max-w-3xl text-center">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-card/60 px-3 py-1 text-xs">
            <span className="flex size-1.5 rounded-full bg-primary" />
            <span className="font-mono uppercase tracking-wider text-muted-foreground">
              v2 · 12,000+ cases indexed weekly
            </span>
          </div>

          <h1 className="font-serif text-5xl leading-[1.05] tracking-tight text-balance md:text-6xl lg:text-7xl">
            The legal research
            <br />
            <span className="text-primary italic">co-counsel</span> you can cite.
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-base leading-relaxed text-muted-foreground text-pretty md:text-lg">
            LegalEagle v2 reads case law, statutes, and your own documents — then
            answers in plain language with verifiable citations. No hallucinated
            precedents. No more billable hours lost to research.
          </p>

          <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Button asChild size="lg" className="gap-2 rounded-full px-6">
              <Link href="/chat">
                Start researching
                <ArrowRight className="size-4" />
              </Link>
            </Button>
            <Button
              asChild
              size="lg"
              variant="outline"
              className="gap-2 rounded-full border-border bg-card/40 px-6"
            >
              <Link href="/documents">
                <FileSearch className="size-4" />
                Analyze a document
              </Link>
            </Button>
          </div>

          <p className="mt-6 font-mono text-[11px] uppercase tracking-wider text-muted-foreground">
            Trusted by 4,200+ lawyers · Free for students
          </p>
        </div>

        <div className="mx-auto mt-14 max-w-5xl">
          <ChatPreview />
        </div>
      </div>
    </section>
  )
}

function ChatPreview() {
  return (
    <div className="rounded-3xl border border-border bg-card/60 p-3 shadow-2xl shadow-primary/5 ring-1 ring-border/40">
      <div className="rounded-2xl border border-border/60 bg-background">
        <div className="flex items-center justify-between border-b border-border/60 px-4 py-2.5">
          <div className="flex items-center gap-2">
            <div className="flex gap-1">
              <span className="size-2.5 rounded-full bg-muted" />
              <span className="size-2.5 rounded-full bg-muted" />
              <span className="size-2.5 rounded-full bg-muted" />
            </div>
            <span className="ml-2 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              legaleagle.app/chat
            </span>
          </div>
          <span className="font-mono text-[10px] text-muted-foreground">
            Thread · Property
          </span>
        </div>

        <div className="grid gap-0 md:grid-cols-[1fr_320px]">
          <div className="space-y-5 p-6">
            <div className="flex justify-end">
              <div className="max-w-[80%] rounded-2xl rounded-tr-md border border-border bg-secondary/40 px-4 py-2.5 text-sm">
                Can a landlord evict a tenant who has missed two months of rent
                without giving notice?
              </div>
            </div>

            <div className="flex gap-3">
              <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/20">
                <Sparkles className="size-3.5 text-primary" />
              </div>
              <div className="flex-1 space-y-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">LegalEagle</span>
                  <ConfidenceBadge level="high" />
                </div>
                <p className="text-sm leading-relaxed text-foreground/90">
                  No. Under most Rent Control Acts, a landlord must serve
                  written statutory notice (typically 15–30 days) before filing
                  for eviction. The tenant retains the right to cure default by
                  depositing arrears with interest before the final order.
                  <span className="ml-1 inline-flex items-baseline gap-0.5 align-baseline">
                    <a
                      href="#"
                      className="font-mono text-[10px] text-primary hover:underline"
                    >
                      [1]
                    </a>
                    <a
                      href="#"
                      className="font-mono text-[10px] text-primary hover:underline"
                    >
                      [2]
                    </a>
                  </span>
                </p>

                <div className="grid gap-2 sm:grid-cols-2">
                  {sampleSources.slice(0, 2).map((src, i) => (
                    <SourceCard
                      key={src.id}
                      source={src}
                      index={i}
                      variant="compact"
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-border/60 bg-card/40 p-5 md:border-l md:border-t-0">
            <div className="flex items-center gap-2">
              <Gavel className="size-3.5 text-primary" />
              <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                Acts referenced
              </span>
            </div>
            <ul className="mt-3 space-y-2">
              {[
                { act: "Rent Control Act, 1958", section: "§ 14(1)(a)" },
                { act: "Transfer of Property Act", section: "§ 106" },
                { act: "Code of Civil Procedure", section: "Order XV-A" },
              ].map((a) => (
                <li
                  key={a.section}
                  className="flex items-baseline justify-between gap-2 rounded-lg border border-border bg-card/60 p-2.5"
                >
                  <span className="text-xs font-medium leading-tight">
                    {a.act}
                  </span>
                  <span className="font-mono text-[10px] text-accent">
                    {a.section}
                  </span>
                </li>
              ))}
            </ul>

            <div className="mt-4 rounded-lg border border-accent/20 bg-accent/5 p-3">
              <div className="flex items-center gap-1.5 text-[11px] font-medium text-accent">
                <Scale className="size-3" />
                Risk note
              </div>
              <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
                Provisions vary by state. Verify your jurisdiction.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function SocialProof() {
  return (
    <section className="border-b border-border/60 py-10">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        <p className="text-center font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
          Built for the world&apos;s most demanding legal teams
        </p>
        <div className="mx-auto mt-6 grid max-w-4xl grid-cols-2 items-center gap-x-8 gap-y-4 opacity-70 sm:grid-cols-3 md:grid-cols-5">
          {[
            "Khaitan & Co.",
            "AZB Partners",
            "Trilegal",
            "Cyril Amarchand",
            "Shardul Mangaldas",
          ].map((firm) => (
            <span
              key={firm}
              className="text-center font-serif text-base tracking-tight text-muted-foreground"
            >
              {firm}
            </span>
          ))}
        </div>
      </div>
    </section>
  )
}

function FeatureGrid() {
  const features = [
    {
      icon: BookOpen,
      title: "Verifiable citations",
      desc: "Every answer points to a paragraph in a real case, statute, or section. Click to verify the source.",
      tag: "No hallucinations",
    },
    {
      icon: FileSearch,
      title: "Document analysis",
      desc: "Upload contracts, FIRs, and judgments. LegalEagle indexes them and answers from your private corpus.",
      tag: "PDF · DOCX · 25 MB",
    },
    {
      icon: ShieldCheck,
      title: "Confidential by design",
      desc: "End-to-end encrypted. Your documents are never used for model training. SOC 2 Type II.",
      tag: "Enterprise grade",
    },
    {
      icon: Gavel,
      title: "Jurisdiction-aware",
      desc: "Switch between Indian, UK, US, and EU corpora. Get answers grounded in the right legal system.",
      tag: "Multi-jurisdiction",
    },
  ]

  return (
    <section id="features" className="border-b border-border/60 py-20">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
            What it does
          </span>
          <h2 className="mt-3 font-serif text-4xl tracking-tight text-balance md:text-5xl">
            Research like a senior associate.
            <br />
            <span className="text-muted-foreground italic">
              Cite like one too.
            </span>
          </h2>
        </div>

        <div className="mt-14 grid gap-4 md:grid-cols-2">
          {features.map((f) => {
            const Icon = f.icon
            return (
              <div
                key={f.title}
                className="group relative overflow-hidden rounded-2xl border border-border bg-card/60 p-6 transition-colors hover:border-primary/30"
              >
                <div className="flex items-start justify-between">
                  <div className="flex size-11 items-center justify-center rounded-xl bg-primary/10 text-primary ring-1 ring-primary/20">
                    <Icon className="size-5" />
                  </div>
                  <span className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                    {f.tag}
                  </span>
                </div>
                <h3 className="mt-5 font-serif text-2xl tracking-tight">
                  {f.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {f.desc}
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

function CitationShowcase() {
  return (
    <section id="citations" className="border-b border-border/60 py-20">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
              The citation engine
            </span>
            <h2 className="mt-3 font-serif text-4xl tracking-tight text-balance md:text-5xl">
              Every claim, traceable to the page.
            </h2>
            <p className="mt-4 text-base leading-relaxed text-muted-foreground">
              LegalEagle does not just summarise. It quotes — with paragraph-level
              precision from primary sources. Open the original document in a
              click, and copy a citation in BlueBook, OSCOLA, or ILI format.
            </p>

            <ul className="mt-6 space-y-3">
              {[
                "Paragraph-level grounding from primary sources",
                "Automatic confidence scoring per answer",
                "BlueBook, OSCOLA, ILI citation export",
                "Full chain of reasoning, always inspectable",
              ].map((p) => (
                <li
                  key={p}
                  className="flex items-start gap-2.5 text-sm text-foreground/90"
                >
                  <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-primary" />
                  {p}
                </li>
              ))}
            </ul>

            <div className="mt-8">
              <DisclaimerBanner />
            </div>
          </div>

          <div className="space-y-3">
            {sampleSources.slice(0, 3).map((src, i) => (
              <SourceCard key={src.id} source={src} index={i} />
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

function UseCases() {
  return (
    <section id="use-cases" className="border-b border-border/60 py-20">
      <div className="mx-auto max-w-7xl px-4 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
            Built for every practice area
          </span>
          <h2 className="mt-3 font-serif text-4xl tracking-tight text-balance md:text-5xl">
            From criminal defense to corporate due diligence.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted-foreground">
            Filter your research by jurisdiction and category. LegalEagle adapts
            its retrieval and prompts to the practice area you select.
          </p>
        </div>

        <div className="mx-auto mt-10 max-w-3xl">
          <CategoryChips categories={categories} />
        </div>

        <div className="mt-14 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {[
            {
              cat: "Criminal Law",
              prompt:
                "Quash an FIR — find precedents under §482 CrPC for matrimonial disputes.",
            },
            {
              cat: "Property",
              prompt:
                "Compare adverse possession requirements across Indian states.",
            },
            {
              cat: "Contract",
              prompt:
                "Draft a force majeure clause that holds up post-pandemic.",
            },
            {
              cat: "Constitution",
              prompt:
                "Analyze a state law for Article 14 reasonable classification.",
            },
          ].map((u) => (
            <div
              key={u.cat}
              className="rounded-2xl border border-border bg-card/60 p-5 transition-colors hover:border-primary/30"
            >
              <span className="font-mono text-[10px] uppercase tracking-wider text-accent">
                {u.cat}
              </span>
              <p className="mt-3 text-sm leading-relaxed">{u.prompt}</p>
              <div className="mt-4 flex items-center gap-1.5 text-xs text-primary">
                Try this prompt
                <ArrowRight className="size-3" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function TestimonialBand() {
  return (
    <section className="border-b border-border/60 bg-card/30 py-20">
      <div className="mx-auto max-w-4xl px-4 text-center lg:px-8">
        <Quote className="mx-auto size-8 text-accent" />
        <blockquote className="mt-6 font-serif text-2xl leading-relaxed tracking-tight text-balance md:text-3xl">
          &ldquo;LegalEagle has replaced three hours of database hopping with
          three minutes of grounded research. The citations alone make it
          indispensable for any litigator.&rdquo;
        </blockquote>
        <div className="mt-6 flex items-center justify-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-full bg-primary/10 font-serif text-primary ring-1 ring-primary/20">
            AS
          </div>
          <div className="text-left">
            <p className="text-sm font-medium">Anuradha Sharma</p>
            <p className="text-xs text-muted-foreground">
              Senior Partner · Sharma & Associates, Delhi
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

function CTA() {
  return (
    <section className="py-24">
      <div className="mx-auto max-w-4xl px-4 text-center lg:px-8">
        <h2 className="font-serif text-5xl tracking-tight text-balance md:text-6xl">
          Stop digging through{" "}
          <span className="italic text-muted-foreground">SCC Online</span>.
          <br />
          Start citing with confidence.
        </h2>
        <p className="mx-auto mt-5 max-w-xl text-base leading-relaxed text-muted-foreground text-pretty">
          Free to try. No credit card. Your first 50 queries are on us.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button asChild size="lg" className="gap-2 rounded-full px-7">
            <Link href="/chat">
              Open LegalEagle
              <ArrowRight className="size-4" />
            </Link>
          </Button>
          <Button
            asChild
            size="lg"
            variant="outline"
            className="rounded-full border-border bg-card/40 px-7"
          >
            <Link href="#">Talk to sales</Link>
          </Button>
        </div>
      </div>
    </section>
  )
}

function SiteFooter() {
  return (
    <footer className="border-t border-border bg-card/30">
      <div className="mx-auto grid max-w-7xl gap-10 px-4 py-14 lg:grid-cols-4 lg:px-8">
        <div className="lg:col-span-2">
          <Logo />
          <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted-foreground">
            AI-assisted legal research with verifiable citations. Made for
            lawyers, students, and informed citizens.
          </p>
          <p className="mt-4 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            © 2026 LegalEagle Inc. · All rights reserved
          </p>
        </div>
        {[
          {
            heading: "Product",
            links: ["Chat", "Document analysis", "Citations", "Pricing"],
          },
          {
            heading: "Company",
            links: ["About", "Security", "Privacy", "Terms"],
          },
        ].map((col) => (
          <div key={col.heading}>
            <p className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
              {col.heading}
            </p>
            <ul className="mt-3 space-y-2">
              {col.links.map((l) => (
                <li key={l}>
                  <a
                    href="#"
                    className="text-sm text-foreground/80 hover:text-foreground"
                  >
                    {l}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </footer>
  )
}
