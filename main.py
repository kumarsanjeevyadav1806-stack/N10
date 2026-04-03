import os
import sqlite3
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB ---
def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat
    (id INTEGER PRIMARY KEY, role TEXT, content TEXT)
    """)
    conn.commit()
    conn.close()

init_db()

# --- TOOL: Calculator ---
def calculator(q):
    try:
        return str(eval(q))
    except:
        return None

# --- API ---
@app.post("/ask")
async def ask(data: dict = Body(...)):
    user_input = data.get("user_input")
    messages = data.get("messages", [])
    pdf_text = data.get("pdf_text")

    # --- TOOL USE ---
    if any(op in user_input for op in ["+", "-", "*", "/"]):
        result = calculator(user_input)
        if result:
            return {"response": f"🧮 Answer: {result}"}

    # --- PDF Context ---
    if pdf_text:
        user_input += f"\n\nDocument:\n{pdf_text[:3000]}"

    # --- SYSTEM PROMPT ---
    system = {
        "role": "system",
        "content": """You are Nexus Flow AI (PRO).
You are as powerful as ChatGPT.

Abilities:
- Memory
- Coding
- Explanation
- Reasoning
- Document analysis

Always give structured, clean answers."""
    }

    final_messages = [system] + messages + [{"role":"user","content":user_input}]

    llm = ChatGroq(
        temperature=0.5,
        model_name="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY")
    )

    res = llm.invoke(final_messages)
    answer = res.content

    return {"response": answer}
