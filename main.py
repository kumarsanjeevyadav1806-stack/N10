import os
import uvicorn
import sqlite3
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

app = FastAPI()

# 1. CORS Setup
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 2. Database for Context
def init_db():
    conn = sqlite3.connect('nexus_brain.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (role TEXT, content TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.post("/ask")
async def reasoning_engine(user_input: str = Body(..., embed=True), image_b64: str = Body(None, embed=True)):
    try:
        conn = sqlite3.connect('nexus_brain.db')
        c = conn.cursor()
        c.execute("SELECT role, content FROM history ORDER BY rowid DESC LIMIT 6")
        context = "\n".join([f"{r}: {c}" for r, c in reversed(c.fetchall())])

        # ADVANCED REASONING PROMPT (Thinking Power)
        # Hum AI ko 'Chain of Thought' process ke liye force kar rahe hain.
        reasoning_system_prompt = f"""
        You are Nexus Flow AI, an advanced reasoning model. 
        Before answering, perform a deep mental analysis of the user's request.
        1. Break down the problem into logical steps.
        2. Identify potential errors or edge cases.
        3. Provide the most optimized, professional solution directly.
        Context: {context}
        """

        # Using Llama 3.3 70B (Best for Reasoning)
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
        
        if image_b64:
            # High-end Vision Reasoning
            llm_vision = ChatGroq(model_name="llama-3.2-90b-vision-preview", groq_api_key=GROQ_API_KEY)
            res = llm_vision.invoke([{"role": "user", "content": [
                {"type": "text", "text": reasoning_system_prompt + f"\nAnalyze this image and solve: {user_input}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}])
        else:
            # Deep Logic Reasoning
            res = llm.invoke(f"{reasoning_system_prompt}\nUser Query: {user_input}\nNexus Reasoning & Solution:")
        
        answer = res.content
        c.execute("INSERT INTO history VALUES (?, ?)", ("user", user_input))
        c.execute("INSERT INTO history VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()
        return {"response": answer}

    except Exception as e:
        return {"response": f"Reasoning Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
