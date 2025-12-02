"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Menu, Send, Download, Bookmark, Mic, MicOff } from "lucide-react"
import { ChatSidebar } from "./chat-sidebar"
import { VerseSearch } from "./verse-search"
import { BookmarksDialog } from "./bookmarks-dialog"
import { PricingDialog } from "@/components/subscription/pricing-dialog"
import { UsageIndicator } from "@/components/subscription/usage-indicator"
import { 
  getDefaultSubscription, 
  checkMessageLimit, 
  incrementMessageCount,
  type UserSubscription 
} from "@/lib/subscription"

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

interface ChatHistory {
  id: string
  title: string
  timestamp: number
  messages: Message[]
}

export function ChatWindow() {
  const [currentChatId, setCurrentChatId] = useState<string | null>(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Welcome to Bible GPT! Ask me anything about scripture, passages, theological concepts, or biblical stories. I'm here to help you explore and understand the Bible.",
      sender: "bot",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [subscription, setSubscription] = useState<UserSubscription>(getDefaultSubscription())
  const [pricingOpen, setPricingOpen] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Load subscription from localStorage
  useEffect(() => {
    const saved = localStorage.getItem("bible-gpt-subscription")
    if (saved) {
      setSubscription(JSON.parse(saved))
    }
  }, [])

  // Save subscription to localStorage
  useEffect(() => {
    localStorage.setItem("bible-gpt-subscription", JSON.stringify(subscription))
  }, [subscription])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Save chat to localStorage whenever messages change
  useEffect(() => {
    if (currentChatId && messages.length > 1) {
      saveCurrentChat()
    }
  }, [messages, currentChatId])

  const saveCurrentChat = () => {
    if (!currentChatId) return

    const chats = JSON.parse(localStorage.getItem("bible-gpt-chats") || "[]")
    const chatIndex = chats.findIndex((c: ChatHistory) => c.id === currentChatId)
    
    const chatTitle = messages.find(m => m.sender === "user")?.text.slice(0, 50) || "New Chat"
    
    const chatData: ChatHistory = {
      id: currentChatId,
      title: chatTitle,
      timestamp: Date.now(),
      messages: messages,
    }

    if (chatIndex >= 0) {
      chats[chatIndex] = chatData
    } else {
      chats.unshift(chatData)
    }

    localStorage.setItem("bible-gpt-chats", JSON.stringify(chats))
  }

  const loadChat = (chatId: string) => {
    const chats = JSON.parse(localStorage.getItem("bible-gpt-chats") || "[]")
    const chat = chats.find((c: ChatHistory) => c.id === chatId)
    
    if (chat) {
      setCurrentChatId(chatId)
      setMessages(chat.messages.map((m: Message) => ({
        ...m,
        timestamp: new Date(m.timestamp)
      })))
      setSidebarOpen(false)
    }
  }

  const startNewChat = () => {
    const newChatId = `chat-${Date.now()}`
    setCurrentChatId(newChatId)
    setMessages([
      {
        id: 1,
        text: "Welcome to Bible GPT! Ask me anything about scripture, passages, theological concepts, or biblical stories. I'm here to help you explore and understand the Bible.",
        sender: "bot",
        timestamp: new Date(),
      },
    ])
    setSidebarOpen(false)
  }

  const deleteChat = (chatId: string) => {
    const chats = JSON.parse(localStorage.getItem("bible-gpt-chats") || "[]")
    const filteredChats = chats.filter((c: ChatHistory) => c.id !== chatId)
    localStorage.setItem("bible-gpt-chats", JSON.stringify(filteredChats))
    
    if (currentChatId === chatId) {
      startNewChat()
    }
  }

  // Initialize with a chat ID on first load or load most recent chat
  useEffect(() => {
    if (!currentChatId) {
      const chats = JSON.parse(localStorage.getItem("bible-gpt-chats") || "[]")
      if (chats.length > 0) {
        // Load the most recent chat
        const mostRecentChat = chats[0]
        loadChat(mostRecentChat.id)
      } else {
        // Start a new chat
        setCurrentChatId(`chat-${Date.now()}`)
      }
    }
  }, [])

  // Export chat as text file
  const exportChat = () => {
    const chatContent = messages
      .map((msg) => {
        const time = new Date(msg.timestamp).toLocaleString()
        const sender = msg.sender === "user" ? "You" : "Bible GPT"
        return `[${time}] ${sender}:\n${msg.text}\n`
      })
      .join("\n")

    const blob = new Blob([chatContent], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `bible-gpt-chat-${new Date().toISOString().split("T")[0]}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  // Bookmark a message
  const bookmarkMessage = (messageId: number) => {
    const message = messages.find((m) => m.id === messageId)
    if (!message) return

    const bookmarks = JSON.parse(localStorage.getItem("bible-gpt-bookmarks") || "[]")
    const bookmark = {
      id: `bookmark-${Date.now()}`,
      messageId,
      text: message.text,
      sender: message.sender,
      timestamp: Date.now(),
      chatId: currentChatId,
    }

    bookmarks.unshift(bookmark)
    localStorage.setItem("bible-gpt-bookmarks", JSON.stringify(bookmarks))
    alert("Message bookmarked!")
  }

  // Voice input
  const [isListening, setIsListening] = useState(false)
  const [recognition, setRecognition] = useState<any>(null)

  useEffect(() => {
    if (typeof window !== "undefined" && "webkitSpeechRecognition" in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition
      const recognitionInstance = new SpeechRecognition()
      recognitionInstance.continuous = false
      recognitionInstance.interimResults = false
      recognitionInstance.lang = "en-US"

      recognitionInstance.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript
        setInput(transcript)
        setIsListening(false)
      }

      recognitionInstance.onerror = () => {
        setIsListening(false)
      }

      recognitionInstance.onend = () => {
        setIsListening(false)
      }

      setRecognition(recognitionInstance)
    }
  }, [])

  const toggleVoiceInput = () => {
    if (!recognition) {
      alert("Voice input is not supported in your browser. Please use Chrome or Edge.")
      return
    }

    if (isListening) {
      recognition.stop()
      setIsListening(false)
    } else {
      recognition.start()
      setIsListening(true)
    }
  }

  const handleUpgrade = () => {
    // In a real app, this would integrate with Stripe or another payment processor
    // For now, we'll just upgrade the user locally
    setSubscription({
      ...subscription,
      tier: 'premium',
      subscriptionEndDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
    })
    alert("🎉 Upgraded to Premium! (Demo mode - no payment required)")
  }

  const handleSendMessage = async () => {
    if (!input.trim()) return

    // Check message limit
    const limitCheck = checkMessageLimit(subscription)
    if (!limitCheck.canSend) {
      setPricingOpen(true)
      return
    }

    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: "user",
      timestamp: new Date(),
    }

    setMessages([...messages, userMessage])
    setInput("")
    setLoading(true)

    // Increment message count
    setSubscription(incrementMessageCount(subscription))

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          messages: [
            ...messages.map(m => ({
              role: m.sender === "user" ? "user" : "assistant",
              content: m.text
            })),
            { role: "user", content: input }
          ]
        }),
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: "Failed to parse error response" }))
        throw new Error(errorData.error || "Failed to get response")
      }

      const data = await response.json()
      const aiText = data.response

      const botMessage: Message = {
        id: messages.length + 2,
        text: aiText || "Sorry, I couldn't generate a response.",
        sender: "bot",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      const errorMessage: Message = {
        id: messages.length + 2,
        text: "Sorry, I encountered an error processing your question. Please try again.",
        sender: "bot",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <ChatSidebar
        currentChatId={currentChatId}
        onSelectChat={loadChat}
        onNewChat={startNewChat}
        onDeleteChat={deleteChat}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        subscriptionTier={subscription.tier}
      />

      {/* Main Chat Area */}
      <div className="flex flex-col flex-1 h-full">
        {/* Header */}
        <div className="border-b border-border px-6 py-4 bg-card space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="rounded-lg hover:bg-accent/20"
              >
                <Menu className="w-5 h-5" />
              </Button>
              <div>
                <h2 className="text-xl font-semibold text-foreground">Scripture Explorer</h2>
                <p className="text-xs text-muted-foreground">Ask questions about the Bible</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <VerseSearch onVerseSelect={(verse) => {
                setInput(verse)
                setTimeout(() => handleSendMessage(), 100)
              }} />
              <BookmarksDialog />
              <Button
                variant="ghost"
                size="icon"
                onClick={exportChat}
                className="rounded-lg hover:bg-accent/20"
                title="Export chat"
              >
                <Download className="w-5 h-5" />
              </Button>
              <PricingDialog
                currentTier={subscription.tier}
                onUpgrade={handleUpgrade}
              />
            </div>
          </div>
          
          {/* Usage Indicator */}
          <UsageIndicator
            tier={subscription.tier}
            messagesRemaining={checkMessageLimit(subscription).remaining}
            messageLimit={subscription.tier === 'free' ? 300 : null}
            onUpgradeClick={() => setPricingOpen(true)}
          />
        </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-4 bg-background">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div className="flex items-start gap-2 max-w-2xl">
              {message.sender === "bot" && (
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => bookmarkMessage(message.id)}
                  className="mt-2 h-6 w-6 opacity-0 hover:opacity-100 transition-opacity"
                  title="Bookmark this message"
                >
                  <Bookmark className="w-3 h-3" />
                </Button>
              )}
              <div className={`rounded-xl px-4 py-3 ${
                message.sender === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-accent/20"
              }`}>
                <p className="text-sm whitespace-pre-wrap">{message.text}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-accent/20 rounded-xl px-4 py-3 max-w-md">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-primary rounded-full animate-pulse"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-pulse animation-delay-200"></div>
                <div className="w-2 h-2 bg-primary rounded-full animate-pulse animation-delay-400"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

        {/* Input */}
        <div className="border-t border-border px-6 py-4 bg-card">
          <div className="flex gap-2">
            <Button
              onClick={toggleVoiceInput}
              disabled={loading}
              variant={isListening ? "default" : "ghost"}
              size="icon"
              className="rounded-xl"
              title={isListening ? "Stop listening" : "Voice input"}
            >
              {isListening ? <MicOff className="w-4 h-4" /> : <Mic className="w-4 h-4" />}
            </Button>
            <Input
              type="text"
              placeholder={isListening ? "Listening..." : "Ask about verses, topics, or ask for explanations..."}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSendMessage()}
              disabled={loading}
              className="flex-1 bg-input border-border rounded-xl placeholder:text-muted-foreground"
            />
            <Button
              onClick={handleSendMessage}
              disabled={loading || !input.trim()}
              className="bg-primary hover:bg-primary/90 text-primary-foreground rounded-xl px-4"
              size="icon"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
