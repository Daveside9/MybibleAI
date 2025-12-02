import { GoogleGenerativeAI } from "@google/generative-ai"

const apiKey = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY || ""
const genAI = new GoogleGenerativeAI(apiKey)

export async function GET() {
  try {
    const models = await genAI.listModels()
    return Response.json({ 
      models: models.map(m => ({
        name: m.name,
        displayName: m.displayName,
        supportedMethods: m.supportedGenerationMethods
      }))
    })
  } catch (error: any) {
    console.error("Error listing models:", error)
    return Response.json({ error: error.message }, { status: 500 })
  }
}
