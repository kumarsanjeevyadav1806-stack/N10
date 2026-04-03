import streamlit as st
import requests
import base64
import time

st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# Gemini + ChatGPT Hybrid Styling
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    .main .block-container { padding-bottom: 150px; }
    
    /* Bottom Bar Container */
    .stChatInput {
        position: fixed;
        bottom: 20px;
        z-index: 1000;
        padding-left: 65px !important;
    }

    /* Floating Plus Icon */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 30px;
        left: 20px;
        z-index: 1001;
    }
    
    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 48px !important;
        height: 48px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 22px !important;
    }

    .stChatMessage { border-radius: 15px; background-color: #f7f7f8; }
    </style>
    """, unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- BOTTOM UI ---
with st.popover("➕"):
    st.markdown("### Attachments")
    uploaded_file = st.file_uploader("Photo / PDF", type=['png', 'jpg', 'jpeg', 'pdf'], label_visibility="collapsed")

prompt = st.chat_input("Ask Nexus anything...")

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
        with st.spinner("Processing..."):
            try:
                res = requests.post(backend_url, json={"user_input": prompt, "image_b64": img_b64}, timeout=90)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.05)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
            except:
                st.error("Connection Failed")
                
