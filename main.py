import os
import uvicorn
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

# Configuration
api_key = os.getenv("GROQ_API_KEY")

# Advanced Memory: Ye pichle 10 messages yaad rakhega (ChatGPT style)
memory = ConversationBufferWindowMemory(k=10)

# ChatGPT-like Personalization
template = """
You are Nexus Flow AI, an advanced artificial intelligence developed by Sanjeev Kumar. 
Your goal is to be a multi-talented expert:
1. CODING: Expert in Python, C++, and Web Dev. Provide full, fixed code.
2. EXAMS: Expert tutor for SAT (target 1500+) and BSEB Class 12 (Maths, Physics, Chemistry).
3. STYLE: Be concise, helpful, and professional. Use a touch of wit like a supportive peer.
4. LANGUAGE: Answer in the language the user uses (Hinglish/English).

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

@app.get("/")
async def root():
    return {"status": "Nexus Flow Advanced Engine is Online"}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not api_key:
        raise HTTPException(status_code=500, detail="API Key Missing!")
    
    try:
        # Using the most powerful Llama 3 model available on Groq
        llm = ChatGroq(
            temperature=0.6, 
            groq_api_key=api_key, 
            model_name="llama-3.3-70b-versatile" 
        )
        
        # Advanced Chain with custom prompt
        nexus_chain = ConversationChain(
            llm=llm, 
            memory=memory,
            prompt=PROMPT
        )
        
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
