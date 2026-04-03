import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Ultra-Clean Professional CSS (No Plus Icon)
st.markdown("""
    <style>
    /* White Theme */
    .stApp { background-color: #ffffff; color: #212121; }
    
    /* Hide Everything Unnecessary */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}

    /* Content Area Styling */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 120px !important;
        max-width: 800px;
    }

    /* Professional Message Bubbles */
    .stChatMessage { 
        border-radius: 12px; 
        padding: 1.5rem; 
        margin-bottom: 1rem;
        border: 1px solid #e5e5e5;
    }
    
    /* Assistant Background */
    div[data-testid="stChatMessageAssistant"] {
        background-color: #f7f7f8 !important;
    }

    /* Fixed Bottom Search Bar - NO PLUS ICON SPACE */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        left: 0;
        right: 0;
        z-index: 1000;
        padding: 0 10% !important;
    }
    
    /* Input Field Styling */
    .stChatInput textarea {
        border-radius: 26px !important;
        border: 1px solid #d1d1d1 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    /* Code Block Styling */
    code {
        background-color: #0d0d0d !important;
        color: #f8f8f8 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("<h1 style='text-align: center; font-weight: 700;'>Nexus Flow</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Direct. Fast. Intelligent.</p>", unsafe_allow_html=True)

# 4. Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Conversation
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# 5. SIDEBAR FOR UTILITIES (Plus icon options moved here)
with st.sidebar:
    st.title("Settings & Media")
    uploaded_file = st.file_uploader("Analyze Image/PDF", type=['png', 'jpg', 'jpeg', 'pdf'])
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# 6. MAIN INPUT (The Only Entry Point)
prompt = st.chat_input("Message Nexus...")

# 7. LOGIC
if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    backend_url = "https://web-production-68d0e.up.railway.app/ask"
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        with st.spinner(" "):
            try:
                # Optimized Payload for 90B Model
                payload = {"user_input": f"Solve directly: {prompt}", "image_b64": img_b64}
                res = requests.post(backend_url, json=payload, timeout=120)
                
                if res.status_code == 200:
                    answer = res.json().get("response")
                    # Smooth Typing Animation
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
                else:
                    st.error("Engine Timeout! 🛑")
            except Exception as e:
                st.error("Connection Lost. Check Railway Status.")
                
