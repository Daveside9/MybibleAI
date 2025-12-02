"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Plus, MessageSquare, Trash2, X } from "lucide-react"
import { UserMenu } from "./user-menu"
import type { SubscriptionTier } from "@/lib/subscription"

interface ChatHistory {
  id: string
  title: string
  timestamp: number
  messages: Array<{ id: number; text: string; sender: "user" | "bot"; timestamp: Date }>
}

interface ChatSidebarProps {
  currentChatId: string | null
  onSelectChat: (chatId: string) => void
  onNewChat: () => void
  onDeleteChat: (chatId: string) => void
  isOpen: boolean
  onClose: () => void
  subscriptionTier: SubscriptionTier
}

export function ChatSidebar({
  currentChatId,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  isOpen,
  onClose,
  subscriptionTier,
}: ChatSidebarProps) {
  const [chats, setChats] = useState<ChatHistory[]>([])

  useEffect(() => {
    loadChats()
    // Reload chats when sidebar opens
  }, [isOpen])

  const loadChats = () => {
    const savedChats = localStorage.getItem("bible-gpt-chats")
    if (savedChats) {
      const parsedChats = JSON.parse(savedChats)
      setChats(parsedChats.sort((a: ChatHistory, b: ChatHistory) => b.timestamp - a.timestamp))
    }
  }

  const handleDelete = (chatId: string, e: React.MouseEvent) => {
    e.stopPropagation()
    onDeleteChat(chatId)
    loadChats()
  }

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:relative inset-y-0 left-0 z-40 w-80 bg-card border-r border-border flex flex-col transition-transform duration-300 ${
          isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        {/* Header */}
        <div className="p-4 border-b border-border flex items-center justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">Bible GPT</h2>
            {chats.length > 0 && (
              <p className="text-xs text-muted-foreground">{chats.length} saved chat{chats.length !== 1 ? 's' : ''}</p>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="lg:hidden"
          >
            <X className="w-5 h-5" />
          </Button>
        </div>

        {/* New Chat Button */}
        <div className="p-4 pb-2">
          <Button
            onClick={onNewChat}
            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
          >
            <Plus className="w-4 h-4 mr-2" />
            New Chat
          </Button>
        </div>

        {/* Chat History Section */}
        <div className="px-4 py-2">
          <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Chat History
          </h3>
        </div>

        {/* Chat History List */}
        <ScrollArea className="flex-1 px-4">
          <div className="space-y-2 pb-4">
            {chats.length === 0 ? (
              <div className="text-center text-muted-foreground text-sm py-4">
                No saved chats yet.<br />
                <span className="text-xs">Start chatting to create history!</span>
              </div>
            ) : (
              chats.map((chat) => (
                <div
                  key={chat.id}
                  onClick={() => onSelectChat(chat.id)}
                  className={`group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
                    currentChatId === chat.id
                      ? "bg-primary/10 border border-primary/20"
                      : "hover:bg-accent/50"
                  }`}
                >
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    <MessageSquare className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-foreground truncate">
                        {chat.title}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(chat.timestamp).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={(e) => handleDelete(chat.id, e)}
                    className="opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    <Trash2 className="w-4 h-4 text-destructive" />
                  </Button>
                </div>
              ))
            )}
          </div>
        </ScrollArea>

        {/* Footer */}
        <div className="p-4 border-t border-border space-y-3">
          <UserMenu subscriptionTier={subscriptionTier} />
          <p className="text-xs text-muted-foreground text-center">
            Powered by Gemini 2.5 Flash
          </p>
        </div>
      </div>
    </>
  )
}
