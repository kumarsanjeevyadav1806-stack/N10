import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Professional Clean CSS (Zero Icons, High Focus)
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

    /* Fixed Input Bar - Professional Position */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 30px;
        z-index: 1000;
        border-radius: 24px !important;
    }

    /* Dark Code Block */
    code {
        background-color: #1a1a1a !important;
        color: #d1d1d1 !important;
        padding: 12px !important;
        border-radius: 8px !important;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; font-weight: 800;'>Nexus Flow</h2>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"cp_{i}"):
                st.write(f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>', unsafe_allow_html=True)

# Sidebar for Image/PDF Upload
with st.sidebar:
    st.title("📂 Media Control")
    uploaded_file = st.file_uploader("Upload for Vision Analysis", type=['png', 'jpg', 'jpeg', 'pdf'])
    st.divider()
    if st.button("🗑️ Reset Brain"):
        st.session_state.messages = []
        st.rerun()

prompt = st.chat_input("Ask anything. Reasoning is active...")

if prompt:
    img_b64 = None
    if uploaded_file and uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_res = ""
        # Advanced Thinking Effect
        with st.status("Nexus is thinking...", expanded=False) as status:
            try:
                res = requests.post("https://web-production-68d0e.up.railway.app/ask", 
                                    json={"user_input": prompt, "image_b64": img_b64}, timeout=150)
                if res.status_code == 200:
                    answer = res.json().get("response")
                    status.update(label="Reasoning complete!", state="complete", expanded=False)
                    for word in answer.split():
                        full_res += word + " "
                        time.sleep(0.04)
                        placeholder.markdown(full_res + "▌")
                    placeholder.markdown(full_res)
                    st.session_state.messages.append({"role": "assistant", "content": full_res})
                    st.rerun()
                else:
                    st.error("Engine Overload. Try again.")
            except:
                st.error("Connection Interrupted.")
                
