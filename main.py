import os
import uvicorn
import requests
import base64
import random
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

@app.get("/")
async def root():
    return {"status": "Nexus Flow Pollinations Engine Online"}

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # Direct Image Trigger
    image_keywords = ["draw", "generate image", "image of", "picture of", "make a picture"]
    if any(k in text_lower for k in image_keywords):
        prompt_slug = user_input.replace(" ", "_")
        seed = random.randint(0, 99999)
        # Fast Model: Flux
        image_url = f"https://image.pollinations.ai/prompt/{prompt_slug}?width=1024&height=1024&seed={seed}&model=flux"
        
        try:
            img_res = requests.get(image_url, timeout=60)
            if img_res.status_code == 200:
                img_str = base64.b64encode(img_res.content).decode()
                return {"response": "Aapki image ready hai! 🎨✨", "image": img_str}
            else:
                return {"response": "Image service busy. Try again!"}
        except:
            return {"response": "Connection failed while drawing."}

    # Text Logic
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": "Nexus Engine is busy. Try after 5 seconds."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
