# AllRounderAI 🤖

AllRounderAI is a versatile chatbot built with Python, FastAPI, and Flet UI, using a custom local model powered by Ollama. It stores chat history per topic in MongoDB and reloads the conversation if the user resumes the same topic.

---

## 💠 Features

- Chatbot interface with subject-based conversations  
- Local model using Ollama (custom `allrounder` model)  
- MongoDB integration for persistent chat history  
- Modern desktop UI built with Flet  
- Fully local and private  

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/andriiVIt/AllRounderAI.git
cd AllRounderAI
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama and create the custom model

```bash
ollama run llama3
ollama create allrounder -f Modelfile
```

### 5. Run the backend

```bash
uvicorn main:app --reload
```

### 6. Run the UI

```bash
python app.py
```

---

## 🧠 Notes

- MongoDB must be running locally on default port `27017`  
- Make sure Ollama is installed and the custom model is created before sending chat messages  

---

## 📁 File Structure

```
AllRounderAI/
├── app.py                # Flet UI
├── main.py               # FastAPI backend
├── db.py                 # MongoDB logic
├── Modelfile             # Ollama custom model file
├── requirements.txt
└── README.md
```

---

Enjoy chatting with **AllRounderAI**! 😎
