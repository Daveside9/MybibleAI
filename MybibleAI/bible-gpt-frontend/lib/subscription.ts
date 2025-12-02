// Subscription types and utilities

export type SubscriptionTier = 'free' | 'premium'

export interface SubscriptionPlan {
  tier: SubscriptionTier
  name: string
  price: number
  features: string[]
  messageLimit: number | null // null means unlimited
}

export const PLANS: Record<SubscriptionTier, SubscriptionPlan> = {
  free: {
    tier: 'free',
    name: 'Free Plan',
    price: 0,
    features: [
      '300 messages per day',
      'Basic Bible search',
      'Chat history',
      'Bookmarks',
    ],
    messageLimit: 300,
  },
  premium: {
    tier: 'premium',
    name: 'Premium Plan',
    price: 9.99,
    features: [
      'Unlimited messages',
      'Priority AI responses',
      'Advanced verse analysis',
      'Export conversations',
      'Voice input',
      'No ads',
    ],
    messageLimit: null,
  },
}

export interface UserSubscription {
  tier: SubscriptionTier
  messagesUsedToday: number
  lastResetDate: string
  subscriptionEndDate?: string
}

export function getDefaultSubscription(): UserSubscription {
  return {
    tier: 'free',
    messagesUsedToday: 0,
    lastResetDate: new Date().toISOString().split('T')[0],
  }
}

export function checkMessageLimit(subscription: UserSubscription): {
  canSend: boolean
  remaining: number | null
} {
  const plan = PLANS[subscription.tier]
  
  // Reset daily counter if it's a new day
  const today = new Date().toISOString().split('T')[0]
  if (subscription.lastResetDate !== today) {
    subscription.messagesUsedToday = 0
    subscription.lastResetDate = today
  }

  if (plan.messageLimit === null) {
    return { canSend: true, remaining: null }
  }

  const remaining = plan.messageLimit - subscription.messagesUsedToday
  return {
    canSend: remaining > 0,
    remaining: Math.max(0, remaining),
  }
}

export function incrementMessageCount(subscription: UserSubscription): UserSubscription {
  return {
    ...subscription,
    messagesUsedToday: subscription.messagesUsedToday + 1,
  }
}
