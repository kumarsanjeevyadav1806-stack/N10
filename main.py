import os
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()

# Streamlit connection fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key handling
api_key = os.getenv("GROQ_API_KEY")

# Global memory initialization (Memory ko bahar rakhna zaroori hai)
memory_store = ConversationBufferMemory()

@app.get("/")
async def root():
    return {"status": "Nexus Flow is Live", "api_key_detected": bool(api_key)}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY missing in Railway Environment.")
    
    try:
        # LLM setup inside the request for stability
        llm = ChatGroq(
            temperature=0.7, 
            groq_api_key=api_key, 
            model_name="llama-3.3-70b-versatile"
        )
        
        # Chain setup with existing memory
        nexus_chain = ConversationChain(llm=llm, memory=memory_store)
        
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
        
    except Exception as e:
        # Error details for debugging
        raise HTTPException(status_code=500, detail=str(e))
