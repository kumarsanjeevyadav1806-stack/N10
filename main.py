import os
import uvicorn
import requests
import io
import base64
from fastapi import FastAPI, Body, HTTPException
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

# Keys from Railway Variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

# Memory for context (ChatGPT style)
memory = ConversationBufferWindowMemory(k=10)

# ChatGPT-like Personalization (No features removed)
template = """
You are Nexus Flow AI, an extremely advanced AI developed by Sanjeev Kumar. 
1. CODING: Expert in Python, C++, and Web Dev. Provide full, fixed code always.
2. EXAMS: Specialist tutor for SAT (Target 1500+) and BSEB Class 12 (Physics, Chem, Math).
3. STYLE: Be concise, supportive, and professional. Use emojis 🤖✨.
4. IMAGE: If user asks to draw or generate an image, tell them you are creating it.

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

@app.post("/ask")
async def nexus_engine(user_input: str = Body(..., embed=True)):
    text_lower = user_input.lower()
    
    # --- FEATURE 1: DIRECT IMAGE GENERATION ---
    image_keywords = ["draw", "generate image", "image of", "picture of", "make a photo"]
    if any(k in text_lower for k in image_keywords):
        if not HF_API_KEY:
            return {"response": "Sanjeev, please add HF_API_KEY in Railway Variables for images! 🎨"}
        
        API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
        headers = {"Authorization": f"Bearer {HF_API_KEY}"}
        
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": user_input}, timeout=100)
            if response.status_code == 200:
                img_str = base64.b64encode(response.content).decode()
                return {"response": "Lo Sanjeev, aapki image tayyar hai! 🎨✨", "image": img_str}
            else:
                return {"response": "Model is warming up. Please try again in 10 seconds! ⏳"}
        except:
            return {"response": "Image generation failed. Please check connection."}

    # --- FEATURE 2: ADVANCED CHAT & CODING ---
    try:
        # Using Llama 3.3 70B for next-level intelligence
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile", temperature=0.6)
        nexus_chain = ConversationChain(llm=llm, memory=memory, prompt=PROMPT)
        answer = nexus_chain.predict(input=user_input)
        return {"response": answer}
    except Exception as e:
        return {"response": f"Nexus Engine Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
