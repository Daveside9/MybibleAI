"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"
import { Trash2, Download, Crown } from "lucide-react"
import type { SubscriptionTier } from "@/lib/subscription"

interface SettingsDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  userName: string
  userEmail: string
  subscriptionTier: SubscriptionTier
  onClearHistory?: () => void
}

export function SettingsDialog({
  open,
  onOpenChange,
  userName,
  userEmail,
  subscriptionTier,
  onClearHistory,
}: SettingsDialogProps) {
  const [darkMode, setDarkMode] = useState(false)
  const [notifications, setNotifications] = useState(true)

  useEffect(() => {
    // Load settings from localStorage
    const savedDarkMode = localStorage.getItem("bible-gpt-dark-mode")
    const savedNotifications = localStorage.getItem("bible-gpt-notifications")
    
    if (savedDarkMode) setDarkMode(savedDarkMode === "true")
    if (savedNotifications) setNotifications(savedNotifications === "true")
  }, [])

  const handleDarkModeToggle = (checked: boolean) => {
    setDarkMode(checked)
    localStorage.setItem("bible-gpt-dark-mode", String(checked))
    // Apply dark mode
    if (checked) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }

  const handleNotificationsToggle = (checked: boolean) => {
    setNotifications(checked)
    localStorage.setItem("bible-gpt-notifications", String(checked))
  }

  const handleClearHistory = () => {
    if (confirm("Are you sure you want to clear all chat history? This cannot be undone.")) {
      localStorage.removeItem("bible-gpt-chats")
      if (onClearHistory) {
        onClearHistory()
      }
      alert("Chat history cleared successfully!")
      onOpenChange(false)
    }
  }

  const handleClearBookmarks = () => {
    if (confirm("Are you sure you want to clear all bookmarks? This cannot be undone.")) {
      localStorage.removeItem("bible-gpt-bookmarks")
      alert("Bookmarks cleared!")
    }
  }

  const handleExportData = () => {
    const data = {
      chats: localStorage.getItem("bible-gpt-chats"),
      bookmarks: localStorage.getItem("bible-gpt-bookmarks"),
      subscription: localStorage.getItem("bible-gpt-subscription"),
      exportDate: new Date().toISOString(),
    }

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `bible-gpt-data-${new Date().toISOString().split("T")[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Settings</DialogTitle>
          <DialogDescription>
            Manage your account settings and preferences
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          {/* Account Section */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Account</h3>
              <p className="text-sm text-muted-foreground">Your account information</p>
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div>
                  <p className="text-sm font-medium">Name</p>
                  <p className="text-sm text-muted-foreground">{userName}</p>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div>
                  <p className="text-sm font-medium">Email</p>
                  <p className="text-sm text-muted-foreground">{userEmail}</p>
                </div>
              </div>
              <div className="flex items-center justify-between p-3 bg-muted rounded-lg">
                <div>
                  <p className="text-sm font-medium">Subscription</p>
                  <p className="text-sm text-muted-foreground">
                    {subscriptionTier === 'premium' ? 'Premium Plan' : 'Free Plan'}
                  </p>
                </div>
                {subscriptionTier === 'premium' && (
                  <Crown className="w-5 h-5 text-yellow-500" />
                )}
              </div>
            </div>
          </div>

          <Separator />

          {/* Appearance Section */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Appearance</h3>
              <p className="text-sm text-muted-foreground">Customize how Bible GPT looks</p>
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="dark-mode">Dark Mode</Label>
                <p className="text-sm text-muted-foreground">
                  Toggle dark mode theme
                </p>
              </div>
              <Switch
                id="dark-mode"
                checked={darkMode}
                onCheckedChange={handleDarkModeToggle}
              />
            </div>
          </div>

          <Separator />

          {/* Notifications Section */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Notifications</h3>
              <p className="text-sm text-muted-foreground">Manage notification preferences</p>
            </div>
            <div className="flex items-center justify-between">
              <div className="space-y-0.5">
                <Label htmlFor="notifications">Enable Notifications</Label>
                <p className="text-sm text-muted-foreground">
                  Receive updates and alerts
                </p>
              </div>
              <Switch
                id="notifications"
                checked={notifications}
                onCheckedChange={handleNotificationsToggle}
              />
            </div>
          </div>

          <Separator />

          {/* Data Management Section */}
          <div className="space-y-4">
            <div>
              <h3 className="text-lg font-semibold">Data Management</h3>
              <p className="text-sm text-muted-foreground">Manage your data and privacy</p>
            </div>
            <div className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start"
                onClick={handleExportData}
              >
                <Download className="mr-2 h-4 w-4" />
                Export All Data
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start text-destructive hover:text-destructive"
                onClick={handleClearHistory}
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Clear Chat History
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start text-destructive hover:text-destructive"
                onClick={handleClearBookmarks}
              >
                <Trash2 className="mr-2 h-4 w-4" />
                Clear Bookmarks
              </Button>
            </div>
          </div>

          <Separator />

          {/* About Section */}
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">About</h3>
            <div className="text-sm text-muted-foreground space-y-1">
              <p>Bible GPT v1.0.0</p>
              <p>Powered by Gemini 2.5 Flash</p>
              <p className="text-xs">© 2024 Bible GPT. All rights reserved.</p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
