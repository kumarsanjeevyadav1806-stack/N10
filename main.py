import os
import uvicorn
import requests
import io
import base64
import random
from FastAPI import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration for Groq (Hugging Face Key is NOT needed now)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # 🖼️ IMAGE GENERATION FEATURE: Direct Chat in Chat (Pollinations AI)
    # Detects image requests instantly without "Warming up" error.
    image_keywords = ["draw", "generate image", "image of", "picture of", "create a photo", "make a picture"]
    if any(k in text_lower for k in image_keywords):
        # Generate a stable-diffusion-style URL (no key needed)
        prompt_slug = user_input.replace(" ", "_")
        
        # Adding a random seed for unique images each time.
        random_seed = random.randint(0, 10000)
        
        # Fast & Free Model from Pollinations AI (FLUX.1- Schnell)
        image_url = f"https://image.pollinations.ai/prompt/{prompt_slug}?width=1024&height=1024&seed={random_seed}&model=flux"
        
        try:
            # Download the image data instantly
            img_res = requests.get(image_url, timeout=90)
            if img_res.status_code == 200:
                # Convert the image to Base64 to send it as a string
                img_str = base64.b64encode(img_res.content).decode()
                return {"response": "Lo Sanjeev, Pollinations AI ne ye draw kiya hai! 🎨✨", "image": img_str}
            else:
                return {"response": "Pollinations AI is currently unavailable. Try again!"}
        except:
            return {"response": "Connection failed while drawing."}

    # 🐍 TEXT FEATURE: Advanced Chat, Coding, SAT, BSEB (Groq)
    try:
        # Most powerful Llama 3 model (ChatGPT-level)
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": "Nexus Engine is busy. Please try again in a moment."}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
