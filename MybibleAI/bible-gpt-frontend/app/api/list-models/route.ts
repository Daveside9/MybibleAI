const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || ""

export async function GET() {
  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models?key=${apiKey}`
    )

    const data = await response.json()
    
    return Response.json({ 
      models: data.models?.map((m: any) => m.name) || [],
      fullData: data
    })
  } catch (error: any) {
    return Response.json({ error: error.message }, { status: 500 })
  }
}
