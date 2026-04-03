import os
import uvicorn
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
    return {"status": "Nexus Flow Fast Engine Online"}

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # Direct Image Keywords Detection
    image_keywords = ["draw", "generate image", "image of", "picture of", "make a picture", "create a photo"]
    
    if any(k in text_lower for k in image_keywords):
        # Image prompt ko URL friendly bana rahe hain
        prompt_slug = user_input.replace(" ", "%20")
        seed = random.randint(1, 999999)
        
        # Pollinations AI Direct Link (No download needed on backend)
        image_url = f"https://image.pollinations.ai/prompt/{prompt_slug}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
        
        return {
            "response": "Lo Sanjeev, aapki image ready ho rahi hai! ✨🎨",
            "image_url": image_url # Sending direct link to Streamlit
        }

    # Normal Chat Logic (Coding, SAT, BSEB etc.)
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        res = llm.invoke(user_input)
        return {"response": res.content}
    except Exception as e:
        return {"response": f"Nexus Engine is busy. Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
