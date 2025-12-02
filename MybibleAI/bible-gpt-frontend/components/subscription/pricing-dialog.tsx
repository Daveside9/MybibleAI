"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Check, Crown, Sparkles } from "lucide-react"
import { PLANS, type SubscriptionTier } from "@/lib/subscription"

interface PricingDialogProps {
  currentTier: SubscriptionTier
  onUpgrade: () => void
  trigger?: React.ReactNode
}

export function PricingDialog({ currentTier, onUpgrade, trigger }: PricingDialogProps) {
  const [open, setOpen] = useState(false)

  const handleUpgrade = () => {
    onUpgrade()
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        {trigger || (
          <Button variant="outline" className="gap-2">
            <Crown className="w-4 h-4" />
            Upgrade
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="max-w-4xl">
        <DialogHeader>
          <DialogTitle className="text-2xl">Choose Your Plan</DialogTitle>
          <DialogDescription>
            Select the plan that best fits your Bible study needs
          </DialogDescription>
        </DialogHeader>

        <div className="grid md:grid-cols-2 gap-6 mt-6">
          {/* Free Plan */}
          <div className="border rounded-lg p-6 space-y-4">
            <div className="space-y-2">
              <h3 className="text-xl font-semibold">{PLANS.free.name}</h3>
              <div className="flex items-baseline gap-1">
                <span className="text-3xl font-bold">${PLANS.free.price}</span>
                <span className="text-muted-foreground">/month</span>
              </div>
            </div>

            <ul className="space-y-3">
              {PLANS.free.features.map((feature, i) => (
                <li key={i} className="flex items-start gap-2">
                  <Check className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                  <span className="text-sm">{feature}</span>
                </li>
              ))}
            </ul>

            <Button
              variant="outline"
              className="w-full"
              disabled={currentTier === 'free'}
            >
              {currentTier === 'free' ? 'Current Plan' : 'Downgrade'}
            </Button>
          </div>

          {/* Premium Plan */}
          <div className="border-2 border-primary rounded-lg p-6 space-y-4 relative bg-primary/5">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2">
              <span className="bg-primary text-primary-foreground text-xs font-semibold px-3 py-1 rounded-full flex items-center gap-1">
                <Sparkles className="w-3 h-3" />
                POPULAR
              </span>
            </div>

            <div className="space-y-2">
              <h3 className="text-xl font-semibold flex items-center gap-2">
                {PLANS.premium.name}
                <Crown className="w-5 h-5 text-yellow-500" />
              </h3>
              <div className="flex items-baseline gap-1">
                <span className="text-3xl font-bold">${PLANS.premium.price}</span>
                <span className="text-muted-foreground">/month</span>
              </div>
            </div>

            <ul className="space-y-3">
              {PLANS.premium.features.map((feature, i) => (
                <li key={i} className="flex items-start gap-2">
                  <Check className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                  <span className="text-sm font-medium">{feature}</span>
                </li>
              ))}
            </ul>

            <Button
              className="w-full bg-primary hover:bg-primary/90"
              onClick={handleUpgrade}
              disabled={currentTier === 'premium'}
            >
              {currentTier === 'premium' ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  Current Plan
                </>
              ) : (
                <>
                  <Crown className="w-4 h-4 mr-2" />
                  Upgrade to Premium
                </>
              )}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
