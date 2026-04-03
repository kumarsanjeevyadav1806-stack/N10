import os
import uvicorn
import sqlite3
import base64
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

# 1. FastAPI Instance (Railway needs this at top level)
app = FastAPI()

# 2. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 3. Database Memory Setup
def init_db():
    conn = sqlite3.connect('nexus_brain.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS history (role TEXT, content TEXT)')
    conn.commit()
    conn.close()

init_db()

@app.post("/ask")
async def reasoning_engine(
    user_input: str = Body(..., embed=True), 
    image_b64: str = Body(None, embed=True)
):
    try:
        conn = sqlite3.connect('nexus_brain.db')
        c = conn.cursor()
        c.execute("SELECT role, content FROM history ORDER BY rowid DESC LIMIT 8")
        rows = c.fetchall()
        context = "\n".join([f"{r}: {c}" for r, c in reversed(rows)])

        # CHAIN OF THOUGHT PROMPT (Deep Reasoning)
        reasoning_prompt = f"""
        System: You are Nexus Flow AI, an advanced reasoning machine. 
        Analyze the problem step-by-step. Provide a direct, professional, and optimized solution.
        Context Memory: {context}
        """

        if image_b64:
            # 90B Vision for high-end image analysis
            llm = ChatGroq(model_name="llama-3.2-90b-vision-preview", groq_api_key=GROQ_API_KEY)
            res = llm.invoke([{"role": "user", "content": [
                {"type": "text", "text": reasoning_prompt + f"\nAnalyze image & Solve: {user_input}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]}])
        else:
            # 70B Versatile for complex reasoning/coding
            llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
            res = llm.invoke(f"{reasoning_prompt}\nUser Query: {user_input}")
        
        answer = res.content
        
        # Save to database
        c.execute("INSERT INTO history VALUES (?, ?)", ("user", user_input))
        c.execute("INSERT INTO history VALUES (?, ?)", ("assistant", answer))
        conn.commit()
        conn.close()
        
        return {"response": answer}

    except Exception as e:
        return {"response": f"Thinking Engine Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
