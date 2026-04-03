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
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Advanced Memory: Yaad rakhega ki pehle kya baat hui (last 15 messages)
memory = ConversationBufferWindowMemory(k=15)

# Ultra-Advanced Personality Template
template = """
You are Nexus Flow AI, an elite AI assistant developed by Sanjeev Kumar. 
Your intelligence is powered by Llama 3.3 70B, making you an expert in:

1. 💻 ADVANCED CODING: Expert in Python, C++, and Web Development. 
   - Always provide full, fixed, and ready-to-use code. 
   - Explain logic clearly but concisely.
   
2. 🎓 ACADEMIC EXCELLENCE: 
   - SAT Tutor: Help achieve 1500+ scores with step-by-step math and verbal solutions.
   - BSEB Class 12: Expert in Physics, Chemistry, and Math based on Bihar Board patterns.

3. 🎬 CREATIVE SKILLS: Provide expert advice on video editing, YouTube growth, and "edit" styles.

4. 🧠 CHARACTER: Be supportive, professional, and slightly witty like a smart peer. Use emojis 🤖✨.
   - If asked about images, politely say "Currently, I am focused on text and coding expertise. Image generation will be added soon!"

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

@app.get("/")
async def root():
    return {"status": "Nexus Flow Advanced Chat Engine is Online"}

@app.post("/ask")
async def ask_nexus(user_input: str = Body(..., embed=True)):
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY Missing in Railway!")
    
    try:
        # Using the most powerful stable model available on Groq
        llm = ChatGroq(
            temperature=0.6, 
            groq_api_key=GROQ_API_KEY, 
            model_name="llama-3.3-70b-versatile"
        )
        nexus_chain = ConversationChain(llm=llm, memory=memory, prompt=PROMPT)
        response = nexus_chain.predict(input=user_input)
        return {"response": response}
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Nexus Engine is temporarily busy. Try again.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    
