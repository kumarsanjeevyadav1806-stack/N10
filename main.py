import os
import uvicorn
import random
import urllib.parse
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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # Image Keywords
    image_keywords = ["draw", "generate image", "image of", "picture of", "make a picture", "create a photo"]
    
    if any(k in text_lower for k in image_keywords):
        # 🛠️ FIX: Clean prompt for URL
        clean_prompt = urllib.parse.quote(user_input)
        seed = random.randint(1, 100000)
        
        # Pollinations AI URL (Fast & No-Logo)
        image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
        
        return {
            "response": "Lo Sanjeev, aapki image ready hai! ✨🎨",
            "image_url": image_url 
        }

    # Text Logic
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": "Nexus Engine is busy. Try again!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
