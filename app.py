import streamlit as st
import requests
import base64
import time
import re

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Professional Minimalist CSS (No Plus Icon)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1f1f1f; }
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Chat Area Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 150px !important;
        max-width: 800px;
    }

    /* Message Bubbles */
    .stChatMessage { 
        border-radius: 12px; 
        padding: 1.5rem; 
        margin-bottom: 1rem;
        border: 1px solid #f0f0f0;
    }

    /* Bottom Input Pinning (Clean ChatGPT Style) */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        border-radius: 24px !important;
    }

    /* Dark Code Blocks */
    code {
        background-color: #1a1a1a !important;
        color: #d1d1d1 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-weight: 800;'>Nexus Flow AI</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat with Smart Copy Logic
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Assistant logic for Copying Code
        if msg["role"] == "assistant":
            # FIXED: One-line regex to avoid syntax errors
            code_blocks = re.findall(r'
