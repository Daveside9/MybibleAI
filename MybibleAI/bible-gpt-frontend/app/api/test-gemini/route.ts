const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || ""

export async function GET() {
  try {
    if (!apiKey || apiKey === "your_google_api_key_here") {
      return Response.json({ 
        error: "API key not configured",
        hasKey: false,
        keyLength: 0
      }, { status: 500 })
    }

    // Test with a simple prompt
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
              text: "Say hello"
            }]
          }]
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {
      return Response.json({ 
        error: "API request failed",
        status: response.status,
        details: data,
        hasKey: true,
        keyLength: apiKey.length
      }, { status: response.status })
    }

    return Response.json({ 
      success: true,
      hasKey: true,
      keyLength: apiKey.length,
      response: data.candidates?.[0]?.content?.parts?.[0]?.text || "No response",
      message: "API key is working!"
    })
  } catch (error: any) {
    return Response.json({ 
      error: error.message,
      hasKey: !!apiKey,
      keyLength: apiKey.length
    }, { status: 500 })
  }
}
