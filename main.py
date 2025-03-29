from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI()

class ChatRequest(BaseModel):
    subject: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    messages = [
        {"role": "user", "content": f"(Subject: {req.subject}) {req.message}"}
    ]

    response = ollama.chat(
        model="allrounder",  # назва моделі (створимо далі)
        messages=messages,
        options={
            "temperature": 0.7,
            "top_p": 0.9
        }
    )
    reply_text = response["message"]["content"]

    return ChatResponse(reply=reply_text)
