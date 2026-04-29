import type { Metadata } from "next"
import { Geist, Geist_Mono, Instrument_Serif } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/sonner"
import "./globals.css"

const geist = Geist({
  subsets: ["latin"],
  variable: "--font-geist",
})
const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
})
const instrumentSerif = Instrument_Serif({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-instrument-serif",
})

export const metadata: Metadata = {
  title: "LegalEagle v2 — AI Legal Research Assistant",
  description:
    "Trusted AI legal research, document analysis, and case-law citation. LegalEagle v2 helps lawyers, students, and citizens understand the law with verifiable sources.",
  generator: "v0.app",
  keywords: [
    "legal AI",
    "legal research",
    "case law",
    "document analysis",
    "legal chatbot",
    "law assistant",
  ],
}

export const viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#fafaf5" },
    { media: "(prefers-color-scheme: dark)", color: "#0c1220" },
  ],
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${geist.variable} ${geistMono.variable} ${instrumentSerif.variable} bg-background`}
    >
      <body className="font-sans antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="dark"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
        {process.env.NODE_ENV === "production" && <Analytics />}
      </body>
    </html>
  )
}
