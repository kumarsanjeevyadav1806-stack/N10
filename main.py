import streamlit as st
import requests
import base64
import time
import re

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Clean Professional CSS
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1f1f1f; }
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Content Area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* Professional Bubbles */
    .stChatMessage { 
        border-radius: 12px; 
        padding: 1.5rem; 
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
    }

    /* Fixed Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        border-radius: 24px !important;
    }

    /* Professional Code Block Styling */
    code {
        background-color: #1a1a1a !important;
        color: #d1d1d1 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        display: block;
    }

    /* Small Copy Button Styling */
    .copy-section {
        display: flex;
        justify-content: flex-end;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-weight: 800;'>Nexus Flow</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Messages with Smart Copy Logic
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # --- SMART COPY LOGIC ---
        # Sirf tabhi Copy button dikhao jab content mein Code (```) ya specific technical keywords hon
        if msg["role"] == "assistant":
            contains_code = "```" in msg["content"]
            contains_technical = any(word in msg["content"].lower() for word in ["step 1", "solution:", "formula:", "result:", "code:"])
            
            if contains_code or contains_technical:
                # Extracting only the code part if backticks exist, else take full content
                code_match = re.findall(r'
