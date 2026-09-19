"use client"

import { useState, useEffect } from "react"
import {
  User,
  Globe2,
  Bell,
  ShieldCheck,
  Brain,
  CreditCard,
  Trash2,
  Check,
  RotateCcw,
  Save,
} from "lucide-react"
import { SettingsCard, SettingsRow } from "@/components/legal/settings-card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { useSettings } from "@/hooks/use-settings"

export default function SettingsPage() {
  const {
    settings,
    updateSettings,
    resetSettings,
  } = useSettings()

  const [form, setForm] = useState(settings)
  const [savedSuccess, setSavedSuccess] = useState(false)
  const [resetSuccess, setResetSuccess] = useState(false)

  useEffect(() => {
    setForm(settings)
  }, [settings])

  const handleSave = () => {
    updateSettings(form)
    setSavedSuccess(true)
    setTimeout(() => setSavedSuccess(false), 2500)
  }

  const handleReset = () => {
    resetSettings()
    setResetSuccess(true)
    setTimeout(() => setResetSuccess(false), 2500)
  }

  const handleDeleteWorkspace = () => {
    localStorage.clear()
    sessionStorage.clear()
    window.location.href = "/"
  }

  return (
    <main className="flex-1 overflow-y-auto">
      <div className="mx-auto max-w-3xl px-4 py-8 lg:px-8 lg:py-10">
        <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-primary">
              Settings
            </span>
            <h1 className="mt-1 font-serif text-3xl tracking-tight md:text-4xl">
              Workspace preferences.
            </h1>
            <p className="mt-1.5 max-w-xl text-sm text-muted-foreground">
              Configure your account, jurisdiction, AI behavior, and privacy controls.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={handleReset}
              className="gap-1.5 text-xs"
            >
              <RotateCcw className="size-3.5" />
              Reset Defaults
            </Button>
            <Button
              size="sm"
              onClick={handleSave}
              className="gap-1.5 text-xs bg-primary text-primary-foreground"
            >
              {savedSuccess ? (
                <>
                  <Check className="size-3.5 text-emerald-300" />
                  Saved!
                </>
              ) : (
                <>
                  <Save className="size-3.5" />
                  Save Preferences
                </>
              )}
            </Button>
          </div>
        </header>

        {savedSuccess && (
          <div className="mt-4 rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-2.5 text-center text-xs text-emerald-600 dark:text-emerald-400 font-medium">
            ✓ Preferences saved successfully to local storage.
          </div>
        )}

        {resetSuccess && (
          <div className="mt-4 rounded-lg border border-amber-500/30 bg-amber-500/10 p-2.5 text-center text-xs text-amber-600 dark:text-amber-400 font-medium">
            ✓ Settings have been reset to default values.
          </div>
        )}

        <div className="mt-8 space-y-5">
          <SettingsCard
            icon={User}
            title="Profile"
            description="How you appear inside LegalEagle."
          >
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-1.5">
                <Label htmlFor="name" className="text-xs">
                  Full name
                </Label>
                <Input
                  id="name"
                  value={form.fullName}
                  onChange={(e) => setForm((prev) => ({ ...prev, fullName: e.target.value }))}
                />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="email" className="text-xs">
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  value={form.email}
                  onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
                />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="firm" className="text-xs">
                  Firm / Organization
                </Label>
                <Input
                  id="firm"
                  value={form.firm}
                  onChange={(e) => setForm((prev) => ({ ...prev, firm: e.target.value }))}
                />
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="role" className="text-xs">
                  Role
                </Label>
                <Select
                  value={form.role}
                  onValueChange={(val: any) => setForm((prev) => ({ ...prev, role: val }))}
                >
                  <SelectTrigger id="role">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="partner">Partner</SelectItem>
                    <SelectItem value="associate">Associate</SelectItem>
                    <SelectItem value="paralegal">Paralegal</SelectItem>
                    <SelectItem value="student">Law Student</SelectItem>
                    <SelectItem value="inhouse">In-house Counsel</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </SettingsCard>

          <SettingsCard
            icon={Globe2}
            title="Jurisdiction & language"
            description="Sets the legal corpus LegalEagle searches by default."
          >
            <SettingsRow
              label="Primary jurisdiction"
              description="Used for default retrieval, citations, and statute lookups."
              control={
                <Select
                  value={form.jurisdiction}
                  onValueChange={(val: any) => setForm((prev) => ({ ...prev, jurisdiction: val }))}
                >
                  <SelectTrigger className="w-44">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="in">India (BNS/IPC)</SelectItem>
                    <SelectItem value="uk">United Kingdom</SelectItem>
                    <SelectItem value="us">United States</SelectItem>
                    <SelectItem value="eu">European Union</SelectItem>
                  </SelectContent>
                </Select>
              }
            />
            <SettingsRow
              label="Language"
              control={
                <Select
                  value={form.language}
                  onValueChange={(val: any) => setForm((prev) => ({ ...prev, language: val }))}
                >
                  <SelectTrigger className="w-44">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="hi">Hindi</SelectItem>
                  </SelectContent>
                </Select>
              }
            />
            <SettingsRow
              label="Citation format"
              description="BlueBook, OSCOLA, or Indian Law Institute style."
              control={
                <Select
                  value={form.citationFormat}
                  onValueChange={(val: any) => setForm((prev) => ({ ...prev, citationFormat: val }))}
                >
                  <SelectTrigger className="w-44">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="bluebook">BlueBook (US)</SelectItem>
                    <SelectItem value="oscola">OSCOLA (UK)</SelectItem>
                    <SelectItem value="ili">ILI (India)</SelectItem>
                  </SelectContent>
                </Select>
              }
            />
          </SettingsCard>

          <SettingsCard
            icon={Brain}
            title="AI behavior"
            description="Tune how LegalEagle reasons and what it shows you."
          >
            <SettingsRow
              label="Show confidence scores"
              description="Display a high/medium/low badge next to every assistant answer."
              control={
                <Switch
                  checked={form.showConfidence}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, showConfidence: checked }))}
                />
              }
            />
            <SettingsRow
              label="Always show sources"
              description="Cite primary sources inline by default. Disable for shorter answers."
              control={
                <Switch
                  checked={form.showSources}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, showSources: checked }))}
                />
              }
            />
            <SettingsRow
              label="Show chain of reasoning"
              description="Reveal the retrieval and reasoning steps for each answer."
              control={
                <Switch
                  checked={form.showReasoning}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, showReasoning: checked }))}
                />
              }
            />
            <SettingsRow
              label="Answer style"
              control={
                <Select
                  value={form.answerStyle}
                  onValueChange={(val: any) => setForm((prev) => ({ ...prev, answerStyle: val }))}
                >
                  <SelectTrigger className="w-44">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="concise">Concise</SelectItem>
                    <SelectItem value="balanced">Balanced</SelectItem>
                    <SelectItem value="thorough">Thorough memo</SelectItem>
                  </SelectContent>
                </Select>
              }
            />
          </SettingsCard>

          <SettingsCard
            icon={ShieldCheck}
            title="Privacy & data"
            description="Your documents are encrypted and never used for training."
          >
            <SettingsRow
              label="Retain chat history"
              description="Keep conversations in your sidebar. Disable for ephemeral sessions."
              control={
                <Switch
                  checked={form.retainHistory}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, retainHistory: checked }))}
                />
              }
            />
            <SettingsRow
              label="Index uploaded documents"
              description="Required for document Q&A. Disabling deletes existing indexes."
              control={
                <Switch
                  checked={form.indexDocuments}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, indexDocuments: checked }))}
                />
              }
            />
            <SettingsRow
              label="Two-factor authentication"
              description="Protect your account with TOTP or hardware security keys."
              control={
                <span className="inline-flex items-center gap-1 rounded-full bg-primary/10 px-2 py-0.5 text-[11px] font-medium text-primary">
                  <Check className="size-3" />
                  Enabled
                </span>
              }
            />
          </SettingsCard>

          <SettingsCard
            icon={Bell}
            title="Notifications"
            description="When LegalEagle should notify you."
          >
            <SettingsRow
              label="New case law alerts"
              description="Notify me when new judgments match my saved searches."
              control={
                <Switch
                  checked={form.caseAlerts}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, caseAlerts: checked }))}
                />
              }
            />
            <SettingsRow
              label="Document processing complete"
              control={
                <Switch
                  checked={form.processingAlerts}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, processingAlerts: checked }))}
                />
              }
            />
            <SettingsRow
              label="Weekly research digest"
              control={
                <Switch
                  checked={form.weeklyDigest}
                  onCheckedChange={(checked) => setForm((prev) => ({ ...prev, weeklyDigest: checked }))}
                />
              }
            />
          </SettingsCard>

          <SettingsCard
            icon={CreditCard}
            title="Plan & billing"
            description="You are on the Pro plan."
          >
            <div className="rounded-xl border border-primary/20 bg-primary/5 p-4">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-serif text-base">Pro · ₹2,400/mo</p>
                  <p className="text-xs text-muted-foreground">
                    Unlimited research · 50 documents/month · Priority support
                  </p>
                </div>
                <Button variant="outline" size="sm" className="bg-card/60">
                  Manage
                </Button>
              </div>
            </div>
            <p className="text-xs text-muted-foreground">
              Next invoice on{" "}
              <span className="text-foreground">October 1, 2026</span> · Visa ending 4242
            </p>
          </SettingsCard>

          <Separator className="my-2" />

          <div className="rounded-2xl border border-destructive/30 bg-destructive/5 p-6">
            <div className="flex items-start gap-3">
              <div className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-destructive/10 text-destructive ring-1 ring-destructive/20">
                <Trash2 className="size-4" />
              </div>
              <div className="min-w-0 flex-1">
                <h2 className="font-serif text-lg tracking-tight text-destructive">
                  Danger zone
                </h2>
                <p className="mt-0.5 text-sm leading-relaxed text-muted-foreground">
                  Permanently clear your local workspace cache, reset preferences,
                  and reload the application.
                </p>
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <AlertDialog>
                <AlertDialogTrigger asChild>
                  <Button variant="destructive" size="sm">
                    Delete workspace
                  </Button>
                </AlertDialogTrigger>
                <AlertDialogContent>
                  <AlertDialogHeader>
                    <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
                    <AlertDialogDescription>
                      This will reset all your saved local settings, clear local session cache,
                      and return to the home screen.
                    </AlertDialogDescription>
                  </AlertDialogHeader>
                  <AlertDialogFooter>
                    <AlertDialogCancel>Cancel</AlertDialogCancel>
                    <AlertDialogAction onClick={handleDeleteWorkspace}>
                      Confirm Reset
                    </AlertDialogAction>
                  </AlertDialogFooter>
                </AlertDialogContent>
              </AlertDialog>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
