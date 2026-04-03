import os
import uvicorn
import requests
import io
import base64
import time
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
HF_API_KEY = os.getenv("HF_API_KEY")

# Sabse fast aur advanced model
HF_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text = user_input.lower()
    
    # Direct Image Trigger Words
    img_keywords = ["draw", "generate image", "image of", "picture of", "create image", "make a photo"]
    
    if any(k in text for k in img_keywords):
        if not HF_API_KEY:
            return {"response": "Sanjeev, HF_API_KEY missing in Railway! 🎨"}
        
        API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        # Retry Logic: 3 baar try karega agar model warm up ho raha ho
        for i in range(3):
            try:
                response = requests.post(API_URL, headers=headers, json={"inputs": user_input}, timeout=120)
                
                if response.status_code == 200:
                    img_str = base64.b64encode(response.content).decode()
                    return {"response": "Lo Sanjeev, aapki advanced image ready hai! ✨🚀", "image": img_str}
                
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    time.sleep(5)
                    continue
                else:
                    return {"response": f"Hugging Face Error ({response.status_code}). 10 sec baad phir try karein."}
            except Exception as e:
                return {"response": f"Drawing error: {str(e)}"}
        
        return {"response": "Model abhi bhi so raha hai (Warming up). 30 second baad ek baar aur 'Hi' bol kar image mangiye! ⏳"}

    # Text Logic (Coding, SAT, BSEB etc.)
    try:
        # Llama 3.3 70B is very stable
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": "Nexus Engine is busy. Please try again in a moment."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
