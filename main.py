import os
import uvicorn
import sqlite3
import base64
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

app = FastAPI()

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Environment Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 3. Persistent Memory Setup (SQLite)
def init_db():
    conn = sqlite3.connect('nexus_memory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat_log 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.post("/ask")
async def nexus_core_logic(
    user_input: str = Body(..., embed=True),
    image_b64: str = Body(None, embed=True)
):
    try:
        conn = sqlite3.connect('nexus_memory.db')
        c = conn.cursor()
        
        # Fetch conversation context (Last 8 messages)
        c.execute("SELECT role, content FROM chat_log ORDER BY id DESC LIMIT 8")
        memory_rows = c.fetchall()
        context = "\n".join([f"{r}: {c}" for r, c in reversed(memory_rows)])

        # CASE 1: VISION MODE (If Image is provided)
        if image_b64:
            # Using the heavy-duty 90B Vision model
            llm_vision = ChatGroq(model_name="llama-3.2-90b-vision-preview", groq_api_key=GROQ_API_KEY)
            response = llm_vision.invoke([{"role": "user", "content": [
                {"type": "text", "text": f"Expert Mode: Solve directly and professionally. Context: {context}\nQuestion: {user_input}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}])
            answer = response.content

        # CASE 2: SEARCH MODE (If Internet Search is triggered)
        elif any(key in user_input.lower() for key in ["latest", "current", "news", "today", "weather"]):
            search_tool = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
            search_results = search_tool.run(user_input)
            llm_chat = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            response = llm_chat.invoke(f"Search Data: {search_results}\nContext: {context}\nUser: {user_input}\nNexus (Direct Solve):")
            answer = response.content

        # CASE 3: STANDARD PROFESSIONAL CHAT
        else:
            llm_chat = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            system_prompt = f"System: You are Nexus Flow AI, a professional developer assistant. Solve directly without fluff.\nContext:\n{context}\nUser: {user_input}\nNexus:"
            response = llm_chat.invoke(system_prompt)
            answer = response.content

        # Save to Memory
        c.execute("INSERT INTO chat_log (role, content) VALUES (?, ?)", ("user", user_input))
        c.execute("INSERT INTO chat_log (role, content) VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()

        return {"response": answer}

    except Exception as e:
        return {"response": f"System Error: {str(e)} ⚠️ (Check API Keys)"}

if __name__ == "__main__":
    # Railway-ready port binding
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
