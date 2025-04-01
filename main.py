from fastapi import FastAPI
from pydantic import BaseModel
from db import save_message, load_conversation
from fastapi.responses import JSONResponse
import ollama

app = FastAPI()

class ChatRequest(BaseModel):
    subject: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/history/{subject}")
def get_history(subject: str):
    history = load_conversation(subject)
    chat = [{"role": entry["role"], "message": entry["message"]} for entry in history]
    return JSONResponse(content=chat)

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    # Load conversation history and convert for Ollama
    messages = []
    history = load_conversation(req.subject)

    for entry in history:
        messages.append({
            "role": entry["role"],
            "content": entry["message"]
        })

    # Add current user message
    messages.append({
        "role": "user",
        "content": req.message
    })

    # Send to Ollama
    response = ollama.chat(
        model="allrounder",
        messages=messages,
        options={
            "temperature": 0.7,
            "top_p": 0.9
        }
    )

    reply_text = response["message"]["content"]

    # Save both user input and assistant reply
    save_message(req.subject, "user", req.message)
    save_message(req.subject, "assistant", reply_text)

    return ChatResponse(reply=reply_text)
