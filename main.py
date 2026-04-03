import os
import uvicorn
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

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- MEMORY SETUP (Last 20 messages context) ---
if "nexus_memory" not in globals():
    global nexus_memory
    nexus_memory = ConversationBufferWindowMemory(k=20)

template = """
You are Nexus Flow AI, an elite assistant developed by Sanjeev Kumar. 
You have a perfect memory of this conversation. 
1. CODING: Provide full, optimized code for Python/C++.
2. EXAMS: Tutor for SAT and BSEB Class 12.
3. CHARACTER: Professional, smart, and supportive. Use emojis 🤖✨.

Current conversation:
{history}
Human: {input}
Nexus Flow AI:"""

PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)

@app.post("/ask")
async def ask_nexus(
    user_input: str = Body(..., embed=True),
    image_b64: str = Body(None, embed=True)
):
    try:
        # VISION LOGIC (If Image exists)
        if image_b64:
            vision_llm = ChatGroq(model_name="llama-3.2-11b-vision-preview", groq_api_key=GROQ_API_KEY)
            msg = vision_llm.invoke([
                {"role": "user", "content": [
                    {"type": "text", "text": f"Context: {user_input}. Analyze this image carefully."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                ]}
            ])
            return {"response": msg.content}

        # CHAT WITH MEMORY LOGIC
        llm = ChatGroq(temperature=0.6, groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        nexus_chain = ConversationChain(llm=llm, memory=nexus_memory, prompt=PROMPT)
        response = nexus_chain.predict(input=user_input)
        return {"response": response}

    except Exception as e:
        return {"response": f"Nexus Engine Error: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    
