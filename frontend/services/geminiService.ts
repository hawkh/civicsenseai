
import { GoogleGenAI, Type } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export interface AIAnalysis {
  category: string;
  department: string;
  severity: 'Low' | 'Medium' | 'High';
  shortDescription: string;
}

export const analyzeIssue = async (base64Image: string): Promise<AIAnalysis> => {
  try {
    const response = await ai.models.generateContent({
      model: 'gemini-3-flash-preview',
      contents: {
        parts: [
          {
            inlineData: {
              mimeType: 'image/jpeg',
              data: base64Image.split(',')[1] || base64Image,
            },
          },
          {
            text: "Analyze this image of a civic issue. Identify the category of the problem, the likely government department responsible, the severity (Low, Medium, High), and provide a concise one-sentence description. Format your response as JSON.",
          },
        ],
      },
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            category: { type: Type.STRING },
            department: { type: Type.STRING },
            severity: { 
              type: Type.STRING,
              description: "Must be 'Low', 'Medium', or 'High'"
            },
            shortDescription: { type: Type.STRING },
          },
          required: ["category", "department", "severity", "shortDescription"],
        },
      },
    });

    return JSON.parse(response.text || "{}") as AIAnalysis;
  } catch (error) {
    console.error("AI Analysis failed:", error);
    // Fallback if AI fails
    return {
      category: "Uncategorized Civic Issue",
      department: "General Administration",
      severity: "Medium",
      shortDescription: "A civic issue was reported via image."
    };
  }
};
