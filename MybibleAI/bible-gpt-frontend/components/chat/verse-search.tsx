"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Search, BookOpen } from "lucide-react"

interface VerseSearchProps {
  onVerseSelect: (verse: string) => void
}

export function VerseSearch({ onVerseSelect }: VerseSearchProps) {
  const [open, setOpen] = useState(false)
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSearch = async () => {
    if (!search.trim()) return

    setLoading(true)
    // Send the verse reference to the chat
    onVerseSelect(`What does ${search} say?`)
    setOpen(false)
    setSearch("")
    setLoading(false)
  }

  const quickVerses = [
    "John 3:16",
    "Psalm 23",
    "Proverbs 3:5-6",
    "Romans 8:28",
    "Philippians 4:13",
    "Isaiah 41:10",
    "Matthew 6:33",
    "Jeremiah 29:11",
  ]

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="rounded-lg hover:bg-accent/20"
          title="Search verses"
        >
          <BookOpen className="w-5 h-5" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Search Bible Verses</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="flex gap-2">
            <Input
              placeholder="e.g., John 3:16 or Psalm 23"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
              className="flex-1"
            />
            <Button onClick={handleSearch} disabled={loading || !search.trim()}>
              <Search className="w-4 h-4 mr-2" />
              Search
            </Button>
          </div>

          <div>
            <p className="text-sm text-muted-foreground mb-2">Quick access:</p>
            <div className="grid grid-cols-2 gap-2">
              {quickVerses.map((verse) => (
                <Button
                  key={verse}
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    onVerseSelect(`What does ${verse} say?`)
                    setOpen(false)
                  }}
                  className="justify-start"
                >
                  {verse}
                </Button>
              ))}
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
