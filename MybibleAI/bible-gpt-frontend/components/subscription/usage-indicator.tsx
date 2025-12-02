"use client"

import { Crown, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { type SubscriptionTier } from "@/lib/subscription"

interface UsageIndicatorProps {
  tier: SubscriptionTier
  messagesRemaining: number | null
  messageLimit: number | null
  onUpgradeClick: () => void
}

export function UsageIndicator({
  tier,
  messagesRemaining,
  messageLimit,
  onUpgradeClick,
}: UsageIndicatorProps) {
  if (tier === 'premium') {
    return (
      <div className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-yellow-500/10 to-orange-500/10 rounded-lg border border-yellow-500/20">
        <Crown className="w-4 h-4 text-yellow-500" />
        <span className="text-sm font-medium">Premium</span>
        <span className="text-xs text-muted-foreground">Unlimited</span>
      </div>
    )
  }

  if (messageLimit === null || messagesRemaining === null) {
    return null
  }

  const usagePercent = ((messageLimit - messagesRemaining) / messageLimit) * 100
  const isLow = messagesRemaining <= 3

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
          <Zap className={`w-4 h-4 ${isLow ? 'text-destructive' : 'text-primary'}`} />
          <span className="font-medium">
            {messagesRemaining} message{messagesRemaining !== 1 ? 's' : ''} left today
          </span>
        </div>
        <Button
          variant="ghost"
          size="sm"
          onClick={onUpgradeClick}
          className="h-7 text-xs gap-1"
        >
          <Crown className="w-3 h-3" />
          Upgrade
        </Button>
      </div>
      <Progress value={usagePercent} className="h-1.5" />
      {isLow && (
        <p className="text-xs text-destructive">
          Running low! Upgrade to Premium for unlimited messages.
        </p>
      )}
    </div>
  )
}
