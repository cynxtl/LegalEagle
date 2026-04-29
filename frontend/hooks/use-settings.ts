"use client"

import { useCallback, useState, useEffect } from "react"

export interface SettingsState {
  fullName: string
  email: string
  firm: string
  role: "partner" | "associate" | "paralegal" | "student" | "inhouse"
  jurisdiction: "in" | "uk" | "us" | "eu"
  language: "en" | "hi"
  citationFormat: "bluebook" | "oscola" | "ili"
  showConfidence: boolean
  showSources: boolean
  showReasoning: boolean
  answerStyle: "concise" | "balanced" | "thorough"
  retainHistory: boolean
  indexDocuments: boolean
  caseAlerts: boolean
  processingAlerts: boolean
  weeklyDigest: boolean
}

const DEFAULT_SETTINGS: SettingsState = {
  fullName: "Anjali Verma",
  email: "anjali@sharma-law.in",
  firm: "Sharma & Associates",
  role: "associate",
  jurisdiction: "in",
  language: "en",
  citationFormat: "ili",
  showConfidence: true,
  showSources: true,
  showReasoning: false,
  answerStyle: "balanced",
  retainHistory: true,
  indexDocuments: true,
  caseAlerts: true,
  processingAlerts: true,
  weeklyDigest: false,
}

const STORAGE_KEY = "legaleagle-settings"

export function useSettings() {
  const [settings, setSettings] = useState<SettingsState>(DEFAULT_SETTINGS)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Load settings from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        const parsed = JSON.parse(stored)
        setSettings((prev) => ({ ...prev, ...parsed }))
      }
    } catch (err) {
      console.error("Failed to load settings:", err)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const updateSettings = useCallback((updates: Partial<SettingsState>) => {
    setSettings((prev) => {
      const updated = { ...prev, ...updates }
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
      } catch (err) {
        console.error("Failed to save settings:", err)
        setError("Failed to save settings")
      }
      return updated
    })
  }, [])

  const updateProfile = useCallback(
    (fullName: string, email: string, firm: string, role: SettingsState["role"]) => {
      updateSettings({ fullName, email, firm, role })
    },
    [updateSettings]
  )

  const updateJurisdiction = useCallback(
    (
      jurisdiction: SettingsState["jurisdiction"],
      language: SettingsState["language"],
      citationFormat: SettingsState["citationFormat"]
    ) => {
      updateSettings({ jurisdiction, language, citationFormat })
    },
    [updateSettings]
  )

  const updateAIBehavior = useCallback(
    (
      showConfidence: boolean,
      showSources: boolean,
      showReasoning: boolean,
      answerStyle: SettingsState["answerStyle"]
    ) => {
      updateSettings({ showConfidence, showSources, showReasoning, answerStyle })
    },
    [updateSettings]
  )

  const updatePrivacy = useCallback(
    (retainHistory: boolean, indexDocuments: boolean) => {
      updateSettings({ retainHistory, indexDocuments })
    },
    [updateSettings]
  )

  const updateNotifications = useCallback(
    (caseAlerts: boolean, processingAlerts: boolean, weeklyDigest: boolean) => {
      updateSettings({ caseAlerts, processingAlerts, weeklyDigest })
    },
    [updateSettings]
  )

  const resetSettings = useCallback(() => {
    setSettings(DEFAULT_SETTINGS)
    try {
      localStorage.removeItem(STORAGE_KEY)
    } catch (err) {
      console.error("Failed to reset settings:", err)
    }
  }, [])

  return {
    settings,
    isLoading,
    error,
    updateSettings,
    updateProfile,
    updateJurisdiction,
    updateAIBehavior,
    updatePrivacy,
    updateNotifications,
    resetSettings,
  }
}
