import os
import uvicorn
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

app = FastAPI()

# Frontend connection allow karne ke liye (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Initialization
api_key = os.getenv("GROQ_API_KEY")

# Memory ko global rakha hai taaki bot ko purani baatein yaad rahein
memory = ConversationBufferMemory()

@app.get("/")
async def root():
    return {"status": "Nexus Flow Backend is Online", "api_key_set": bool(api_key)}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is missing!")
    
    try:
        # Stable Model use kar rahe hain
        llm = ChatGroq(
            temperature=0.7, 
            groq_api_key=api_key, 
            model_name="llama3-8b-8192"
        )
        
        nexus_chain = ConversationChain(llm=llm, memory=memory)
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
  
