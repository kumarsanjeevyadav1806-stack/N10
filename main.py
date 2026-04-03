import os
import uvicorn
import base64
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilyAnswer
from langchain.memory import ConversationBufferWindowMemory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys (Railway Variables mein add karein)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY") # Internet Search ke liye

memory = ConversationBufferWindowMemory(k=10)

@app.post("/ask")
async def nexus_mega_engine(
    user_input: str = Body(..., embed=True),
    image_b64: str = Body(None, embed=True) # Photo data
):
    try:
        # --- FEATURE 1: VISION (Agar Photo bheji hai) ---
        if image_b64:
            vision_llm = ChatGroq(model_name="llama-3.2-11b-vision-preview", groq_api_key=GROQ_API_KEY)
            msg = vision_llm.invoke([
                {"role": "user", "content": [
                    {"type": "text", "text": f"Sanjeev asked: {user_input}. Analyze this image and provide a detailed solution."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]}
            ])
            return {"response": msg.content}

        # --- FEATURE 2: SEARCH (Agar latest info chahiye) ---
        search_keywords = ["latest", "news", "today", "weather", "score", "current"]
        if any(word in user_input.lower() for word in search_keywords) and TAVILY_API_KEY:
            search = TavilyAnswer(tavily_api_key=TAVILY_API_KEY)
            search_res = search.run(user_input)
            return {"response": f"Internet Search Result: {search_res}"}

        # --- FEATURE 3: NORMAL CHAT (Llama 3.3 70B) ---
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", groq_api_key=GROQ_API_KEY)
        res = llm.invoke(user_input)
        return {"response": res.content}

    except Exception as e:
        return {"response": f"Nexus Mega Engine Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
