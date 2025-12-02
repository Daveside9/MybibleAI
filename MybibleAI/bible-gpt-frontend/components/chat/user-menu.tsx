"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Settings, LogOut, Crown } from "lucide-react"
import { SettingsDialog } from "./settings-dialog"
import type { SubscriptionTier } from "@/lib/subscription"

interface UserMenuProps {
  subscriptionTier: SubscriptionTier
}

export function UserMenu({ subscriptionTier }: UserMenuProps) {
  const router = useRouter()
  const [settingsOpen, setSettingsOpen] = useState(false)
  const [userName, setUserName] = useState("User")
  const [userEmail, setUserEmail] = useState("user@example.com")

  useEffect(() => {
    // Get user info from localStorage
    const userStr = localStorage.getItem('user')
    if (userStr) {
      try {
        const user = JSON.parse(userStr)
        setUserName(user.name || user.email.split('@')[0])
        setUserEmail(user.email)
      } catch (e) {
        console.error('Failed to parse user data')
      }
    }
  }, [])

  const handleLogout = () => {
    if (confirm("Are you sure you want to log out?")) {
      // Clear all local storage
      localStorage.clear()
      // Redirect to login
      router.push("/login")
    }
  }

  return (
    <>
      <div className="space-y-2">
        {/* User Info */}
        <div className="px-3 py-2 bg-muted/50 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-semibold truncate">{userName}</p>
              <p className="text-xs text-muted-foreground truncate">{userEmail}</p>
              <div className="flex items-center gap-1 mt-1">
                {subscriptionTier === 'premium' ? (
                  <span className="text-xs bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                    <Crown className="w-3 h-3" />
                    Premium
                  </span>
                ) : (
                  <span className="text-xs text-muted-foreground">
                    Free Plan
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="space-y-1">
          <Button
            variant="ghost"
            className="w-full justify-start"
            onClick={() => setSettingsOpen(true)}
          >
            <Settings className="mr-2 h-4 w-4" />
            Settings
          </Button>
          <Button
            variant="ghost"
            className="w-full justify-start text-destructive hover:text-destructive hover:bg-destructive/10"
            onClick={handleLogout}
          >
            <LogOut className="mr-2 h-4 w-4" />
            Log out
          </Button>
        </div>
      </div>

      <SettingsDialog
        open={settingsOpen}
        onOpenChange={setSettingsOpen}
        userName={userName}
        userEmail={userEmail}
        subscriptionTier={subscriptionTier}
        onClearHistory={() => {
          // Trigger a page reload to refresh the chat list
          window.location.reload()
        }}
      />
    </>
  )
}
