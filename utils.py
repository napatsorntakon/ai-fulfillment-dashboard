import os
import google.generativeai as genai

def ask_llm(prompt, context):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            return "❌ AI service is not configured."

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-2.5-flash-lite")

        full_prompt = f"{prompt}\n\n{context}"
        response = model.generate_content(full_prompt)

        return response.text

    except Exception:
        return "❌ AI service is currently unavailable. Please try again later."
