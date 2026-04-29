import { LegalSidebar } from "@/components/legal/sidebar"
import { MobileHeader } from "@/components/legal/mobile-header"

export default function AppShellLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex min-h-svh bg-background">
      <LegalSidebar />
      <div className="flex min-w-0 flex-1 flex-col lg:ml-72">
        <MobileHeader />
        {children}
      </div>
    </div>
  )
}
