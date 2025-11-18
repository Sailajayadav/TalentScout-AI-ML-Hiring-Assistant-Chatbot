# gemini_client.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # Make sure .env variables load locally

class GeminiClient:
    def __init__(self, model="models/gemini-2.0-flash"):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing!")

        # Authenticate the client
        genai.configure(api_key=api_key)
        self.model = model

    def generate(self, prompt, max_tokens=300, temperature=0.2):
        try:
            response = genai.GenerativeModel(self.model).generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": max_tokens,
                    "temperature": temperature
                }
            )
            return response.text

        except Exception as e:
            return f"[ERROR] {str(e)}"
