import { BookOpen } from "lucide-react"
import { useEffect, useState } from "react"

interface MessageBubbleProps {
  message: {
    id: number
    text: string
    sender: "user" | "bot"
    timestamp: Date
  }
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const [formattedTime, setFormattedTime] = useState("")

  useEffect(() => {
    // This code will only run on the client, after hydration
    setFormattedTime(
      message.timestamp.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      })
    )
  }, [message.timestamp])

  return (
    <div className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-md px-4 py-3 rounded-xl ${
          message.sender === "user"
            ? "bg-primary text-primary-foreground rounded-br-none"
            : "bg-accent/10 border border-accent/20 text-foreground rounded-bl-none"
        }`}
      >
        {message.sender === "bot" && (
          <div className="flex items-center gap-2 mb-2">
            <BookOpen className="w-4 h-4 text-primary" />
            <span className="text-xs font-semibold text-primary">Bible GPT</span>
          </div>
        )}
        <p className="text-sm leading-relaxed">{message.text}</p>
        {formattedTime && (
          <p className="text-xs opacity-70 mt-2">
            {formattedTime}
          </p>
        )}
      </div>
    </div>
  )
}
