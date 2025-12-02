"use client"

import { ChatWindow } from "@/components/chat/chat-window"

export function ChatDashboard() {
  return (
    <div className="flex h-screen bg-background text-foreground">
      {/* Chat Window */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatWindow />
      </div>
    </div>
  )
}