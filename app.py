import streamlit as st
import requests
import base64
import time

# 1. Page Configuration
st.set_page_config(page_title="Nexus Flow AI", page_icon="🤖", layout="centered")

# 2. Updated CSS (Fixed Bottom ChatGPT Style Input)
st.markdown("""
    <style>
    .stApp { background-color: white; color: black; }
    
    .main .block-container {
        padding-bottom: 160px !important;
        max-width: 800px;
        margin: auto;
    }

    .stChatMessage { 
        border-radius: 20px; 
        border: none; 
        background-color: #f7f7f8; 
        padding: 20px; 
        margin-bottom: 15px;
        line-height: 1.6;
    }

    /* FIXED Bottom Input Bar */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 12px 20px;
        border-top: 1px solid #e5e5e5;
        z-index: 1000;
    }

    div[data-testid="stChatInput"] textarea {
        border-radius: 25px !important;
        padding-left: 60px !important;
        padding-right: 20px !important;
        font-size: 16px;
    }

    /* Plus Icon */
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 18px;
        left: 20px;
        z-index: 1001;
    }

    div[data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #f0f4f9 !important;
        border: none !important;
        font-size: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: 0.3s ease;
    }
    
    div[data-testid="stPopover"] > button:hover {
        background-color: #d3e3fd !important;
        transform: scale(1.05);
    }

    section.main > div {
        padding-bottom: 160px;
    }

    .copy-btn { margin-top: 10px; cursor: pointer; color: blue; font-size: 14px; }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("Nexus Flow AI 🤖⚡")

# 3. Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for i, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"📋 Copy", key=f"copy_{i}"):
                st.write(
                    f'<script>navigator.clipboard.writeText("{msg["content"].encode("unicode_escape").decode()}");</script>',
                    unsafe_allow_html=True
                )

# 4. Bottom UI

# Plus Button
with st.popover("➕"):
    st.markdown("### Attach Files 📂")
    uploaded_file = st.file_uploader(
        "Upload Image or Document",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.success(f"File '{uploaded_file.name}' is attached! ✅")

# Chat Input
prompt = st.chat_input("Ask Gemini...")

# 5. Logic
if prompt:
    img_b64 = None
    if 'uploaded_file' in locals() and uploaded_file:
        if uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
            img_b64 = base64.b64encode(uploaded_file.getvalue()).decode()

    # User message
    st.session_state.messages.append({"role": "user", "content": f"👤 {prompt}"})
    with st.chat_message("user"):
        st.markdown(f"👤 {prompt}")

    backend_url = "https://web-production-68d0e.up.railway.app/ask"

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with st.spinner("Analyzing... 🧠"):
            try:
                enhanced_prompt = f"System: Provide optimized code or fix errors. Do not explain features. Just solve it directly. Input: {prompt}"
                payload = {"user_input": enhanced_prompt, "image_b64": img_b64}

                response = requests.post(backend_url, json=payload, timeout=90)

                if response.status_code == 200:
                    answer = response.json().get("response")

                    for word in answer.split():
                        full_response += word + " "
                        time.sleep(0.04)
                        message_placeholder.markdown(full_response + "▌")

                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
                    st.rerun()
                else:
                    st.error("Engine Timeout! Please try again. 🛑")

            except:
                st.error("Connection Failed. Make sure Railway is running.")

# Sidebar
with st.sidebar:
    st.title("⚙️ Nexus Flow Memory")
    if st.button("🗑️ Reset All Chats"):
        st.session_state.messages = []
        st.rerun()
    st.info("Nexus is now in **Advanced Mode**. Memory, Vision, and Internet are enabled.")
