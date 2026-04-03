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

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text = user_input.lower()
    
    # Direct Image Trigger Words
    img_keywords = ["draw", "generate image", "image of", "picture of", "create image"]
    
    if any(k in text for k in img_keywords):
        if not HF_API_KEY:
            return {"response": "Sanjeev, please add HF_API_KEY in Railway! 🎨"}
        
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": user_input}, timeout=120)
            if response.status_code == 200:
                img_str = base64.b64encode(response.content).decode()
                return {"response": "Lo Sanjeev, aapki image ready hai! ✨", "image": img_str}
            elif response.status_code == 503:
                return {"response": "Model is warming up. Please wait 10 seconds and try again! ⏳"}
            else:
                return {"response": "Hugging Face is busy. Try after 10 seconds."}
        except:
            return {"response": "Connection failed while drawing."}

    # Text Response logic (Coding, SAT, BSEB etc.)
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": f"Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
