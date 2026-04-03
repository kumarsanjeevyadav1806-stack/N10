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
HF_API_KEY = os.getenv("HF_API_KEY")

# Advanced Memory
memory = ConversationBufferWindowMemory(k=10)

template = """
You are Nexus Flow AI, an extremely advanced AI developed by Sanjeev Kumar. 
1. CODING: Provide full, fixed code for Python/C++.
2. EXAMS: Tutor for SAT and BSEB.
3. IMAGES: Tell users to use the sidebar "Generate Image" tool for drawing.
4. STYLE: Professional yet friendly. Use emojis 🤖✨.

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

@app.get("/")
async def root():
    return {"status": "Nexus Flow Engine is Online"}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY Missing!")
    
    try:
        # FIXED: Using a more stable and powerful model
        llm = ChatGroq(
            temperature=0.6, 
            groq_api_key=GROQ_API_KEY, 
            model_name="llama-3.3-70b-versatile" 
        )
        nexus_chain = ConversationChain(llm=llm, memory=memory, prompt=PROMPT)
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
    except Exception as e:
        # Detailed error log
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Nexus Engine is temporarily overloaded. Try again.")

@app.post("/generate-image")
async def generate_image(image_prompt: str = Body(..., embed=True)):
    if not HF_API_KEY:
        raise HTTPException(status_code=500, detail="HF_API_KEY Missing!")
    
    API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": image_prompt}, timeout=90)
        if response.status_code == 200:
            return StreamingResponse(io.BytesIO(response.content), media_type="image/jpeg")
        else:
            raise HTTPException(status_code=response.status_code, detail="Hugging Face is loading, try again in 10s.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
