import os
import uvicorn
import sqlite3
import json
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE SETUP (SQLite) ---
def init_db():
    conn = sqlite3.connect('nexus_chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    try:
        # 1. Save User Message to Database
        conn = sqlite3.connect('nexus_chat.db')
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)", ("user", user_input))
        
        # 2. Get Past Context (Last 20 messages for reasoning)
        c.execute("SELECT role, content FROM chat_history ORDER BY id DESC LIMIT 20")
        rows = c.fetchall()
        history_str = "\n".join([f"{r}: {c}" for r, c in reversed(rows)])
        
        # 3. Call AI with History
        llm = ChatGroq(temperature=0.6, groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        
        prompt = f"System: You are Nexus Flow AI by Sanjeev Kumar with long-term memory.\nHistory:\n{history_str}\nNexus Flow AI:"
        res = llm.invoke(prompt)
        answer = res.content
        
        # 4. Save AI Response to Database
        c.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()
        
        return {"response": answer}

    except Exception as e:
        return {"response": f"Memory Error: {str(e)}"}

# New Endpoint to fetch all history (for UI)
@app.get("/history")
async def get_history():
    conn = sqlite3.connect('nexus_chat.db')
    c = conn.cursor()
    c.execute("SELECT role, content FROM chat_history ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in rows]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
