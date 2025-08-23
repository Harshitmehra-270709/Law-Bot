# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import UPLawChatbot   # your existing chatbot.py
from gemini_client import ask_gemini

app = FastAPI(title="UP LawBot API")

# Allow requests from frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load chatbot once (loads your data/*.txt files)
chatbot = UPLawChatbot()

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "UP LawBot backend running"}

@app.post("/chat")
def chat(q: Question):
    if not q.question or not q.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    # Build the prompt from chatbot and call Gemini via your gemini_client
    try:
        prompt = chatbot.build_prompt(q.question)
        response = ask_gemini(prompt)   # uses your gemini_client.ask_gemini
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
