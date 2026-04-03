import os
import uvicorn
import requests
import io
from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY") # NEW: Get this from Hugging Face Settings (FREE)

# Advanced Memory
memory = ConversationBufferWindowMemory(k=10)

# ChatGPT-like Personalization + Image Capability
template = """
You are Nexus Flow AI, an extremely advanced AI developed by Sanjeev Kumar. 
Your goal is to be a supportive expert:
1. CODING: Expert in Python, C++, and Web Dev. Provide full, fixed code.
2. EXAMS: Tutor for SAT and BSEB Class 12.
3. IMAGE GENERATION: When a user asks to "generate an image" or "draw," tell them you can do it, then provide a text prompt they can use. Also, explicitly tell them to click the "Generate Image" button on the sidebar. (Streamlit limitation).
4. STYLE: Use a professional, supporting, peer-like tone. Use Hindustani expressions occasionally.

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

# Hugging Face Model for Free Image Generation
HF_IMAGE_MODEL = "runwayml/stable-diffusion-v1-5" 

@app.get("/")
async def root():
    return {"status": "Nexus Flow Advanced Image Engine is Online"}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY Missing!")
    
    try:
        # Most powerful Llama 3 model (ChatGPT-level)
        llm = ChatGroq(
            temperature=0.6, 
            groq_api_key=GROQ_API_KEY, 
            model_name="llama-3.1-405b-reasoning"
        )
        nexus_chain = ConversationChain(llm=llm, memory=memory, prompt=PROMPT)
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-image")
async def generate_image(image_prompt: str = Body(..., embed=True)):
    if not HF_API_KEY:
        raise HTTPException(status_code=500, detail="Hugging Face API Key is missing!")
    
    API_URL = f"https://api-inference.huggingface.co/models/{HF_IMAGE_MODEL}"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    try:
        # Call Hugging Face API
        response = requests.post(API_URL, headers=headers, json={"inputs": image_prompt}, timeout=90)
        if response.status_code == 200:
            return StreamingResponse(io.BytesIO(response.content), media_type="image/jpeg")
        else:
            raise HTTPException(status_code=500, detail=f"Hugging Face Error: {response.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
