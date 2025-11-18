# gemini_client.py
from google import genai
import os

class GeminiClient:
    def __init__(self, model="models/gemini-2.0-flash"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing!")

        self.model = model
        self.client = genai.Client(api_key=api_key)

    def generate(self, prompt, max_tokens=300, temperature=0.2):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            return response.text
        except Exception as e:
            return f"[ERROR] {e}"
