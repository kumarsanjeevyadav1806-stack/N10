import os
import uvicorn
import sqlite3
import base64
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

app = FastAPI()

# 1. CORS Setup for Streamlit Connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. API Keys (Railway Environment Variables)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# 3. DATABASE SETUP (Long-term Memory)
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
        
        # 1. Fetch Last 10 messages for Deep Context
        c.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT 10")
        rows = c.fetchall()
        past_memory = "\n".join([f"{r}: {c}" for r, c in reversed(rows)])

        # 2. VISION LOGIC (Fixed: Llama 3.2 90B Vision)
        if image_b64:
            # Humne yahan naya model use kiya hai jo decommissioning error nahi dega
            llm = ChatGroq(model_name="llama-3.2-90b-vision-preview", groq_api_key=GROQ_API_KEY)
            res = llm.invoke([{"role": "user", "content": [
                {"type": "text", "text": f"System: Directly solve the problem in the image. Memory: {past_memory}\nUser Question: {user_input}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}])
            answer = res.content
        
        # 3. INTERNET SEARCH LOGIC (Tavily)
        elif any(word in user_input.lower() for word in ["latest", "news", "today", "search", "weather", "current"]):
            if not TAVILY_API_KEY:
                answer = "Sanjeev, please add TAVILY_API_KEY in Railway to use Internet Search! 🌐"
            else:
                search = TavilySearchResults(tavily_api_key=TAVILY_API_KEY)
                search_data = search.run(user_input)
                llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
                res = llm.invoke(f"Internet Data: {search_data}\n\nUser: {user_input}\nNexus (Provide direct answer):")
                answer = res.content
            
        # 4. NORMAL CHAT (Llama 3.3 70B Expert)
        else:
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            full_prompt = f"System: You are Nexus Flow AI. Solve directly. Do not explain features.\nMemory:\n{past_memory}\nUser: {user_input}\nNexus:"
            res = llm.invoke(full_prompt)
            answer = res.content

        # 5. Save Interaction to Memory
        c.execute("INSERT INTO history (role, content) VALUES (?, ?)", ("user", user_input))
        c.execute("INSERT INTO history (role, content) VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()

        return {"response": answer}

    except Exception as e:
        # Error handling for decommissioned models or connection issues
        return {"response": f"God Engine Error: {str(e)} 🛑 (Check if GROQ API is active)"}

if __name__ == "__main__":
    # Standard Railway Port binding
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
