from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
db = client["allrounder_ai"]
collection = db["chat_history"]

def save_message(subject: str, role: str, message: str):
    # Normalize role before saving
    if role == "bot":
        role = "assistant"  # ✅ important for Ollama compatibility

    doc = {
        "subject": subject,
        "role": role,
        "message": message,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(doc)

def load_conversation(subject: str):
    # Normalize roles during load just in case there are old values
    history = list(collection.find({"subject": subject}).sort("timestamp", 1))
    for entry in history:
        if entry["role"] == "bot":
            entry["role"] = "assistant"
    return history
