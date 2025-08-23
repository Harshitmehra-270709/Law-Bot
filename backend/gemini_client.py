import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path= ".env")

API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash-latest')

def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"[Error communicating with Gemini API: {e}]" 