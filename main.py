import os
import uvicorn
import sqlite3
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- DATABASE SETUP (Permanent Memory) ---
def init_db():
    conn = sqlite3.connect('nexus_brain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, content TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.post("/ask")
async def nexus_god_engine(
    user_input: str = Body(..., embed=True),
    image_b64: str = Body(None, embed=True)
):
    try:
        conn = sqlite3.connect('nexus_brain.db')
        c = conn.cursor()
        
        # 1. Fetch Last 10 messages for context
        c.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT 10")
        rows = c.fetchall()
        past_memory = "\n".join([f"{r}: {c}" for r, c in reversed(rows)])

        # 2. Vision Check (If Image)
        if image_b64:
            llm = ChatGroq(model_name="llama-3.2-11b-vision-preview", groq_api_key=GROQ_API_KEY)
            res = llm.invoke([{"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}])
            answer = res.content
        
        # 3. Internet Search Check
        elif any(word in user_input.lower() for word in ["latest", "news", "today", "weather", "search"]):
            search = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
            search_data = search.run(user_input)
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            res = llm.invoke(f"Context from internet: {search_data}\n\nQuestion: {user_input}")
            answer = res.content
            
        # 4. Normal Chat with Memory
        else:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            prompt = f"System: You are Nexus Flow AI with long-term memory.\nMemory:\n{past_memory}\nUser: {user_input}\nNexus:"
            res = llm.invoke(prompt)
            answer = res.content

        # 5. Save to Permanent Memory
        c.execute("INSERT INTO history (role, content) VALUES (?, ?)", ("user", user_input))
        c.execute("INSERT INTO history (role, content) VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()

        return {"response": answer}

    except Exception as e:
        return {"response": f"God Engine Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
