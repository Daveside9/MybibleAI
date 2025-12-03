const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || ""
console.log("API Key exists:", !!apiKey, "Length:", apiKey.length)

export async function POST(request: Request) {
  try {
    // Check if API key is configured
    if (!apiKey || apiKey === "your_google_api_key_here") {
      console.error("API key not configured properly")
      return Response.json({ 
        error: "API key not configured. Please add your GEMINI_API_KEY to .env.local file" 
      }, { status: 500 })
    }

    const { messages } = await request.json()

    if (!messages || !Array.isArray(messages)) {
      return Response.json({ error: "Invalid messages" }, { status: 400 })
    }

    const systemPrompt = `You are Bible GPT, a knowledgeable assistant specializing in biblical knowledge. 
You provide insights about scripture, explain passages, answer theological questions, 
and help users explore the Bible. Always be respectful, educational, and cite relevant 
verses when appropriate. Format your responses in a clear, conversational manner.`

    // Convert messages to a single prompt
    const conversationHistory = messages.map(m => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`).join('\n')
    const fullPrompt = `${systemPrompt}\n\n${conversationHistory}`

    // Use v1beta API with gemini-2.5-flash
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          contents: [{
            parts: [{
              text: fullPrompt
            }]
          }]
        })
      }
    )

    if (!response.ok) {
      const errorText = await response.text()
      console.error("Gemini API error:", response.status, errorText)
      throw new Error(`Gemini API error: ${response.status} - ${errorText}`)
    }

    const data = await response.json()
    const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "No response generated"

    return Response.json({ response: text })
  } catch (error: any) {
    console.error("Chat API error:", error)
    console.error("Error details:", error.message, error.status, error.statusText)
    return Response.json(
      {
        error: error instanceof Error ? error.message : "Failed to generate response",
        details: error.statusText || error.status || "Unknown error"
      },
      { status: 500 }
    )
  }
}