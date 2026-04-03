import os
import uvicorn
import requests
import io
import base64
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

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

@app.post("/ask")
async def nexus_logic(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # IMAGE GENERATION LOGIC (Direct Trigger)
    image_keywords = ["draw", "generate image", "create image", "make a picture", "image of"]
    if any(word in text_lower for word in image_keywords):
        if not HF_API_KEY:
            return {"response": "Error: Hugging Face API Key missing in Railway Variables!"}
        
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": user_input}, timeout=90)
            if response.status_code == 200:
                # Image ko Base64 string mein convert kar rahe hain taaki chat mein bheja ja sake
                img_str = base64.b64encode(response.content).decode()
                return {"response": "Here is your generated image! 🎨", "image": img_str}
            else:
                return {"response": "I tried to draw it, but the art studio is busy. Try again!"}
        except Exception as e:
            return {"response": f"Image Error: {str(e)}"}

    # NORMAL TEXT LOGIC (ChatGPT Style)
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
