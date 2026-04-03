import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Premium Professional CSS (Plus Icon Removed)
st.markdown("""
    <style>
    /* Global White & Clean Theme */
    .stApp { background-color: #ffffff; color: #1f1f1f; font-family: 'Inter', sans-serif; }
    
    /* Hide Streamlit Branding */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Content Area Padding */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* Professional Chat Bubbles (ChatGPT Style) */
    .stChatMessage { 
        border-radius: 12px; 
        padding: 20px; 
        margin-bottom: 1.5rem;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Assistant Message Background */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #f9f9fb !important;
    }

    /* Fixed Bottom Search Bar (Modern Gemini/ChatGPT Style) */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        border-radius: 24px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08) !important;
    }

    /* Professional Code Block Styling */
    code {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #eee;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>Nexus Flow AI 🤖</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>God-Level Intelligence | Zero Distraction</p>", unsafe_allow_html=True)

# 3. Session State Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History with Smooth UI
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            # Direct Copy Feature
            if st.button(f"📋 Copy Response", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 4. CLEAN CHAT INPUT (No Plus Icon)
# File upload ka option hum sidebar mein shift kar dete hain for a cleaner look
with st.sidebar:
    st.title("📂 Media & Files")
    uploaded_file = st.file_uploader("Upload Image/PDF for Analysis", type=['png', 'jpg', 'jpeg', 'pdf'])
    if uploaded_file:
        st.info(f"Analyzing: {uploaded_file.name} ✅")
    
    st.divider()
    if st.button("🗑️ Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("Message Nexus...")

# 5. CORE ENGINE LOGIC
if prompt:
    # Image handling (Base64)
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User entry
    st.session_state.messages.
    
