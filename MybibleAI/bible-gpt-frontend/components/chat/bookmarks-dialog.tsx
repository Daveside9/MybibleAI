"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Bookmark, Trash2 } from "lucide-react"

interface BookmarkItem {
  id: string
  messageId: number
  text: string
  sender: string
  timestamp: number
  chatId: string | null
}

export function BookmarksDialog() {
  const [open, setOpen] = useState(false)
  const [bookmarks, setBookmarks] = useState<BookmarkItem[]>([])

  useEffect(() => {
    if (open) {
      loadBookmarks()
    }
  }, [open])

  const loadBookmarks = () => {
    const saved = localStorage.getItem("bible-gpt-bookmarks")
    if (saved) {
      setBookmarks(JSON.parse(saved))
    }
  }

  const deleteBookmark = (id: string) => {
    const filtered = bookmarks.filter((b) => b.id !== id)
    setBookmarks(filtered)
    localStorage.setItem("bible-gpt-bookmarks", JSON.stringify(filtered))
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
    alert("Copied to clipboard!")
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="rounded-lg hover:bg-accent/20"
          title="View bookmarks"
        >
          <Bookmark className="w-5 h-5" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-2xl max-h-[80vh]">
        <DialogHeader>
          <DialogTitle>Bookmarked Messages</DialogTitle>
        </DialogHeader>
        <ScrollArea className="h-[60vh] pr-4">
          {bookmarks.length === 0 ? (
            <div className="text-center text-muted-foreground py-8">
              No bookmarks yet. Click the bookmark icon on any AI response to save it.
            </div>
          ) : (
            <div className="space-y-4">
              {bookmarks.map((bookmark) => (
                <div
                  key={bookmark.id}
                  className="p-4 rounded-lg bg-accent/20 border border-border"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1">
                      <p className="text-sm whitespace-pre-wrap">{bookmark.text}</p>
                      <p className="text-xs text-muted-foreground mt-2">
                        {new Date(bookmark.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <div className="flex gap-1">
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => copyToClipboard(bookmark.text)}
                        className="h-8 w-8"
                        title="Copy to clipboard"
                      >
                        📋
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => deleteBookmark(bookmark.id)}
                        className="h-8 w-8"
                        title="Delete bookmark"
                      >
                        <Trash2 className="w-4 h-4 text-destructive" />
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </ScrollArea>
      </DialogContent>
    </Dialog>
  )
}
